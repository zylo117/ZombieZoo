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

if args["timerange"] is None:
    new_date = datetime.datetime.now()
    old_date = (new_date - datetime.timedelta(days=1)).date()
    new_date = "/".join(str(new_date.date()).split("-")) + "/07/00/00"
    old_date = "/".join(str(old_date).split("-")) + "/07/00/00"
else:
    old_date, new_date = args["timerange"].split("-")

category = args["category"]  # could be "BlueBerry", "Angel", "MerMaid", "Lumber", "Syrup", "Cotton"

# get_data.get_gfc_lot_data("GFCUP", "GFC-UP", old_date, new_date, category, tmp_sava_path + "gfc_up.csv", interval=0.5)
#
# get_data.get_gfc_lot_data("GFCDWN", "GFC-DWN", old_date, new_date, category, tmp_sava_path + "gfc_down.csv", interval=0.5)
#
# lens_code = ["G-818-02093-GENIUS", "G-818-02093-LARGAN", "G-818-02093-OLM", "G-818-02093-KANTATSU"]
# get_data.get_material_data(lens_code, old_date, new_date, tmp_sava_path + "lens.csv", interval=0.5)
#
# aa_code = ["AACV125             1A", "AACV126             1A", "AACV127             1A", "AACV128             1A"]
# get_data.get_material_data(aa_code, old_date, new_date, tmp_sava_path + "aa.csv", interval=0.5)
#
# ircf_code = ["G-816-00424-AGC", "G-816-00424-PTOT"]
# get_data.get_material_data(ircf_code, old_date, new_date, tmp_sava_path + "ircf.csv", interval=0.5)

# move or merge the new data
target_path = args["out"] + args["category"] + "/"

if not os.path.exists(target_path):
    os.makedirs(target_path)

# backup old data
backup_path = args["out"] + args["category"] + "/backup/"
try:
    shutil.copytree(target_path, backup_path + str(datetime.datetime.now().date()) + "/",
                    ignore=shutil.ignore_patterns("backup"))
except:
    pass
# delete old backups
fuck = os.walk(backup_path)
for dirpath, dirname, filename in os.walk(backup_path):
    if dirpath != backup_path:
        date = dirpath.split("/")[-1].split("-")
        year, month, day = [int(i) for i in date]
        if (datetime.date.today() - datetime.date(year, month, day)).days > 7:
            shutil.rmtree(dirpath)

if not os.path.exists(target_path + "gfc_up.csv"):
    shutil.move(tmp_sava_path + "gfc_up.csv", target_path + "gfc_up.csv")
else:
    merge_data.append_data(target_path + "gfc_up.csv", tmp_sava_path + "gfc_up.csv")

if not os.path.exists(target_path + "gfc_down.csv"):
    shutil.move(tmp_sava_path + "gfc_down.csv", target_path + "gfc_down.csv")
else:
    merge_data.append_data(target_path + "gfc_down.csv", tmp_sava_path + "gfc_down.csv")

if not os.path.exists(target_path + "lens.csv"):
    shutil.move(tmp_sava_path + "lens.csv", target_path + "lens.csv")
else:
    merge_data.append_data(target_path + "lens.csv", tmp_sava_path + "lens.csv")

if not os.path.exists(target_path + "aa.csv"):
    shutil.move(tmp_sava_path + "aa.csv", target_path + "aa.csv")
else:
    merge_data.append_data(target_path + "aa.csv", tmp_sava_path + "aa.csv")

if not os.path.exists(target_path + "ircf.csv"):
    shutil.move(tmp_sava_path + "ircf.csv", target_path + "ircf.csv")
else:
    merge_data.append_data(target_path + "ircf.csv", tmp_sava_path + "ircf.csv")

# output merged data
# generate the merged data
gfc_up_csv_path = target_path + "gfc_up.csv"
gfc_down_csv_path = target_path + "gfc_down.csv"
lens_csv_path = target_path + "lens.csv"
aa_csv_path = target_path + "aa.csv"
ircf_csv_path = target_path + "ircf.csv"

ircf_aa_lens_gfc_all = merge_data.generate_material_data(ircf_csv_path, aa_csv_path, lens_csv_path)
if not os.path.exists(target_path + "material_data.csv"):
    ircf_aa_lens_gfc_all.to_csv(target_path + "material_data.csv", encoding="utf-8", index=False)
else:
    ircf_aa_lens_gfc_all.to_csv(target_path + "material_data.csv", header=False, index=False, mode="a", encoding="utf-8")
