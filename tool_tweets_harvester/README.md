# Tweets harvester

*Plain Python tool for performing searches in historical tweets.*

## About

This tool basically:

1. Connects to the Twitter historical API;
2. Converts ```json``` data request into ```powertrack``` query if needed;
3. Saves obtained results to a local ```json``` file.

It was tested in Python 3.7 and depends on the module [searchtweets](https://pypi.org/project/searchtweets/).

## Usage

All arguments must be provided in a ```json``` file (structure described as following).

A typical call would be in the form of:

    $ python main.py some_file_path.json

The choice for using ```json``` file format for arguments comes from:

1. Facilitates the readability: as the number of parameters can be huge;
2. Easily association of "search request" -> "search result" by saving the request ```json``` file with the returned ```json``` file.

### JSON arguments file

The ```json``` file is expected to hold a dictionary object with pre-defined set of keys (described later on).

An example of arguments file would have a content given by:

    {
        "output_file_path": "/(...)/output.json",
        "credentials_file_path": "/(...)/credentials.txt",
        "results_params":{
            "results_per_call": 100,
            "max_results": 50
        },
        "search_criteria": {
            "keywords_in": ["flood", "flooded", "inundation", "inundated", "#tostorm", "#stormto"],
            "keywords_out": ["mana"],
            "users_out": [],
            "time_interval_UTC": {
                "from": "2013-07-08",
                "to": "2013-07-09"
            },
            "area_circle": {
                "center_lat_WGS": 0,
                "center_lng_WGS": 0,
                "radius_mi": 0
            },
            "area_place": "Toronto"
        }
    }

So the following set of key -> structure is expected:

- **output_file_path**: String. Path of the output ```json``` file to be written.
- **credentials_file_path**: String. Path of the plain ```text``` used my ```searchtweets``` tool for Twitter API credentials.
- **results_params**: Dictionary with the following keys:
  - **results_per_call**: Integer. 
  - **max_results**: Integer. Expected to be smaller than ```results_per_call```.
- **search_criteria**: Dictionary or string with ```powertrack``` syntax. If dictionary:
  - **keywords_in**: List of strings. At least one of the strings must be present in the retrieved twitter.
  - **keywords_out**: List of strings. Twitts with one or more of the strings listed will be ignored.
  - **users_out**: ```TODO``` - *not implemented yet*
  - **time_interval_UTC**. Dictionary with the following keys:
    - **from**: String. Date-time in ```YYYY-MM-DD``` format describe the earliest date-time accepted.
    - **to**: String. Date-time in ```YYYY-MM-DD``` format describe the latest date-time accepted.
  - **area_circle**: ```TODO``` - *not implemented yet*
  - **area_place**: String. The name of a constraining location. If present, only geolocated twitts are considered.
