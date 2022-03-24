#!/usr/bin/env python3

# import the library
import can
import cantools
import re
import pandas as pd
import time

# load dbc
db = cantools.database.load_file("./tests/files/sample-data/OBD2 (Audi A4)/CSS-Electronics-OBD2-v1.4.dbc")
print(db.messages)

path_to_file = "./tests/files/sample-data/OBD2 (Audi A4)/00000002_CAN.asc"

msg_dict = {}
output = []
with can.LogReader(path_to_file) as reader:
  # iterate over received messages
  for msg in reader:
    try:
      decoded = db.decode_message(msg.arbitration_id, msg.data)
    except:
      decoded = {}
      continue

    # print(msg)
    tmp_list = [
      msg.timestamp,
      msg.arbitration_id,
      msg.is_extended_id,
      msg.channel,
      msg.dlc,
      re.split('(..)', msg.data.hex().upper())[1::2],
      msg.is_fd,
      msg.is_rx,
      decoded
    ]

    msg_dict[msg.arbitration_id] = [
      msg.timestamp,
      msg.dlc,
      re.split('(..)', msg.data.hex().upper())[1::2],
      decoded]

    def clear_console(): return print('\n' * 150)
    clear_console()
    print(msg_dict)
    time.sleep(0.5)
    # print(tmp_list)
    output.append(tmp_list)

df = pd.DataFrame(output)
df.columns = ([
  "timestamp",
  "arbitration_id",
  "is_extended_id",
  "channel",
  "DLC",
  "DATA(HEX)",
  "is_fd",
  "is_rx",
  "decoded"
])

df.to_csv('output.csv')
