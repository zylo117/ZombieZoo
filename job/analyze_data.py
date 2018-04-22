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


if __name__ == "__main__":
    data_path = "c:\\temp\\"

    gfc_csv_path = data_path + "gfc.csv"
    gfc_data = pd.read_csv(gfc_csv_path)

    lens_csv_path = data_path + "lens.csv"
    len_data = pd.read_csv(lens_csv_path)

    aa_csv_path = data_path + "aa.csv"
    aa_data = pd.read_csv(aa_csv_path)

    ircf_csv_path = data_path + "ircf.csv"
    ircf_data = pd.read_csv(ircf_csv_path)

    print(0)
