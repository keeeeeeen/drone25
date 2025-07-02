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

def log_stabalizer_callback(timestamp, data, logconf):
    print('[%d][%s]: %s' % (timestamp, logconf.name, data))

def simple_log_async(scf, logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_stabalizer_callback)
    logconf.start()
    time.sleep(5)
    logconf.stop()


if __name__ == "__main__":
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    log_stabalizer = LogConfig(name='Stabilizer', period_in_ms=10)
    log_stabalizer.add_variable('stabilizer.roll', 'float')
    log_stabalizer.add_variable('stabilizer.pitch', 'float')
    log_stabalizer.add_variable('stabilizer.yaw', 'float')

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:

        simple_log_async(scf, log_stabalizer)