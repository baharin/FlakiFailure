#some parts of this code has been taken from https://github.com/anonoymous9423013/anonymous_paper/
import random
from beamngpy import BeamNGpy, Scenario, Road, Vehicle
from beamngpy.sensors import Ultrasonic, State, Damage, Lidar
import numpy as np
from config import Config
from tester import Tester
import logging as log
import pprint
import os
import time
import math
import subprocess

desired_version = "1.24"
subprocess.check_call(['pip', 'install', f'beamngpy=={desired_version}'])

import beamngpy
from beamngpy import BeamNGpy, Scenario, Road, Vehicle

log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BNG_HOME = "...\\path_to_file\\BeamNG.tech.v0.26.2.0"


def euclidean_distance_3d(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    return distance


def FindRoad(vehiclepos, roadpoints):
    import time
    startt = time.time()

    found = False
    dists = []

    bestmin = 1000
    bestp = ''
    for rid in roadpoints:
        for p in roadpoints[rid]:

            dist = euclidean_distance_3d(vehiclepos, p['middle'])
            if dist < bestmin:
                bestmin = dist
                bestp = p


    rightdist = euclidean_distance_3d(vehiclepos, bestp['right'])
    leftdist = euclidean_distance_3d(vehiclepos, bestp['left'])

    if rightdist > leftdist:
        closeto = 'Left'
        print('the vehicle is close to the left lane')
    else:
        print('the vehicle is close to the right lane')
        closeto = 'Right'

    return closeto, bestp


def WriteToText(road_spec):
    import json

    file_path = "roaddata.txt"  # Change this to your desired file path

    with open(file_path, 'w') as file:
        json.dump(road_spec, file)

def FetchRoadNodes():

    roads = bng.get_roads()
    road_names = list(roads.keys())
    road_spec = {}
    for r_id, r_inf in roads.items():
        if r_inf['drivability'] != '-1':
            road_spec[r_id] = beamng.get_road_edges(r_id)

    WriteToText(road_spec)

    return road_spec

def executeTest(bng, config, road_spec, n=0):
    index_target_waypoint = config.target_index
    speed = config.ego_speed
    traffic_amount = config.traffic_amount
    keep_lane = 1
    weather = ['cloudy_evening', 'sunny_noon', 'sunny_evening',
               'foggy_morning', 'foggy_night', 'sunny', 'rainy'][config.weather]
    
    scenario = Scenario('west_coast_usa', 'road_map_example')
    
    ego = Vehicle('ego', model='etk800', color='White', license='SEDNA')
    
    scenario.add_vehicle(ego, pos=(-717, 101, 118), rot_quat=(0, 0, 1.5, -0.9238795))


    othervehicles = []
    for i in range(traffic_amount):
        vehicle = Vehicle('random_vehicle' + str(i), model='etk800', color = 'Red', licence='CAR' + str(i))
        othervehicles.append(vehicle)
        spawn_point = road_spec[random.choice(list(road_spec.keys()))][0]['middle']
        print('this is spawn point', spawn_point)

        scenario.add_vehicle(vehicle, pos=spawn_point)

    scenario.make(bng)
    
    bng.load_scenario(scenario)

    bng.set_deterministic()
    bng.set_steps_per_second(60)

    ultrasonic = Ultrasonic('ultrasonic', bng, ego)
    damage = Damage()
    state = State()
    lidar = Lidar("lidar", bng, ego, is_visualised=False)
    ego.attach_sensor('damage', damage)
    sensors = [ultrasonic, damage, state, lidar]

    waypoints = {w.name: w for w in scenario.find_waypoints()}
    target = list(waypoints.keys())[index_target_waypoint]
    target_pos = waypoints[target].pos
    
    bng.switch_vehicle(ego)
    
    bng.start_scenario()
    
    bng.set_weather_preset(weather)
    ego.ai_set_mode('manual')


    for i in range(traffic_amount):
        othervehicles[i].ai_set_mode('random')

    ego.ai_set_waypoint(target)
    ego.ai_drive_in_lane(keep_lane)
    ego.ai_set_speed(speed)
    for i in range(72):
        print('Step: ', i)
        bng.step(30)
        sensor_data = readSensors(ego, sensors)

        closeto, bestp = FindRoad(sensor_data[2], road_spec)

        logData(sensor_data, target_pos, config, n, closeto, bestp)


def logData(sensor_data, target_pos, config, n, passorfail, bestp):
    f_ultrasound = sensor_data[0]
    f_damage = sensor_data[1]
    f_dist = np.linalg.norm(sensor_data[2] - target_pos)
    f_lidar = np.min(sensor_data[3][sensor_data[3] > 0])
    output_folder = 'output'
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, str(config) + f'_{n}.txt')
    with open(output_file, 'a') as f:
        f.write('*' * 50 + '\n')
        f.write('Ultrasound: ' + str(f_ultrasound) + '\n')
        f.write('Damage: ' + str(f_damage) + '\n')
        f.write('Distance: ' + str(f_dist) + '\n')
        f.write('Lidar: ' + str(f_lidar) + '\n')
        f.write('ClosetoWhichLane: ' + passorfail + '\n')
        f.write('MiddlePointofRoad: ' + json.dumps(bestp) + '\n')


def readSensors(ego, sensors):
    
    ego.poll_sensors()
    ultrasonic = sensors[0]
    lidar = sensors[-1]
    ultrasonic_data = ultrasonic.poll()['distance']
    lidar_data = lidar.poll()['pointCloud']
    damage_data = ego.sensors['damage']['damage']
    state_data = ego.sensors['state']
    current_pos = np.array(state_data['pos'])
    sensor_data = [ultrasonic_data, damage_data, current_pos, lidar_data]
    return sensor_data


if __name__ == '__main__':
    import json

    file_path = "roaddata.txt"  # Path to the file containing the JSON data

    with open(file_path, 'r') as file:
        road_spec = json.load(file)

    n_repeats = 10
    input_file = 'config.txt'
    output_file = 'output.txt'
    tester = Tester(n_repeats=n_repeats)
    config_str = tester.findNextConfig()

    with BeamNGpy('localhost', 64256, home=BNG_HOME, user="...\\path_to_file\\BeamNG.tech.v0.26.2.0_user") as beamng:
        while tester.findNextConfig() != 'done':
            config_str = tester.findNextConfig()
            log.info(f'Starting new test for config {config_str}...')
            config = Config().fromStr(config_str)
            bng = beamng.open(launch=True)
            n = tester.findNoOfRepeats(config_str)
            executeTest(bng, config, road_spec, n=n)
            with open(output_file, 'a') as f:
                f.write(f'{config_str}_{n}\n')
            log.info(f'Finished repetition {n} for {config_str}...')