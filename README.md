# Twitter Floodmapper

*Harvesting and machine learning scripts for mapping flood-related messages.*

This project consists of a toolset and datasets for extracting, manipulating and interpreting historical Twitter data. The initial objective of this project is to explore patterns in such messages to enhance the flood monitoring capabilities of natural hazard -related agencies and authorities, but with minor adaptations those tools are expected to be appliable for other purposes.

Following is a brief description of each folder/component in the root directory. Further details of each component can be found in the inner README file of each directory.

**tool_tweets_harvester**:  Plain Python tool for performing searches in historical tweets. Data is downloaded into raw ```json``` format.

**tool_tweets_file_converter**: Plain Python tool for converting the ```json``` tweet files into other formats such as ```csv```.

**data_tweets**: Sets of twitts retrieved using the harvesting tool.
