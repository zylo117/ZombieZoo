import datetime
import os

import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# assume every product was tested for 5 secs
time_per_unit = 5
total_index_qty = 12

# set o/s(open/short, electrical) failure bin no.
os_bin_conf = open("./BIN_OS.conf", "rb").read().decode().splitlines()[1:]
os_bin_list = {}
for b in os_bin_conf:
    b = b.split(",")
    os_bin_list[b[0]] = b[1:]


def cal_act(gfc_data, from_time=None, to_time=None, category=None, output=None):
    if category is not None:
        category = category.lower()
        gfc_data = gfc_data[gfc_data["機種"].apply(lambda x: str(x).lower()) == category]

        # get os bin list
        os_bin = os_bin_list[category]
    else:
        # get os bin list
        os_bin = os_bin_list["default"]

    data_by_mac = pd.pivot_table(gfc_data, index=gfc_data["設備"], values=["機種"], aggfunc=len)
    mac_name_list = data_by_mac._stat_axis._data
    yield_val = {}
    activation_val = {}
    activation_pic = {}
    osfr = {}
    osfr_sheet_by_index = [pd.DataFrame(index=mac_name_list, columns=np.arange(1, 13), data=0) for i in range(len(os_bin))]

    if from_time is not None and to_time is not None:
        from_time = datetime.datetime.strptime(from_time, "%Y-%m-%d %H:%M:%S")
        to_time = datetime.datetime.strptime(to_time, "%Y-%m-%d %H:%M:%S")
    else:
        from_time = datetime.datetime.strptime(str(datetime.date.today()) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        to_time = datetime.datetime.strptime(str(datetime.date.today() + datetime.timedelta(days=1)) + " 00:00:00", "%Y-%m-%d %H:%M:%S")

    # output the final data
    output_data = {}

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

            tmp_data["BinNo"] = tmp_data["BinNo"].astype(str)
            os_map = np.array(tmp_data["BinNo"].apply(lambda x: x in os_bin))
            os_data = tmp_data[os_map]
            os_data_backup = tmp_data[os_map]
            os_data = os_data["日期"].apply(lambda x: int((x - from_time).total_seconds() // time_per_unit))
            os_data = np.array(os_data)
            if len(os_data) > 0:
                os_data[os_data >= ttl_section] = ttl_section - 1
                # set ng color
                time_color_bar[:, os_data, :] = [255, 0, 0]

            # get activation
            activation = (len(ok_data) + len(ng_data)) / ttl_section
            activation_val[mac_name] = activation
            activation_pic[mac_name] = time_color_bar

            # time_color_bar = cv2.resize(time_color_bar, (800, 80))
            # # time_color_bar = np.repeat(time_color_bar, 100, axis=0)
            # cv2.imshow("bar", time_color_bar)
            # cv2.waitKey(0)

            # get os failure rate
            osfr_qty = np.count_nonzero(os_map)
            osfr[mac_name] = osfr_qty / ttl_qty

            # get os failure rate by index
            ttl_index_pivot_table = pd.pivot_table(tmp_data, index=tmp_data["UnitIndex"], values=["UnitIndex"], aggfunc=len)
            ttl_index_list = ttl_index_pivot_table._stat_axis._data.astype(int) - 1
            ttl_by_index = np.zeros(12)
            ttl_by_index[ttl_index_list] = np.array(ttl_index_pivot_table["UnitIndex"])

            # calculate every bin failure rate
            os_data_backup["BinNo"] = os_data_backup["BinNo"].astype(str)
            for i in range(len(os_bin)):
                os_failure_index_data = os_data_backup[os_data_backup["BinNo"] == os_bin[i]]
                os_failure_index_pivot_table = pd.pivot_table(os_failure_index_data, index=os_failure_index_data["UnitIndex"], values=["UnitIndex"], aggfunc=len)
                os_index_list = os_failure_index_pivot_table._stat_axis._data.astype(int) - 1

                if len(os_index_list) > 0:
                    osfr_by_index = np.zeros(12)
                    osfr_by_index[os_index_list] = np.array(os_failure_index_pivot_table["UnitIndex"])

                    # osfr_by_index = osfr_by_index / ttl_by_index
                    # osfr_by_index = np.divide(osfr_by_index, ttl_by_index, out=np.zeros_like(osfr_by_index), where=ttl_by_index != 0)

                    osfr_by_index = np.nan_to_num(osfr_by_index)

                    osfr_sheet_by_index[i].loc[mac_name] = osfr_by_index

        if output is not None:
            output_data[mac_name] = pd.DataFrame(data=0, index=os_bin, columns=np.arange(1, 14).astype(str))
            for i in range(len(os_bin)):
                # add the Sum/I
                output_data[mac_name].iloc[i] = np.hstack([osfr_sheet_by_index[i].loc[mac_name], np.sum(osfr_sheet_by_index[i].loc[mac_name])])

    if output is not None:
        # transform output_data to flat data
        flat_index = category
        for mac_name in mac_name_list:
            flat_index = np.hstack((flat_index, mac_name, os_bin, "Sum/B", ""))
        flat_output = pd.DataFrame(data=0, index=flat_index, columns=np.arange(1, 14).astype(str))
        bin_count = len(os_bin) + 2  # 8
        for i in range(len(mac_name_list)):
            flat_output.iloc[i * (bin_count + 1) + 2: i * (bin_count + 1) + bin_count - 1] = output_data[mac_name_list[i]]

            # calculate the Sum/B
            flat_output.iloc[i * (bin_count + 1) + bin_count, :] = flat_output.iloc[i * (bin_count + 1) + 2: i * (bin_count + 1) + bin_count - 1, :].apply(lambda x: np.sum(x))

        # change to percentage
        # flat_output = flat_output.applymap(lambda x: "%.3f" % (100 * x) + "%")

        # title and data fixing
        for i in range(len(mac_name_list)):
            flat_output.iloc[i * (bin_count + 1)] = None
            flat_output.iloc[i * (bin_count + 1) + 1] = np.hstack([np.arange(1, 13), "Sum/I"])
            # flat_output.iat[i * (bin_count + 1) + bin_count, 12] = "%.3f" % (100 * osfr[mac_name_list[i]]) + "%"

        # output
        dir = "/".join(output.split("/")[:-1])
        if not os.path.exists(dir):
            os.makedirs(dir)
        flat_output.to_csv(output, header=None, encoding="utf-8")

    return yield_val, activation_val, activation_pic, osfr


if __name__ == "__main__":
    gfc_data = pd.read_excel("./gfc_act_simple.xlsx")
    result = cal_act(gfc_data, from_time="2018-5-1 00:00:00", to_time="2018-5-1 1:00:00", category="GRanite-e", output="./result.csv")
    # cal_act("F:/Document/GitHub/ZombieZoo/face/000.csv")
    print(0)
