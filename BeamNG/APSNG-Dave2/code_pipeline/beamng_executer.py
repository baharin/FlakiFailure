#This code adds additional functionalities to the beamng_executer code from https://github.com/sbft-cps-tool-competition/cps-tool-competition/tree/main
from code_pipeline.executors import AbstractTestExecutor

import time
import traceback
from typing import Tuple

from self_driving.beamng_brewer import BeamNGBrewer
# maps is a global variable in the module, which is initialized to Maps()
from self_driving.beamng_tig_maps import maps, LevelsFolder
from self_driving.beamng_waypoint import BeamNGWaypoint
from self_driving.simulation_data import SimulationDataRecord, SimulationData
from self_driving.simulation_data_collector import SimulationDataCollector
from self_driving.utils import get_node_coords, points_distance
from self_driving.vehicle_state_reader import VehicleStateReader

from shapely.geometry import Point

import logging as log
import os.path

import shutil

FloatDTuple = Tuple[float, float, float, float]


class BeamngExecutor(AbstractTestExecutor):

    def __init__(self, result_folder, map_size,
                 time_budget=None,
                 oob_tolerance=0.95, max_speed_in_kmh=70,
                 beamng_home='...\\path_to_file\\BeamNG.tech.v0.26.2.0', beamng_user='...\\path_to_file\\\\BeamNG.tech.v0.26.2.0_user', road_visualizer=None, debug=False):
        super(BeamngExecutor, self).__init__(result_folder, map_size,
                                             time_budget=time_budget, debug=debug)

        
        self.risk_value = 0.7

        self.oob_tolerance = oob_tolerance
        self.max_speed_in_ms = max_speed_in_kmh * 0.277778

        self.brewer: BeamNGBrewer = None
        self.beamng_home ='...\\path_to_file\\BeamNG.tech.v0.26.2.0'
        self.beamng_user = '...\\path_to_file\\BeamNG.tech.v0.26.2.0_user'
        
        # Runtime Monitor about relative movement of the car
        self.last_observation = None

        self.min_delta_position = 1.0
        self.road_visualizer = road_visualizer

    def _execute(self, the_test, weather):
        # Ensure we do not execute anything longer than the time budget
        super()._execute(the_test, weather)

        
        log.info("Executing test %s", the_test.id)

        
        counter = 2

        attempt = 0
        sim = None
        condition = True
        while condition:
            attempt += 1
            if attempt == counter:
                test_outcome = "ERROR"
                description = 'Exhausted attempts'
                break
            if attempt > 1:
                self._close()
            if attempt > 2:
                time.sleep(5)

            sim, minimumoob_distance, alloob_distances = self._run_simulation(the_test, weather)

            if sim.info.success:
                if sim.exception_str:
                    test_outcome = "FAIL"
                    description = sim.exception_str
                else:
                    test_outcome = "PASS"
                    description = 'Successful test'
                condition = False
            else:
                test_outcome = "INVALID"
                description = 'Apparently error happened somewhere'
                print(description)
                print(sim.exception_str)

        execution_data = sim.states

        
        return test_outcome, description, execution_data, minimumoob_distance, alloob_distances

    def _is_the_car_moving(self, last_state):
        """ Check if the car moved in the past 10 seconds """

        # Has the position changed
        if self.last_observation is None:
            self.last_observation = last_state
            return True

        # If the car moved since the last observation, we store the last state and move one
        if Point(self.last_observation.pos[0],self.last_observation.pos[1]).distance(Point(last_state.pos[0], last_state.pos[1])) > self.min_delta_position:
            self.last_observation = last_state
            return True
        else:
            # How much time has passed since the last observation?
            if last_state.timer - self.last_observation.timer > 10.0:
                return False
            else:
                return True

    def _run_simulation(self, the_test, weather) -> SimulationData:
        if not self.brewer:
            self.brewer = BeamNGBrewer(beamng_home=self.beamng_home, beamng_user=self.beamng_user)
            self.vehicle = self.brewer.setup_vehicle()

        # For the execution we need the interpolated points
        nodes = the_test.interpolated_points

        brewer = self.brewer
        brewer.setup_road_nodes(nodes)
        beamng = brewer.beamng
        waypoint_goal = BeamNGWaypoint('waypoint_goal', get_node_coords(nodes[-1]))

        # Override default configuration passed via ENV or hardcoded
        if self.beamng_user is not None:
            try:
                os.chdir('...\\path_to_file\\BeamNG.tech.v0.26.2.0_user\\0.26')
                shutil.rmtree('...\\path_to_file\\BeamNG.tech.v0.26.2.0_user\\0.26\\levels\\tig')
            except Exception as e:
                print('While removing...', e)
            # Note This changed since BeamNG.research
            beamng_levels = LevelsFolder(os.path.join(self.beamng_user, '0.26', 'levels'))
            maps.beamng_levels = beamng_levels
            maps.beamng_map = maps.beamng_levels.get_map('tig')
            # maps.print_paths()

        maps.install_map_if_needed()
        maps.beamng_map.generated().write_items(brewer.decal_road.to_json() + '\n' + waypoint_goal.to_json())

        vehicle_state_reader = VehicleStateReader(self.vehicle, beamng)
        brewer.vehicle_start_pose = brewer.road_points.vehicle_start_pose()

        steps = brewer.params.beamng_steps
        simulation_id = time.strftime('%Y-%m-%d--%H-%M-%S', time.localtime())
        name = 'beamng_executor/sim_$(id)'.replace('$(id)', simulation_id)
        sim_data_collector = SimulationDataCollector(self.vehicle, beamng, brewer.decal_road, brewer.params,
                                                     vehicle_state_reader=vehicle_state_reader,
                                                     simulation_name=name)

        
        sim_data_collector.oob_monitor.tolerance = self.oob_tolerance

        sim_data_collector.get_simulation_data().start()

        try:
            brewer.bring_up(weather)

            brewer.vehicle.ai_set_aggression(self.risk_value)
            #  Sets the target speed for the AI in m/s, limit means this is the maximum value (not the reference one)
            brewer.vehicle.ai_set_speed(self.max_speed_in_ms, mode='limit')
            brewer.vehicle.ai_drive_in_lane(True)
            brewer.vehicle.ai_set_waypoint(waypoint_goal.name)

            alloob_distances = []

            startt = time.time()
            oobbb = False

            while True:

                sim_data_collector.collect_current_data(oob_bb=True)

                alloob_distances.append(sim_data_collector.states[-1].oob_distance)


                last_state: SimulationDataRecord = sim_data_collector.states[-1]
                # Target point reached
                if points_distance(last_state.pos, waypoint_goal.position) < 8.0:
                    break

                assert self._is_the_car_moving(last_state), "Car is not moving fast enough " + str(
                    sim_data_collector.name)

                #this line needs to be commented:
                # assert not last_state.is_oob, "Car drove out of the lane " + str(sim_data_collector.name)

                if last_state.is_oob == True:
                    print('Car drove out of lane---------------')
                    oobbb = True

                beamng.step(steps, wait=False)

            sim_data_collector.get_simulation_data().end(success=True)
        except AssertionError as aex:
            # An assertion that trigger is still a successful test execution, otherwise it will count as ERROR
            sim_data_collector.get_simulation_data().end(success=True, exception=aex)
            traceback.print_exception(type(aex), aex, aex.__traceback__)
        except Exception as ex:
            sim_data_collector.save()
            sim_data_collector.get_simulation_data().end(success=False, exception=ex)
            traceback.print_exception(type(ex), ex, ex.__traceback__)
        finally:
            sim_data_collector.save()
            if oobbb == True:
                try:
                    sim_data_collector.get_simulation_data().end(success=True, exception=AssertionError)
                except Exception as ex:
                    sim_data_collector.get_simulation_data().end(success=False, exception=ex)
                    alloob_distances = [1000]

        

            self._close()

        minimumoob_distance = min(alloob_distances)

        return sim_data_collector.simulation_data, minimumoob_distance, alloob_distances

    def end_iteration(self):
        try:
            if self.brewer:
                self.brewer.beamng.stop_scenario()
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)

    def _close(self):
        if self.brewer:
            try:
                # replicating beamng close method. The issue is that the kill_beamng method is not called for some
                # reason
                if self.brewer.beamng.scenario:
                    self.brewer.scenario.close()
                    self.brewer.scenario = None
                self.brewer.beamng.kill_beamng()

                time.sleep(2)

            except Exception as ex:
                traceback.print_exception(type(ex), ex, ex.__traceback__)
            self.brewer = None
