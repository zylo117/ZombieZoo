import argparse
import os
import shutil

import job.get_data as get_data

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--usr", help="username", required=True)
ap.add_argument("-p", "--pwd", help="password", required=True)
ap.add_argument("-e", "--exe", help="where mes.exe is, must use '/'", required=True)
ap.add_argument("-o", "--out", help="where the data should store", required=True)
ap.add_argument("-t", "--timerange", help="from when to when, in '2099/11/11/11/11/11-2099/12/12/12/12/12'", default=None, required=False)
args = vars(ap.parse_args())

program_path = args["exe"]
get_data.open_pg(program_path)
get_data.login(args["usr"], args["pwd"])

tmp_sava_path = "c:\\temp\\"  # must use "\\" instead of "/"

get_data.get_gfc_lot_data("GFCUP", "GFC-UP", "2018/04/19/01/01/01", "2018/04/23/01/01/01", tmp_sava_path + "gfc.csv",
                          interval=0.5)

lens_code = ["G-818-02093-GENIUS", "G-818-02093-LARGAN", "G-818-02093-OLM", "G-818-02093-KANTATSU"]
get_data.get_material_data(lens_code, "2018/04/17/01/01/00", "2018/04/19/01/01/00", tmp_sava_path + "lens.csv",
                           interval=0.5)

aa_code = ["AACV125             1A", "AACV126             1A", "AACV127             1A", "AACV128             1A"]
get_data.get_material_data(aa_code, "2018/04/17/01/01/00", "2018/04/19/01/01/00", tmp_sava_path + "aa.csv", interval=0.5)

ircf_code = ["G-816-00424-AGC", "G-816-00424-PTOT"]
get_data.get_material_data(ircf_code, "2018/04/17/01/01/00", "2018/04/19/01/01/00", tmp_sava_path + "ircf.csv",
                           interval=0.5)

# move or merge the new data
if not os.path.exists(args["out"]):
    os.mkdir(args["out"])

if not os.path.exists(args["out"] + "\\gfc.csv"):
    shutil.move(tmp_sava_path + "gfc.csv", args["out"] +"\\gfc.csv")

if not os.path.exists(args["out"] + "\\lens.csv"):
    shutil.move(tmp_sava_path + "lens.csv", args["out"] +"\\lens.csv")

if not os.path.exists(args["out"] + "\\aa.csv"):
    shutil.move(tmp_sava_path + "aa.csv", args["out"] +"\\aa.csv")

if not os.path.exists(args["out"] + "\\ircf.csv"):
    shutil.move(tmp_sava_path + "ircf.csv", args["out"] +"\\ircf.csv")
