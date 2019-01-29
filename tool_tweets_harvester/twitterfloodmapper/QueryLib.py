
class QueryLib:

    @staticmethod
    def convert_json_to_powertrack(json_dictionary):
        """
        Converts the easy-to-read json object into a string in powertrack format
        :param json_dictionary:
        :return: String if possible to build PowerTrack tag. None otherwise.
        """

        ret_list = []

        if "keywords_in" in json_dictionary.keys():
            tmp = ") OR (".join(json_dictionary["keywords_in"])
            tmp = "( (%s) )" % tmp
            ret_list.append(tmp)

        if "keywords_out" in json_dictionary.keys():
            tmp = ") OR (".join(json_dictionary["keywords_out"])
            tmp = "-( (%s) )" % tmp
            ret_list.append(tmp)

        # TODO - set up other rules

        if "area_place" in json_dictionary.keys():
            '''
            tmp = ') OR (place:'.join(json_dictionary["area_place"])
            tmp = '( (place:%s) )' % tmp
            '''
            tmp = "place:%s" % json_dictionary["area_place"]
            ret_list.append(tmp)

        return " ".join(ret_list)
