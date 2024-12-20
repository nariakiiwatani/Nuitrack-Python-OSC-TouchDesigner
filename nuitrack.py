from PyNuitrack import py_nuitrack

import os
from os.path import join, dirname
from dotenv import load_dotenv
import argparse

from pythonosc import udp_client
from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder

all_joint_names = [
    'head',
    'neck',
    'torso',
    'waist',
    'left_collar',
    'left_shoulder',
    'left_elbow',
    'left_wrist',
    'left_hand',
    'right_collar',
    'right_shoulder',
    'right_elbow',
    'right_wrist',
    'right_hand',
    'left_hip',
    'left_knee',
    'left_ankle',
    'right_hip',
    'right_knee',
    'right_ankle',
]

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

REALSENSE_SERIAL_NUMBER = os.environ.get('REALSENSE_SERIAL_NUMBER')
NUITRACK_API_KEY = os.environ.get('NUITRACK_API_KEY')

if REALSENSE_SERIAL_NUMBER is None or REALSENSE_SERIAL_NUMBER == "":
    print('REALSENSE_SERIAL_NUMBER is not set')
    print('Please set it in .env file')
    exit(1)

parser = argparse.ArgumentParser(description='Nuitrack OSC Sender',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-ip', '--osc_to_ip', type=str, default='127.0.0.1', help='OSC destination IP')
parser.add_argument('-port', '--osc_to_port', type=int, default=12345, help='OSC destination port')
# note: specify use joint names with args
parser.add_argument('-j', '--joint_names', type=str, nargs='+', default=all_joint_names, help='Joint names to send OSC')

args = parser.parse_args()

osc_to_ip = args.osc_to_ip
osc_to_port = args.osc_to_port
osc_client = udp_client.SimpleUDPClient(osc_to_ip, osc_to_port)
print("OSC to " + osc_to_ip + ":" + str(osc_to_port) + " ...")

nuitrack = py_nuitrack.Nuitrack()
nuitrack.init()

devices = nuitrack.get_device_list()

print('Connected devices:')
for i, dev in enumerate(devices):
    print(dev.get_name(), dev.get_serial_number())
    
device_activated = False
for i, dev in enumerate(devices):
    if dev.get_serial_number() == REALSENSE_SERIAL_NUMBER:
        dev.activate(NUITRACK_API_KEY) #you can activate device using python api
        # print(dev.get_activation())
        nuitrack.set_device(dev)
        device_activated = True
        break
    
if not device_activated:
    print('Device with serial number {} not found'.format(REALSENSE_SERIAL_NUMBER))
    exit(1)

print('Activated device: ', dev.get_name(), dev.get_serial_number())

nuitrack.create_modules()
nuitrack.run()


def make_osc_message(address, arg_value, arg_type):
    msg = osc_message_builder.OscMessageBuilder(address=address)
    msg.add_arg(arg_value, arg_type)
    return msg.build()

try:
    print("Press 'Ctrl+C' to exit")

    def nuitrack_cycle():
        nuitrack.update()
        data = nuitrack.get_skeleton()

        bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
        
        for i in range(data.skeletons_num):
            prefix = f'p{i+1}'
            sk = data.skeletons[i]
            bundle.add_content(make_osc_message(f'/{prefix}/id', sk.user_id, 'i'))
            for joint_name in args.joint_names:
                pos = getattr(sk, joint_name).real
                bundle.add_content(make_osc_message(f'/{prefix}/{joint_name}:tx', pos[0]/1000, 'f'))
                bundle.add_content(make_osc_message(f'/{prefix}/{joint_name}:ty', pos[1]/1000, 'f'))
                bundle.add_content(make_osc_message(f'/{prefix}/{joint_name}:tz', pos[2]/1000, 'f'))
        
        osc_client.send(bundle.build())

    while True:
        nuitrack_cycle()

except KeyboardInterrupt:
    print("KeyboardInterrupt")

except Exception as e:
    print(e)

finally:
    try:
        nuitrack.release()
    except Exception as e:
        print(e)

    print("Bye")
    exit(0)