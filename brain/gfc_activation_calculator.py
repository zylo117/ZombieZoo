import datetime

import cv2
import pandas as pd
import numpy as np


# assume every product was tested for 5 secs
time_per_unit = 5

def cal_act(gfc_data, from_time=None, to_time=None, category=None):
    if category is not None:
        gfc_data = gfc_data[gfc_data["機種"].apply(lambda x: str(x).lower()) == category.lower()]

    data_by_mac = pd.pivot_table(gfc_data, index=gfc_data["設備"], values=["2D CODE"], aggfunc=len)
    mac_name_list = data_by_mac._stat_axis._data
    yield_val = {}
    activation_val = {}
    activation_pic = {}


    if from_time is not None and to_time is not None:
        from_time = datetime.datetime.strptime(from_time, "%Y-%m-%d %H:%M:%S")
        to_time = datetime.datetime.strptime(to_time, "%Y-%m-%d %H:%M:%S")
    else:
        from_time = datetime.datetime.strptime(str(datetime.date.today()) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        to_time = datetime.datetime.strptime(str(datetime.date.today() + datetime.timedelta(days=1)) + " 00:00:00", "%Y-%m-%d %H:%M:%S")

    for mac_name in mac_name_list:
        pd.options.mode.chained_assignment = None

        tmp_data = gfc_data[gfc_data["設備"] == mac_name]
        tmp_data["日期"] = tmp_data["日期"].astype(str)
        tmp_data["日期"] = tmp_data["日期"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

        tmp_data = tmp_data.loc[tmp_data["日期"] > from_time].loc[tmp_data["日期"] < to_time]

        ttl_qty = np.count_nonzero(tmp_data["BinNo"] > 0)
        ok_qty = np.count_nonzero(tmp_data["BinNo"] == 1)

        if ttl_qty == 0:
            yield_val[mac_name] = 0

        else:
            # get yield
            yield_val[mac_name] = ok_qty / ttl_qty

            # create time_color_bar
            ttl_sec = int((to_time - from_time).total_seconds())
            ttl_section = ttl_sec // time_per_unit
            time_color_bar = np.full([1, ttl_section, 3], 128).astype(np.uint8)

            ok_data = tmp_data[tmp_data["BinNo"] == 1]["日期"].apply(lambda x: int((x - from_time).total_seconds() // time_per_unit))
            ok_data = np.array(ok_data)
            if len(ok_data) > 0:
                ok_data[ok_data >= ttl_section] = ttl_section - 1
                # set ok color
                time_color_bar[:, ok_data, :] = [0, 255, 0]

            ng_data = tmp_data[tmp_data["BinNo"] > 1]["日期"].apply(lambda x: int((x - from_time).total_seconds() // time_per_unit))
            ng_data = np.array(ng_data)
            if len(ng_data) > 0:
                ng_data[ng_data >= ttl_section] = ttl_section - 1
                # set ng color
                time_color_bar[:, ng_data, :] = [0, 0, 255]

            # get activation
            activation = (len(ok_data) + len(ng_data)) / ttl_section
            activation_val[mac_name] = activation
            activation_pic[mac_name] = time_color_bar

            # print(0)
            # time_color_bar = cv2.resize(time_color_bar, (800, 80))
            # # time_color_bar = np.repeat(time_color_bar, 100, axis=0)
            # cv2.imshow("bar", time_color_bar)
            # cv2.waitKey(0)

    return yield_val, activation_val, activation_pic


if __name__ == "__main__":
    gfc_data = pd.read_excel("/Volumes/OSX_Data/Github/ZombieZoo/face/gfc_act.xlsx")
    result = cal_act(gfc_data, from_time="2018-5-1 00:00:00",
                     to_time="2018-5-1 11:11:11", category="GRanite-e")
    # cal_act("F:/Document/GitHub/ZombieZoo/face/000.csv")
    print(0)
