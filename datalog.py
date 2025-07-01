import logging
logging.basicConfig(level=logging.ERROR)

import time

import cflib.crtp #Scans for CF instances

from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

from cflib.utils import uri_helper



uri = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

def simple_log(scf, logconf):
  with SyncLogger(scf, logconf) as logger:
        for log_entry in logger:
            timestamp = log_entry[0]
            data = log_entry[1]
            logconf_name = log_entry[2]

            print('[%d][%s]: %s' % (timestamp, logconf_name, data))



if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    stabilizer_log = LogConfig(name='Stabilizer', period_in_ms=10)
    stabilizer_log.add_variable('stabilizer.roll', 'float')
    stabilizer_log.add_variable('stabilizer.pitch', 'float')
    stabilizer_log.add_variable('stabilizer.yaw', 'float')

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        simple_log(scf, stabilizer_log)


