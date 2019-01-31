import searchtweets as st   # https://pypi.org/project/searchtweets/
import json

from twitterfloodmapper.QueryLib import QueryLib
import requests
import sys
import os

# get arguments
if len(sys.argv) == 1:
    sys.exit("Input JSON file is missing. Aborting.")
elif not os.path.isfile(sys.argv[1]):
    sys.exit("Input JSON file not found: %s" % sys.argv[1])

# read arguments file
with open(sys.argv[1]) as r_file:
    args = json.load(r_file)
output_file_path = args["output_file_path"]
credentials_file_path = args["credentials_file_path"]
search_criteria = args["search_criteria"]
results_params = args["results_params"]
del args

# load credentials from file
credents = st.load_credentials(filename=credentials_file_path,
                               yaml_key="search_tweets_fullarchive_dev")

# set up search query
if "powertrack" in search_criteria.keys():
    powertrack_rule = search_criteria["powertrack"]
else:
    powertrack_rule = QueryLib.convert_json_to_powertrack(search_criteria)

# basic check
if powertrack_rule is None:
    sys.exit("Aborting: Unable to define powertrack rule.")
elif len(powertrack_rule) > 128:
    sys.exit("Aborting: Powertrack rule got too big (limit is %d, got %d chars)." % (128, len(powertrack_rule)))
else:
    print("Powertrack query size: %d." % len(powertrack_rule))

rule = st.gen_rule_payload(powertrack_rule,
                           from_date=search_criteria["time_interval_UTC"]["from"],  # UTC 2017-09-01 00:00
                           to_date=search_criteria["time_interval_UTC"]["to"],
                           results_per_call=results_params["results_per_call"])

# perform request
try:
    tweets = st.collect_results(rule,
                                max_results=results_params["max_results"],
                                result_stream_args=credents)
except requests.exceptions.HTTPError as e:
    sys.exit(e)

# write output file in json format
tweet_dicts = [dict(t) for t in tweets]
print("Retrieved %d twitts (possible constraint: %d max_result)." % (len(tweet_dicts), results_params["max_results"]))
with open(output_file_path, 'w') as file_w:
    json.dump(tweet_dicts, file_w, indent=4, sort_keys=True)
    print("Wrote: %s" % output_file_path)
