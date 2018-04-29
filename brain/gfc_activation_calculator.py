import datetime

import cv2
import pandas as pd
import numpy as np


# assume every product was tested for 5 secs

def cal_act(gfc_data_path, from_time=None, to_time=None):
    raw_data = pd.read_csv(gfc_data_path)
    data_by_mac = pd.pivot_table(raw_data, index=raw_data["設備"], values=["2D CODE"], aggfunc=len)
    mac_name_list = data_by_mac._stat_axis._data
    result = {}

    if from_time is not None and to_time is not None:
        from_time = datetime.datetime.strptime(from_time, "%Y-%m-%d %H:%M:%S")
        to_time = datetime.datetime.strptime(to_time, "%Y-%m-%d %H:%M:%S")
    else:
        from_time = datetime.datetime.strptime(str(datetime.date.today()) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        to_time = datetime.datetime.strptime(str(datetime.date.today() + datetime.timedelta(days=1)) + " 00:00:00", "%Y-%m-%d %H:%M:%S")

    for mac_name in mac_name_list:
        tmp_data = raw_data[raw_data["設備"] == mac_name]
        tmp_data["日期"] = tmp_data["日期"].apply(lambda x: datetime.datetime.strptime(x, "%Y/%m/%d %H:%M:%S"))

        tmp_data = tmp_data.loc[tmp_data["日期"] > from_time].loc[tmp_data["日期"] < to_time]

        ttl_qty = np.count_nonzero(tmp_data["BinNo"] > 0)
        ok_qty = np.count_nonzero(tmp_data["BinNo"] == 1)

        activation = ok_qty / ttl_qty

        result[mac_name] = activation

    return result


if __name__ == "__main__":
    result = cal_act("F:/Document/GitHub/ZombieZoo/face/000.csv", from_time="2018-04-28 12:50:50", to_time="2018-04-28 18:50:50")
    # cal_act("F:/Document/GitHub/ZombieZoo/face/000.csv")
    print(0)
