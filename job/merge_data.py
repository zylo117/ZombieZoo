import pandas as pd
import numpy as np
import csv

rename_dict = {"材料代码_x": "IRCF Vendor",
               "材料批号_x": "IRCF Lot",
               "在制品代码_x": "Lot",
               "交易时间_x": "FC Process Date",
               "机台代码_x": "FC Mac No",
               "交易时间_y": "AA Process Date",
               "机台代码_y": "AA Mac No",
               "材料代码": "Lens Vendor",
               "材料批号": "Lens Lot",
               "交易时间": "Lens Plasma Process Date",
               "机台代码": "Lens Plasma Mac No"}

wanted_col = ["IRCF Vendor",
              "IRCF Lot",
              "Lot",
              "FC Process Date",
              "FC Mac No",
              "AA Process Date",
              "AA Mac No",
              "Lens Vendor",
              "Lens Lot",
              "Lens Plasma Process Date",
              "Lens Plasma Mac No"]


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


def append_data(old_csv_path, new_csv_path, encoding="utf-8"):
    new_csv = pd.read_csv(new_csv_path, encoding=encoding)
    new_csv.to_csv(old_csv_path, header=False, index=False, mode="a", encoding=encoding)


def generate_material_data(ircf_csv_path, aa_csv_path, lens_csv_path):
    ircf_data = pd.read_csv(ircf_csv_path)
    # remove the irrelevance
    ircf_data = keyword_filter(ircf_data, "机台代码", "FC", 1, 3)
    # keep only the material that had been used more
    ircf_data = ircf_data.sort_values("使用量", ascending=False)
    ircf_data = ircf_data.drop_duplicates("在制品代码", keep="first")
    ircf_data = ircf_data.sort_values("序号", ascending=True)

    aa_data = pd.read_csv(aa_csv_path)
    aa_data = aa_data.sort_values("使用量", ascending=False)
    aa_data = aa_data.drop_duplicates("在制品代码", keep="first")
    aa_data = aa_data.sort_values("序号", ascending=True)

    lens_data = pd.read_csv(lens_csv_path)

    material_data = pd.merge(ircf_data, aa_data, how="left", on="在制品代码")
    material_data = pd.merge(material_data, lens_data, how="left", left_on="材料批号_y", right_on="在制品代码")

    # rename header
    material_data = header_rename(material_data, rename_dict)

    material_data = material_data[wanted_col]

    return material_data


def keyword_filter(pandas_dataframe, col_name, match_content, index_start=0, index_end=0):
    if index_start != 0 and index_end != 0:
        keyword_boolmap = pandas_dataframe[col_name].apply(
            lambda x: True if str(x)[index_start:index_end] == match_content else False)
    else:
        keyword_boolmap = pandas_dataframe[col_name].apply(lambda x: True if str(x) == match_content else False)

    return pandas_dataframe.loc[keyword_boolmap]


def header_rename(pandas_dataframe, name_dict):
    return pandas_dataframe.rename(name_dict, axis="columns")


if __name__ == "__main__":
    data_path = "c:\\temp\\"

    gfc_up_csv_path = data_path + "gfc_up.csv"
    gfc_down_csv_path = data_path + "gfc_down.csv"
    lens_csv_path = data_path + "lens.csv"
    aa_csv_path = data_path + "aa.csv"
    ircf_csv_path = data_path + "ircf.csv"

    ircf_aa_lens_gfc_all = generate_material_data(ircf_csv_path, aa_csv_path, lens_csv_path)

    ircf_aa_lens_gfc_all.to_csv(data_path + "out.csv", encoding="gbk", index=False)

    # ircf_data.to_csv(data_path + "outfuck.csv", header=False, index=False, mode="a", encoding="gbk")

    print(0)
