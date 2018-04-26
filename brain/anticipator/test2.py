import job.merge_data as merge_data
import pandas as pd
import numpy as np

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

    fuck = pd.pivot_table(fusion_data, index=["Category_Config"], columns=["GFC-UP Process Date 7:00"], aggfunc=np.sum)
    print(0)
