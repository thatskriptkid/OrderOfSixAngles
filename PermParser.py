# -*- coding: utf-8 -*-
import numpy as np
import argparse
import glob
import subprocess
import matplotlib.pyplot as plt;

plt.rcdefaults()

parser = argparse.ArgumentParser()
parser.add_argument("dir", type=str, help="folder with apk files")
args = parser.parse_args()

common_permissions = {"INTERNET": 0, "READ_EXTERNAL_STORAGE": 0, "READ_CALENDAR": 0, "WRITE_CALENDAR": 0,
                      "PROCESS_OUTGOING_CALLS": 0, "CAMERA": 0, "READ_CONTACTS": 0, "WRITE_CONTACTS": 0,
                      "GET_ACCOUNTS": 0, "ACCESS_FINE_LOCATION": 0, "ACCESS_COARSE_LOCATION": 0,
                      "RECORD_AUDIO": 0, "READ_PHONE_STATE": 0, "READ_PHONE_NUMBERS": 0, "CALL_PHONE": 0,
                      "ANSWER_PHONE_CALLS": 0, "ADD_VOICEMAIL": 0, "USE_SIP": 0, "BODY_SENSORS": 0,
                      "SEND_SMS": 0, "RECEIVE_SMS": 0, "READ_SMS": 0, "RECEIVE_WAP_PUSH": 0, "RECEIVE_MMS": 0,
                      "WRITE_EXTERNAL_STORAGE": 0, "READ_CALL_LOG": 0, "WRITE_CALL_LOG": 0}

file_list = glob.glob(args.dir + "\\*.apk")

for f in file_list:
    f = f.decode('cp1251').encode('utf8')
    parse_result = subprocess.check_output(
        ["aapt", "dump", "permissions", f])

    pkgs_info = parse_result.splitlines()

    for permission, _ in common_permissions.items():
        for pkg_info in pkgs_info:
            if permission in pkg_info:
                common_permissions[permission] += 1

objects_list = []
performance_list = []

for k, v in common_permissions.items():
    objects_list.append(k)
    performance_list.append(v)

objects = tuple(objects_list)

y_pos = np.arange(len(objects))

plt.rcParams.update({'font.size': 9})

plt.barh(y_pos, performance_list)
plt.yticks(y_pos, objects)
plt.xlabel('Number of apk')
plt.title('Permissions usage')

plt.show()
