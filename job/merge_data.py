import time

import pandas as pd
import numpy as np
import csv

rename_dict = {"材料代码_x": "IRCF Vendor",
               "材料批号_x": "IRCF Lot",
               "在制品代码_x": "Lot",
               "交易时间_x": "FC Process Date",
               "机台代码_x": "FC Mac No",
               "制品名_x": "Product Name",
               "交易时间_y": "AA Process Date",
               "机台代码_y": "AA Mac No",
               "材料代码": "Lens Vendor",
               "材料批号": "Lens Lot",
               "交易时间": "Lens Plasma Process Date",
               "机台代码": "Lens Plasma Mac No"}

wanted_col = ["Lot",
              "Product Name",
              "FC Process Date",
              "FC Mac No",
              "IRCF Vendor",
              "IRCF Lot",
              "Lens Plasma Process Date",
              "Lens Plasma Mac No",
              "AA Process Date",
              "AA Mac No",
              "Lens Vendor",
              "Lens Lot"]


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


def generate_material_data(ircf_csv_path, aa_csv_path, lens_csv_path, encoding="utf-8"):
    ircf_data = pd.read_csv(ircf_csv_path, encoding=encoding)
    # remove the irrelevance
    ircf_data = keyword_filter(ircf_data, "机台代码", "FC", 1, 3)
    # keep only the material that had been used more, never mind, done by data input(MES system)
    # ircf_data = ircf_data.sort_values("使用量", ascending=False)
    # ircf_data = ircf_data.drop_duplicates("在制品代码", keep="first")
    # ircf_data = ircf_data.sort_values("序号", ascending=True)

    aa_data = pd.read_csv(aa_csv_path, encoding=encoding)
    # aa_data = aa_data.sort_values("使用量", ascending=False)
    # aa_data = aa_data.drop_duplicates("在制品代码", keep="first")
    # aa_data = aa_data.sort_values("序号", ascending=True)

    lens_data = pd.read_csv(lens_csv_path, encoding=encoding)

    material_data = pd.merge(ircf_data, aa_data, how="left", on="在制品代码")
    material_data = pd.merge(material_data, lens_data, how="left", left_on="材料批号_y", right_on="在制品代码")

    # rename header
    material_data = header_rename(material_data, rename_dict)

    # extract the wanted col
    material_data = material_data[wanted_col].fillna(0)

    material_data = mutate_data(material_data)

    return material_data


def merge_gfc_data(material_data, gfc_up_data_path, gfc_down_data_path):
    gfc_up_data = pd.read_csv(gfc_up_data_path)
    gfc_down_data = pd.read_csv(gfc_down_data_path)

    fusion_data = pd.merge(material_data, gfc_up_data, how="left", left_on="Lot", right_on="在制品代码")
    fusion_data = pd.merge(fusion_data, gfc_down_data, how="left", left_on="Lot", right_on="在制品代码", suffixes=("_up", "_down"))

    return fusion_data


def mutate_data(material_data):
    # move lot to the front, use wanted_col list instead
    # lot = material_data.pop("Lot")
    # material_data.insert(0, "Lot", lot)

    # add category
    material_data = insert_col(material_data, "Category", after_col_name="Lot")
    material_data["Category"] = material_data["Product Name"].apply(lambda x: _judge_category(x))

    # parse_IRCF_details
    material_data = _parse_ircf_details(material_data)

    # parse_Lens_details
    material_data = _parse_lens_details(material_data)

    return material_data


def _judge_category(x):
    category = None
    # pre-process
    category_header, category_footer = x.split("-")
    category_footer = category_footer.split("_")[0]

    sensor_model = category_header[:5].strip("IU")
    sub_category = category_header.strip("IU"+sensor_model).split("N")[-1]
    sub_config = category_footer.split("Q")[-1]

    if sensor_model == "314":
        if sub_config == "":
            return "Granite-D"
        elif sub_config == "2":
            return "Granite-C"
    elif sensor_model == "354":
        if sub_category == "":
            return "BlueBerry"
        elif sub_category == "2":
            return "Granite-E"
    elif sensor_model == "414":
        return "Angel"
    elif sensor_model == "247":
        return "Lumber"
    elif sensor_model == "190":
        if sub_config == "2":
            return "Syrup-A"
        elif sub_config == "3":
            return "Syrup-S"


