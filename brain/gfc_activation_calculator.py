import datetime

import cv2
import pandas as pd
import numpy as np


# assume every product was tested for 5 secs

def cal_act(gfc_data_path, from_time=None, to_time=None):
    raw_data = pd.read_csv(gfc_data_path)
    data_by_mac = pd.pivot_table(raw_data, index=raw_data["設備"], values=["2D CODE"], aggfunc=len)
    mac_name_list = data_by_mac._stat_axis._data

    for mac_name in mac_name_list:
        tmp_data = raw_data[raw_data["設備"] == mac_name]
        tmp_data["日期"] = tmp_data["日期"].apply(lambda x: datetime.datetime.strptime(x, "%Y/%m/%d %H:%M:%S"))

        if from_time is not None:
            from_time = datetime.datetime.strptime(from_time, "%Y/%m/%d %H:%M:%S")
            tmp_data = tmp_data["日期"].loc[tmp_data["日期"] > from_time]

        ttl_qty = np.count_nonzero(tmp_data["BinNo"] > 0)
        ok_qty = np.count_nonzero(tmp_data["BinNo"] == 1)
        activation = ok_qty / ttl_qty

        print(0)


if __name__ == "__main__":
    cal_act("F:/Document/GitHub/ZombieZoo/face/000.csv", from_time="2018/04/28 12:50:50")
