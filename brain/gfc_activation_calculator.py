import datetime

import cv2
import pandas as pd
import numpy as np


# assume every product was tested for 5 secs
time_per_unit = 8

def cal_act(gfc_data, from_time=None, to_time=None, category=None):
    if category is not None:
        gfc_data = gfc_data[gfc_data["機種"].apply(lambda x: str(x).lower()) == category.lower()]

    data_by_mac = pd.pivot_table(gfc_data, index=gfc_data["設備"], values=["2D CODE"], aggfunc=len)
    mac_name_list = data_by_mac._stat_axis._data
    result = {}

    if from_time is not None and to_time is not None:
        from_time = datetime.datetime.strptime(from_time, "%Y-%m-%d %H:%M:%S")
        to_time = datetime.datetime.strptime(to_time, "%Y-%m-%d %H:%M:%S")
    else:
        from_time = datetime.datetime.strptime(str(datetime.date.today()) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        to_time = datetime.datetime.strptime(str(datetime.date.today() + datetime.timedelta(days=1)) + " 00:00:00", "%Y-%m-%d %H:%M:%S")

    for mac_name in mac_name_list:
        pd.options.mode.chained_assignment = None

        tmp_data = gfc_data[gfc_data["設備"] == mac_name]
        tmp_data["日期"] = tmp_data["日期"].apply(lambda x: datetime.datetime.strptime(x, "%Y/%m/%d %H:%M:%S"))

        tmp_data = tmp_data.loc[tmp_data["日期"] > from_time].loc[tmp_data["日期"] < to_time]

        ttl_qty = np.count_nonzero(tmp_data["BinNo"] > 0)
        ok_qty = np.count_nonzero(tmp_data["BinNo"] == 1)

        if ttl_qty == 0:
            result[mac_name] = 0

        else:
            activation = ok_qty / ttl_qty

            result[mac_name] = activation

            # create time_color_bar
            ttl_sec = int((to_time - from_time).total_seconds())
            ttl_section = ttl_sec // time_per_unit
            time_color_bar = np.full([1, ttl_section, 3], 128).astype(np.uint8)

            ok_data = tmp_data[tmp_data["BinNo"] == 1]["日期"].apply(lambda x: int((x - from_time).total_seconds() // time_per_unit))
            ok_data = np.array(ok_data)
            ng_data = tmp_data[tmp_data["BinNo"] > 1]["日期"].apply(lambda x: int((x - from_time).total_seconds() // time_per_unit))
            ng_data = np.array(ng_data)

            # set ok color
            time_color_bar[:, ok_data, :] = [0, 255, 0]

            # set ng color
            time_color_bar[:, ng_data, :] = [0, 0, 255]

            print(0)
            time_color_bar = cv2.resize(time_color_bar, (800, 80))
            # time_color_bar = np.repeat(time_color_bar, 100, axis=0)
            cv2.imshow("bar", time_color_bar)
            cv2.waitKey(0)

    return result


if __name__ == "__main__":
    gfc_data = pd.read_csv("F:/Document/GitHub/ZombieZoo/face/000.csv")
    result = cal_act(gfc_data, from_time="2018-04-28 12:00:00",
                     to_time="2018-04-28 18:00:00", category="GRanite-C")
    # cal_act("F:/Document/GitHub/ZombieZoo/face/000.csv")
    print(0)
