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


def generate_material_data(ircf_csv_path, aa_csv_path, lens_csv_path, encoding="utf-8"):
    ircf_data = pd.read_csv(ircf_csv_path, encoding=encoding)
    # remove the irrelevance
    ircf_data = keyword_filter(ircf_data, "机台代码", "FC", 1, 3)
    # keep only the material that had been used more
    ircf_data = ircf_data.sort_values("使用量", ascending=False)
    ircf_data = ircf_data.drop_duplicates("在制品代码", keep="first")
    ircf_data = ircf_data.sort_values("序号", ascending=True)

    aa_data = pd.read_csv(aa_csv_path, encoding=encoding)
    aa_data = aa_data.sort_values("使用量", ascending=False)
    aa_data = aa_data.drop_duplicates("在制品代码", keep="first")
    aa_data = aa_data.sort_values("序号", ascending=True)

    lens_data = pd.read_csv(lens_csv_path, encoding=encoding)

    material_data = pd.merge(ircf_data, aa_data, how="left", on="在制品代码")
    material_data = pd.merge(material_data, lens_data, how="left", left_on="材料批号_y", right_on="在制品代码")

    # rename header
    material_data = header_rename(material_data, rename_dict)

    # extract the wanted col
    material_data = material_data[wanted_col]

    material_data = mutate_data(material_data)

    return material_data


def mutate_data(material_data):
    # move lot to the front
    lot = material_data.pop("Lot")
    material_data.insert(0, "Lot", lot)

    # parse_IRCF_details
    material_data = _parse_IRCF_details(material_data)

    # parse_Lens_details
    # simplify Lens vendor
    material_data["Lens Vendor"] = material_data["Lens Vendor"].apply(lambda x: str(x).split("-")[-1])

    return material_data


def _parse_IRCF_details(material_data):
    # simplify IRCF vendor
    material_data["IRCF Vendor"] = material_data["IRCF Vendor"].apply(lambda x: str(x).split("-")[-1])
    material_data = insert_col(material_data, "IRCF Parent Lot", after_col_name="IRCF Lot")
    material_data["IRCF Parent Lot"] = material_data["IRCF Lot"].apply(lambda x: str(x)[:11])
    # get IRCF details
    material_data["IRCF Polishing Site"] = material_data["IRCF Parent Lot"].apply(lambda x: str(x)[0])
    material_data["IRCF Coating Site"] = np.nan
    material_data["IRCF Coating Site"][material_data["IRCF Vendor"] == "AGC"] = material_data["IRCF Parent Lot"].apply(
        lambda x: str(x)[1])
    material_data["IRCF Coating Site"][material_data["IRCF Vendor"] == "PTOT"] = material_data["IRCF Parent Lot"].apply(
        lambda x: str(x)[1:3])
    material_data["IRCF Coating Site IR"] = np.nan
    material_data["IRCF Coating Site AR"] = np.nan
    material_data["IRCF Coating Site IR"][material_data["IRCF Vendor"] == "PTOT"] = material_data[
        "IRCF Parent Lot"].apply(lambda x: str(x)[1])
    material_data["IRCF Coating Site AR"][material_data["IRCF Vendor"] == "PTOT"] = material_data[
        "IRCF Parent Lot"].apply(lambda x: str(x)[2])
    material_data["IRCF BlackMask Site"] = np.nan
    material_data["IRCF BlackMask Site"][material_data["IRCF Vendor"] == "AGC"] = material_data[
        "IRCF Parent Lot"].apply(lambda x: str(x)[2])
    material_data["IRCF BlackMask Site"][material_data["IRCF Vendor"] == "PTOT"] = material_data[
        "IRCF Parent Lot"].apply(lambda x: str(x)[3])
    material_data["IRCF Dicing Site"] = np.nan
    material_data["IRCF Dicing Site"][material_data["IRCF Vendor"] == "AGC"] = material_data["IRCF Parent Lot"].apply(
        lambda x: str(x)[3])
    material_data["IRCF Dicing Site"][material_data["IRCF Vendor"] == "PTOT"] = material_data["IRCF Parent Lot"].apply(
        lambda x: str(x)[4])
    # get IRCF date
    material_data["IRCF Production Date"] = np.nan
    material_data["IRCF Production Date"][material_data["IRCF Vendor"] == "AGC"] = material_data[
        "IRCF Parent Lot"].apply(
        lambda x: str(int(str(x)[4], 36) + 2010) + "/" + str(int(str(x)[5], 36)) + "/" + str(x)[6:8])
    material_data["IRCF Production Date"][material_data["IRCF Vendor"] == "PTOT"] = material_data[
        "IRCF Parent Lot"].apply(
        lambda x: str(int(str(x)[5], 36) + 2010) + "/" + str(int(str(x)[6], 36)) + "/" + str(int(str(x)[7], 36)))
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

    ircf_aa_lens_gfc_all = generate_material_data(ircf_csv_path, aa_csv_path, lens_csv_path, "utf-8")

    ircf_aa_lens_gfc_all.to_csv(data_path + "out.csv", encoding="gbk", index=False)

    # ircf_data.to_csv(data_path + "outfuck.csv", header=False, index=False, mode="a", encoding="gbk")

    print(0)
