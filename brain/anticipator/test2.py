import hands.merge_data as merge_data
import pandas as pd
import numpy as np
from brain.anticipator.holt_winters_prediction import HoltWintersPrediction
import matplotlib.pyplot as plt

gfc_lcb_items = ["GFC-UP Input Quantity",
                 "10_Bin17_LCB(center)",
                 "11_Bin18_LCB(edge)",
                 "12_Bin19_LCB(corner)",
                 "76_Bin22_LCBraw",
                 "77_Bin23_LCBaccum",
                 "GFC-DOWN Input Quantity",
                 "01_Bin17_LCB(center)",
                 "02_Bin18_LCB(edge)",
                 "03_Bin19_LCB(corner)",
                 "77_Bin22_LCBraw",
                 "78_Bin23_LCBaccum",
                 "79_Bin25_LCB_Retest_Count"]

if __name__ == "__main__":
    data_path = "c:\\temp\\"

    gfc_up_csv_path = data_path + "gfc_up.csv"
    gfc_down_csv_path = data_path + "gfc_down.csv"
    lens_csv_path = data_path + "lens.csv"
    aa_csv_path = data_path + "aa.csv"
    ircf_csv_path = data_path + "ircf.csv"

    material_data = merge_data.generate_material_data(ircf_csv_path, aa_csv_path, lens_csv_path, "utf-8")
    material_data.to_csv(data_path + "material.csv", encoding="utf-8", index=False)

    # load csv from either file or memory
    fusion_data = merge_data.merge_gfc_data(material_data, gfc_up_csv_path, gfc_down_csv_path)

    # pre-process starts
    fusion_data["LCB_UP_QTY"] = fusion_data["10_Bin17_LCB(center)"] + fusion_data["11_Bin18_LCB(edge)"] + fusion_data[
        "12_Bin19_LCB(corner)"] + fusion_data["76_Bin22_LCBraw"] + fusion_data["77_Bin23_LCBaccum"]
    fusion_data["LCB_DOWN_QTY"] = fusion_data["01_Bin17_LCB(center)"] + fusion_data["02_Bin18_LCB(edge)"] + fusion_data[
        "03_Bin19_LCB(corner)"] + fusion_data["77_Bin22_LCBraw"] + fusion_data["78_Bin23_LCBaccum"] + fusion_data[
                                      "79_Bin25_LCB_Retest_Count"]

    fusion_data["Category_Config"] = fusion_data["Category_Config"].apply(lambda x: str(x))
    fusion_pivot = pd.pivot_table(fusion_data, index=["Category_Config", "GFC-UP Process Date 7:00"], columns=[],
                                  values=["GFC-UP Input Quantity", "LCB_UP_QTY",
                                           "GFC-DOWN Input Quantity", "LCB_DOWN_QTY"], aggfunc=np.sum)

    fusion_pivot["LCB Failure Rate"] = fusion_pivot["LCB_UP_QTY"] / fusion_pivot["GFC-UP Input Quantity"] + \
                                       fusion_pivot["LCB_DOWN_QTY"] / fusion_pivot["GFC-DOWN Input Quantity"]

    category_list = pd.pivot_table(fusion_data, index=["Category_Config"], values=["GFC-UP Input Quantity", ])
    category_list = category_list._stat_axis._data
    category_list = [str(i) for i in category_list]

    fusion_pivot_list = []
    for category in category_list:
        pivot = fusion_pivot.query("Category_Config == ['%s']" % category)
        fusion_pivot_list.append(pivot)
        # pivot.to_csv("C:/TEMP/%s_pivot.csv" % category)

    e3_lcb_test_trend = fusion_pivot_list[-1]["LCB Failure Rate"].tolist()
    e1_lcb_test_trend = fusion_pivot_list[-1]["LCB Failure Rate"].tolist()

    lcb_hw3 = HoltWintersPrediction(e3_lcb_test_trend, forecast_len=50, forecast_method="additive")
    lcb_hw1 = HoltWintersPrediction(e1_lcb_test_trend, forecast_len=50, forecast_method="additive")

    lcb_forecast3 = lcb_hw3.predict()
    lcb_forecast1 = lcb_hw1.predict()
    plt.figure(1)
    # plt.subplot(211)
    plt.plot(np.hstack([e3_lcb_test_trend, lcb_forecast3[22:]]), label='lcb_forecast_E3')
    plt.plot(e3_lcb_test_trend, label='e3_lcb_test_trend')
    plt.legend()
    plt.axis([0, 80, 0.002, 0.006])

    # plt.subplot(212)
    # plt.plot(lcb_forecast1, label='lcb_forecast_E1')
    # plt.plot(e3_lcb_test_trend, label='e1_lcb_test_trend')
    # plt.legend()
    # plt.axis([0, 80, 0.002, 0.006])


    plt.show()


    print(0)
