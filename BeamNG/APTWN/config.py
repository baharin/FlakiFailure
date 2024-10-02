#some parts of this code has been taken from https://github.com/anonoymous9423013/anonymous_paper/
import random
import logging as log
import numpy as np

log.basicConfig(level=log.INFO)

class Config:
    def __init__(self, target_index=None, ego_speed=None, traffic_amount=None, weather=None):
        self.target_index = target_index
        self.ego_speed = ego_speed
        self.traffic_amount = traffic_amount
        self.weather = weather
        self.configarray = []
    
    def __str__(self):
        return f'{self.target_index}, {self.ego_speed}, {self.traffic_amount}, {self.weather}'

    def fromStr(self, config_str):
        config = config_str.strip().rstrip().split(',')
        config = [x.strip().rstrip() for x in config]
        self.target_index = int(config[0])
        self.ego_speed = float(config[1])
        self.traffic_amount = int(config[2])
        self.weather = int(config[3])
        return self

    def generateRandomConfig(self):
        # weathers = ['cloudy_evening', 'sunny_noon', 'sunny_evening',
        #             'foggy_morning', 'foggy_night', 'sunny', 'rainy']
        self.configarray = []

        self.target_index = random.randint(0, 4)
        self.ego_speed = random.randint(5, 50)
        self.traffic_amount = random.randint(0, 10)
        self.weather = random.randint(0, 6)

        self.configarray.append(self.target_index)
        self.configarray.append(self.ego_speed)
        self.configarray.append(self.traffic_amount)
        self.configarray.append(self.weather)


def ComputeDistance(point, selectedpoints):
    distances = []
    for i in range(len(selectedpoints)):
        d = np.linalg.norm(np.array(point) - np.array(selectedpoints[i]))
        distances.append(d)

    return min(distances)


def ConvertoStr(newselectedpoint):

    return f'{newselectedpoint[0]}, {newselectedpoint[1]}, {newselectedpoint[2]}, {newselectedpoint[3]}'

def GeneratePointsNaiveAdaptiveSearch(config):

    selectedpoints = []
    strselectedpoints = []
    config.generateRandomConfig()
    selectedpoints.append(config.configarray)
    strselectedpoints.append(str(config))

    while len(selectedpoints) < 20:
        distancesofallpoints = []
        randompoints = []
        for i in range(10):
            config.generateRandomConfig()
            randompoints.append(config.configarray)

        for i in range(len(randompoints)):
            minn = ComputeDistance(randompoints[i], selectedpoints)
            distancesofallpoints.append(minn)

        newselectedpoint = randompoints[distancesofallpoints.index(max(distancesofallpoints))]
        selectedpoints.append(newselectedpoint)
        strselectedpoints.append(ConvertoStr(newselectedpoint))

    return selectedpoints, strselectedpoints

if __name__ == '__main__':
    config = Config()
    output_file = 'config.txt'
    n_configs = 200
    configs = []
    for i in range(int(n_configs/20)):
        tests, strtests = GeneratePointsNaiveAdaptiveSearch(config)
        for k in range(len(strtests)):
            configs.append(strtests[k])

    configs.sort()
    with open(output_file, 'w') as f:
        for config in configs:
            f.write(config + '\n')
        f.write('done')
            
    log.info(f'Generated {n_configs} configs and saved to {output_file}!')