def _parse_lens_details(material_data):
    # simplify Lens vendor
    material_data["Lens Vendor"] = material_data["Lens Vendor"].apply(lambda x: str(x).split("-")[-1] if x != "0" else None)
    material_data = insert_col(material_data, "Lens Parent Lot", after_col_name="Lens Lot")
    material_data["Lens Parent Lot"] = material_data["Lens Lot"].apply(lambda x: str(x)[:11] if x != "0" else None)
    # get Lens cav, tool, etc.
    material_data["Lens Factory"] = material_data["Lens Parent Lot"].apply(lambda x: str(x)[0] if x != "0" else None)
    material_data["Lens Project"] = material_data["Lens Parent Lot"].apply(lambda x: str(x)[1] if x != "0" else None)
    material_data["Lens Tool"] = material_data["Lens Parent Lot"].apply(lambda x: str(x)[2:4] if x != "0" else None)
    material_data["Lens Cavity"] = material_data["Lens Parent Lot"].apply(lambda x: str(x)[4] if x != "0" else None)
    material_data["Lens Revision"] = material_data["Lens Parent Lot"].apply(lambda x: str(x)[5:7] if x != "0" else None)
    material_data["Lens Date"] = material_data["Lens Parent Lot"].apply(lambda x: str(int(x[7], 36) + 2010) + "/" + str(int(x[8], 36)) + "/" + str(int(x[9], 36)) if x != "0" else None)

    # Category's special
    material_data["Lens Factory"].loc[material_data["Category"] == "Angel"] = material_data["Lens Factory"].apply(lambda x: str(x)[-1] if x != "nan" else np.nan)
    material_data["Lens Project"].loc[material_data["Category"] == "Angel"] = material_data["Lens Project"].apply(lambda x: str(x)[0:2] if x != "nan" else np.nan)

    return material_data


def _parse_ircf_details(material_data):
    pd.options.mode.chained_assignment = None  # default='warn' disable: SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame
    # simplify IRCF vendor
    material_data["IRCF Vendor"] = material_data["IRCF Vendor"].apply(lambda x: str(x).split("-")[-1])
    material_data = insert_col(material_data, "IRCF Parent Lot", after_col_name="IRCF Lot")
    material_data["IRCF Parent Lot"] = material_data["IRCF Lot"].apply(lambda x: str(x)[:11])
    # get IRCF details
    material_data["IRCF Polishing Site"] = material_data["IRCF Parent Lot"].apply(lambda x: str(x)[0])
    material_data["IRCF Coating Site"] = np.nan
    material_data["IRCF Coating Site"].loc[material_data["IRCF Vendor"] == "AGC"] = material_data["IRCF Parent Lot"].apply(lambda x: str(x)[1])
    material_data["IRCF Coating Site"].loc[material_data["IRCF Vendor"] == "PTOT"] = material_data["IRCF Parent Lot"].apply(lambda x: str(x)[1:3])
    material_data["IRCF Coating Site IR"] = np.nan
    material_data["IRCF Coating Site AR"] = np.nan
    material_data["IRCF Coating Site IR"].loc[material_data["IRCF Vendor"] == "PTOT"] = material_data["IRCF Parent Lot"].apply(lambda x: str(x)[1])
    material_data["IRCF Coating Site AR"].loc[material_data["IRCF Vendor"] == "PTOT"] = material_data["IRCF Parent Lot"].apply(lambda x: str(x)[2])
    material_data["IRCF BlackMask Site"] = np.nan
    material_data["IRCF BlackMask Site"].loc[material_data["IRCF Vendor"] == "AGC"] = material_data["IRCF Parent Lot"].apply(lambda x: str(x)[2])
    material_data["IRCF BlackMask Site"].loc[material_data["IRCF Vendor"] == "PTOT"] = material_data["IRCF Parent Lot"].apply(lambda x: str(x)[3])
    material_data["IRCF Dicing Site"] = np.nan
    material_data["IRCF Dicing Site"].loc[material_data["IRCF Vendor"] == "AGC"] = material_data["IRCF Parent Lot"].apply(lambda x: str(x)[3])
    material_data["IRCF Dicing Site"].loc[material_data["IRCF Vendor"] == "PTOT"] = material_data["IRCF Parent Lot"].apply(lambda x: str(x)[4])
    # get IRCF date
    material_data["IRCF Production Date"] = np.nan
    material_data["IRCF Production Date"].loc[material_data["IRCF Vendor"] == "AGC"] = material_data["IRCF Parent Lot"].apply(lambda x: str(int(str(x)[4], 36) + 2010) + "/" + str(int(str(x)[5], 36)) + "/" + str(x)[6:8])
    material_data["IRCF Production Date"].loc[material_data["IRCF Vendor"] == "PTOT"] = material_data["IRCF Parent Lot"].apply(lambda x: str(int(str(x)[5], 36) + 2010) + "/" + str(int(str(x)[6], 36)) + "/" + str(int(str(x)[7], 36)))
    return material_data


def insert_col(pandas_dataframe, new_col_name, before_col_name=None, after_col_name=None):
    col_name = pandas_dataframe.columns.tolist()
    col_name.insert(col_name.index(before_col_name), new_col_name) if after_col_name is None else col_name.insert(
        col_name.index(after_col_name) + 1, new_col_name)
    return pandas_dataframe.reindex(columns=col_name)


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

    material_data = generate_material_data(ircf_csv_path, aa_csv_path, lens_csv_path, "utf-8")
    material_data.to_csv(data_path + "material.csv", encoding="utf-8", index=False)

    fusion_data = merge_gfc_data(material_data, gfc_up_csv_path, gfc_down_csv_path)
    fusion_data = fusion_data.fillna(0)
    while True:
        try:
            fusion_data.to_csv(data_path + "fusion.csv", encoding="utf-8", index=False)
        except:
            print("File is being overwriting, please close it")
            time.sleep(3)
            continue
        finally:
            break

    # ircf_data.to_csv(data_path + "outfuck.csv", header=False, index=False, mode="a", encoding="gbk")

    print(0)
