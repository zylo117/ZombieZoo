import argparse
import datetime
import os
import shutil
import job.get_data as get_data
import job.merge_data as merge_data

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--usr", help="username", type=str, required=True)
ap.add_argument("-p", "--pwd", help="password", type=str, required=True)
ap.add_argument("-e", "--exe", help="where mes.exe is, must use '/'", type=str, required=True)
ap.add_argument("-o", "--out", help="where the data should store", type=str, required=True)
ap.add_argument("-c", "--category", help="what the category is", type=str, required=True)
ap.add_argument("-t", "--timerange", help="from when to when, in '2099/11/11/11/11/11-2099/12/12/12/12/12'",
                type=str, default=None, required=False)
args = vars(ap.parse_args())

# open program and login
program_path = args["exe"]
get_data.open_pg(program_path)
get_data.login(args["usr"], args["pwd"])

# get data and store in into temp dir
tmp_sava_path = "c:\\temp\\"  # must use "\\" instead of "/"
today_date = datetime.datetime.now()
yesterday_date = (today_date - datetime.timedelta(days=1)).date()
today_date = "/".join(str(today_date.date()).split("-"))
yesterday_date = "/".join(str(yesterday_date).split("-"))

get_data.get_gfc_lot_data("GFCUP", "GFC-UP", yesterday_date + "/07/00/00", today_date + "/07/00/00",
                          tmp_sava_path + "gfc_up.csv",
                          interval=0.5)

get_data.get_gfc_lot_data("GFCDWN", "GFC-DWN", yesterday_date + "/07/00/00", today_date + "/07/00/00",
                          tmp_sava_path + "gfc_down.csv",
                          interval=0.5)

lens_code = ["G-818-02093-GENIUS", "G-818-02093-LARGAN", "G-818-02093-OLM", "G-818-02093-KANTATSU"]
get_data.get_material_data(lens_code, yesterday_date + "/07/00/00", today_date + "/07/00/00",
                           tmp_sava_path + "lens.csv",
                           interval=0.5)

aa_code = ["AACV125             1A", "AACV126             1A", "AACV127             1A", "AACV128             1A"]
get_data.get_material_data(aa_code, yesterday_date + "/07/00/00", today_date + "/07/00/00", tmp_sava_path + "aa.csv",
                           interval=0.5)

ircf_code = ["G-816-00424-AGC", "G-816-00424-PTOT"]
get_data.get_material_data(ircf_code, yesterday_date + "/07/00/00", today_date + "/07/00/00",
                           tmp_sava_path + "ircf.csv",
                           interval=0.5)

# move or merge the new data
if not os.path.exists(args["out"] + args["category"]):
    os.mkdir(args["out"] + args["category"])

if not os.path.exists(args["out"] + "/global_gfc_up.csv"):
    shutil.move(tmp_sava_path + "gfc_up.csv", args["out"] + "/global_gfc_up.csv")
else:
    merge_data.append_data(args["out"] + "/global_gfc_up.csv", tmp_sava_path + "gfc_up.csv")

if not os.path.exists(args["out"] + "/global_gfc_down.csv"):
    shutil.move(tmp_sava_path + "gfc_down.csv", args["out"] + "/global_gfc_down.csv")
else:
    merge_data.append_data(args["out"] + "/global_gfc_down.csv", tmp_sava_path + "gfc_down.csv")

if not os.path.exists(args["out"] + args["category"] + "/lens.csv"):
    shutil.move(tmp_sava_path + "lens.csv", args["out"] + args["category"] + "/lens.csv")
else:
    merge_data.append_data(args["out"] + args["category"] + "/lens.csv", tmp_sava_path + "lens.csv")

if not os.path.exists(args["out"] + args["category"] + "/aa.csv"):
    shutil.move(tmp_sava_path + "aa.csv", args["out"] + args["category"] + "/aa.csv")
else:
    merge_data.append_data(args["out"] + args["category"] + "/aa.csv", tmp_sava_path + "aa.csv")

if not os.path.exists(args["out"] + args["category"] + "/ircf.csv"):
    shutil.move(tmp_sava_path + "ircf.csv", args["out"] + args["category"] + "/ircf.csv")
else:
    merge_data.append_data(args["out"] + args["category"] + "/ircf.csv", tmp_sava_path + "ircf.csv")
