import pandas as pd
import numpy as np
import csv


def read_csv_purepython(csv_path):
    f = open(csv_path, 'r', encoding="utf-8")
    reader = csv.reader(f)
    data = []
    for row in reader:
        data.append(row)
    header = data[0]
    header = np.asarray(header)
    data = data[1:]
    data = np.asarray(data)

    return header, data


def append_data(old_csv_path, new_csv_path, encoding="gbk"):
    new_csv = pd.read_csv(new_csv_path)
    new_csv.to_csv(old_csv_path, header=False, index=False, mode="a", encoding=encoding)


def generate_lcb_data(ircf_csv_path, aa_csv_path, lens_csv_path, gfc_up_csv_path, gfc_down_csv_path):
    ircf_data = pd.read_csv(ircf_csv_path)
    aa_data = pd.read_csv(aa_csv_path)
    lens_data = pd.read_csv(lens_csv_path)
    gfc_up_data = pd.read_csv(gfc_up_csv_path)
    gfc_down_data = pd.read_csv(gfc_down_csv_path)

    ircf_aa = pd.merge(ircf_data, aa_data, how="left", on="在制品代码")
    ircf_aa_lens = pd.merge(ircf_aa, lens_data, how="left", left_on="材料批号_y", right_on="在制品代码")
    ircf_aa_lens_gfc_up = pd.merge(ircf_aa_lens, gfc_up_data, how="left", left_on="在制品代码_x", right_on="在制品代码")
    ircf_aa_lens_gfc_all = pd.merge(ircf_aa_lens_gfc_up, gfc_down_data, how="left", left_on="在制品代码_x",
                                    right_on="在制品代码").fillna(0)
    return ircf_aa_lens_gfc_all


if __name__ == "__main__":
    data_path = "c:\\temp\\"

    gfc_up_csv_path = data_path + "gfc_up.csv"
    gfc_down_csv_path = data_path + "gfc_down.csv"
    lens_csv_path = data_path + "lens.csv"
    aa_csv_path = data_path + "aa.csv"
    ircf_csv_path = data_path + "ircf.csv"

    ircf_aa_lens_gfc_all = generate_lcb_data(ircf_csv_path, aa_csv_path, lens_csv_path, gfc_up_csv_path, gfc_down_csv_path)

    ircf_aa_lens_gfc_all.to_csv(data_path + "out.csv", encoding="gbk")

    # ircf_data.to_csv(data_path + "outfuck.csv", header=False, index=False, mode="a", encoding="gbk")

    print(0)
