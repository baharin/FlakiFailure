import os
import random
import sys
import time
import errno
import importlib
import logging as log
import traceback
import shutil
import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.getcwd(), 'self_driving'))
sys.path.append(os.path.join(os.getcwd(), 'sample_test_generators'))
from deepjanus_seed_generator import *
# from sample_test_generators.deepjanus_seed_generator import *


beamng_home = '...\\path_to_file\\BeamNG.tech.v0.26.2.0'
beamng_user = '...\\path_to_file\\BeamNG.tech.v0.26.2.0_user'

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

OUTPUT_RESULTS_TO = 'results'
module_name = 'deepjanus_seed_generator'
class_name = 'OurAmbieGenGenerator'

module = importlib.import_module(module_name)
the_class = getattr(module, class_name)


default_output_folder = os.path.join(get_script_path(), OUTPUT_RESULTS_TO)
try:
    os.makedirs(default_output_folder)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

timestamp_id = time.time() * 100000000 // 1000000
result_folder = os.path.join(default_output_folder,
                             "_".join([str(module_name), str(class_name), str(timestamp_id)]))
try:
    os.makedirs(result_folder)
except OSError:
    log.fatal("An error occurred during test generation")
    traceback.print_exc()
    sys.exit(2)

executor = 'beamng'

map_size = 200
time_budget = 100
if executor == 'beamng':
    oob_tolerance = 0.85 
else:
    oob_tolerance = 0.95

road_visualizer = None

def ComputeDistance(point, selectedpoints):
    distances = []
    for i in range(len(selectedpoints)):
        d = np.linalg.norm(np.array(point) - np.array(selectedpoints[i]))
        distances.append(d)

    return min(distances)

def InitialGeneratePoint():

    weathers = ['cloudy_evening', 'sunny_noon', 'sunny_evening',
                'foggy_morning', 'foggy_night', 'sunny', 'rainy']

    p=[]
    weather = random.randint(0, 6)

    if executor == 'beamng':

        speed_limit = random.randint(5, 100)  
        max_angle = random.randint(40, 100)
    else:
        speed_limit = random.randint(5, 10) 
        max_angle = random.randint(3, 20) 

    p.append(weather)
    p.append(speed_limit)
    p.append(max_angle)

    return p


def GeneratePointsNaiveAdaptiveSearch():

    selectedpoints = []
    newarray = InitialGeneratePoint()
    selectedpoints.append(newarray)

    while len(selectedpoints) < 20:
        distancesofallpoints = []
        randompoints = []
        for i in range(10):
            randompoints.append(InitialGeneratePoint())

        for i in range(len(randompoints)):
            minn = ComputeDistance(randompoints[i], selectedpoints)
            distancesofallpoints.append(minn)

        newselectedpoint = randompoints[distancesofallpoints.index(max(distancesofallpoints))]
        selectedpoints.append(newselectedpoint)

    return selectedpoints

roaaaddata = pd.DataFrame(columns = ['Index', 'RoadPoints', 'InterpolatedPoints', 'MinimumOOBDistance', 'MaxCurvature', 'Weather', 'Maxspeed', 'MAX_ANGLE', 'TestOutcome'])

roaaaddata.to_excel('...\\path_to_file\\roaddata.xlsx', index = False)


roaaaddata = pd.read_excel('...\\path_to_file\\roaddata.xlsx')


startt = time.time()
c= 0
while len(roaaaddata.index) < 2000:

    tests = GeneratePointsNaiveAdaptiveSearch()  # 20 points

    for i in range(len(tests)):

        
        from code_pipeline.beamng_executor import BeamngExecutor

        the_executor = BeamngExecutor(result_folder, map_size,
                                        time_budget=time_budget,
                                        oob_tolerance=oob_tolerance, max_speed_in_kmh=tests[i][1],
                                        beamng_home=beamng_home, beamng_user=beamng_user,
                                        road_visualizer=road_visualizer)

        test_generator = the_class(executor=the_executor, map_size=map_size, weather = tests[i][0], maxspeed = tests[i][1], max_angle = tests[i][2])
        test_generator.start()

    
    roaaaddata = pd.read_excel('...\\path_to_file\\roaddata.xlsx')

    
    time.sleep(1)
