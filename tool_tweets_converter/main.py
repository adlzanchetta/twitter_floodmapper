import json
import sys
import os
import re

# Reads the content of a JSON file generated by XYZ.py and converts into two CSV files
# Output files:
# - twitts_geo.csv: twitts that are geotagged
#     Collumns: twitt_id, date, user_id, user_name, text, lat, lng
# - twitts_plain.csv: twitts that are not geotagged
#     Collumns: twitt_id, date, user_id, user_name, text

# Variable naming definitions
# fipa: file path
# fopa: folder path

# get arguments
if len(sys.argv) < 3:
    sys.exit("Input json file path and/or output folder path is missing. Aborting.")
elif not os.path.isfile(sys.argv[1]):
    sys.exit("Input JSON file not found: %s" % sys.argv[1])
all_twitts_json_fipa = sys.argv[1]
out_fopa = sys.argv[2]

# define output files path
geo_twitts_csv_fipa = os.path.join(out_fopa, "twitter_geo.csv")
plain_twitts_csv_fipa = os.path.join(out_fopa, "twitter_plain.csv")

# open JSON file and read data
with open(all_twitts_json_fipa, "r") as r_file:
    all_data = json.load(r_file)

    twitts_geo, twitts_plain = [], []
    clean_text = lambda s: re.sub('[^a-zA-Z0-9\#\!\?\,\/ \.]', '', str(s)).strip()
    for cur_data in all_data:

        # read common attributes
        twitt_id = clean_text(cur_data["id_str"])
        twitt_date = "\"%s\"" % clean_text(cur_data["created_at"])
        user_id = clean_text(cur_data["user"]["id_str"])
        user_name = clean_text(cur_data["user"]["name"].replace(";", ","))
        user_name = "\"%s\"" % user_name
        twitt_text = clean_text(cur_data["text"].replace(";", ","))
        twitt_text = "\"%s\"" % twitt_text

        # read geographic data if available
        if ("coordinates" in cur_data.keys()) and (cur_data["coordinates"] is not None):
            obj = cur_data["coordinates"]["coordinates"]
            lat, lng = str(obj[1]), str(obj[0])
        elif ("geo" in cur_data.keys()) and (cur_data["geo"] is not None):
            obj = cur_data["geo"]["coordinates"]
            lat, lng = str(obj[0]), str(obj[1])
        else:
            lat, lng = None, None

        # check if has media (usually it is a photo)
        if "entities" in cur_data.keys():
            obj = cur_data["entities"]
            if ("media" in obj.keys()) and (len(obj["media"]) > 0):
                has_media = True
            else:
                has_media = False
        else:
            has_media = False

        # add to proper list
        if lat is None:
            obj = (twitt_id, twitt_date, user_id, user_name, twitt_text)
            twitts_plain.append(obj)
        else:
            obj = (twitt_id, twitt_date, user_id, user_name, twitt_text, lat, lng)
            twitts_geo.append(obj)

# write file - geo twitts
if len(twitts_geo) == 0:
    print("No geolocatted twitts found.")
else:
    print("Found %i geolocatted twitts." % len(twitts_geo))
    with open(geo_twitts_csv_fipa, "w", encoding="utf-8") as w_file:
        w_file.write("twitt_id; date; user_id; user_name; text; lat; lng\n")
        [w_file.write("%s\n" % "; ".join(obj)) for obj in twitts_geo]
    print(" Wrote: %s" % geo_twitts_csv_fipa)

# write file - plain twitts
if len(twitts_plain) == 0:
    print("No plain twitts found.")
else:
    print("Found %i plain twitts." % len(twitts_plain))
    with open(plain_twitts_csv_fipa, "w") as w_file:
        w_file.write("twitt_id; date; user_id; user_name; text\n")
        [w_file.write("%s\n" % "; ".join(obj)) for obj in twitts_plain]
    print(" Wrote: %s" % plain_twitts_csv_fipa)
