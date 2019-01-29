import searchtweets as st   # https://pypi.org/project/searchtweets/
import json

from twitterfloodmapper.QueryLib import QueryLib
import sys
import os

# get arguments
if len(sys.argv) == 1:
    sys.exit("Input JSON file is missing. Aborting.")
elif not os.path.isfile(sys.argv[1]):
    sys.exit("Input JSON file not found: %s" % sys.argv[1])

with open(sys.argv[1]) as r_file:
    args = json.load(r_file)

output_file_path = args["output_file_path"]
credentials_file_path = args["credentials_file_path"]
search_criteria = args["search_criteria"]
results_params = args["results_params"]

# load credentials from file
credents = st.load_credentials(filename=credentials_file_path,
                               yaml_key="search_tweets_fullarchive_dev")

# load search criteria from object
json_rules = search_criteria

# set up search query
powertrack_rule = QueryLib.convert_json_to_powertrack(json_rules)
rule = st.gen_rule_payload(powertrack_rule,
                           from_date=json_rules["time_interval_UTC"]["from"],  # UTC 2017-09-01 00:00
                           to_date=json_rules["time_interval_UTC"]["to"],
                           results_per_call=results_params["results_per_call"])

# perform request
tweets = st.collect_results(rule,
                            max_results=results_params["max_results"],
                            result_stream_args=credents)

tweet_dicts = [dict(t) for t in tweets]

with open(output_file_path, 'w') as file_w:
    json.dump(tweet_dicts, file_w, indent=4, sort_keys=True)
    print("Wrote: %s" % output_file_path)

print("Done...")
