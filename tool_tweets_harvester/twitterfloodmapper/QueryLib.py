
class QueryLib:

    @staticmethod
    def convert_json_to_powertrack(json_dictionary:dict) -> str or None:
        """
        Converts the easy-to-read json object into a string in powertrack format
        :param json_dictionary:
        :return: String if possible to build PowerTrack tag. None otherwise.
        """

        if not QueryLib._pass_consistency_check(json_dictionary):
            print("Unable to convert Json dictionary to PowerTrack query.")
            return None

        ret_list = []

        # include each key found
        if "keywords_in" in json_dictionary.keys():
            ret_list.append(QueryLib._translate_keywords_in(json_dictionary["keywords_in"]))
        if "keywords_out" in json_dictionary.keys():
            ret_list.append(QueryLib._translate_keywords_out(json_dictionary["keywords_out"]))
        if "area_place" in json_dictionary.keys():
            ret_list.append(QueryLib._translate_area_place(json_dictionary["area_place"]))
        if "area_country" in json_dictionary.keys():
            ret_list.append(QueryLib._translate_area_country(json_dictionary["area_country"]))
        # TODO - set up other rules

        # merge all together
        return " ".join(ret_list)

    # ################################################ Internal ################################################ #

    @staticmethod
    def _pass_consistency_check(jd:dict) -> bool:
        """
        Just checks if
        :param jd: Json dictionary
        :return: TRUE if input is consistent, FALSE otherwise
        """
        all_keys = jd.keys()
        areas = [k for k in all_keys if k.startswith("area_")]
        if len(areas) > 1:
            print("INVALID: Self-excluding keys: {0}".format(areas))
            return False
        return True

    @staticmethod
    def _translate_keywords_in(ki) -> str:
        tmp = ") OR (".join(ki)
        return "( (%s) )" % tmp

    @staticmethod
    def _translate_keywords_out(ko) -> str:
        return "-%s" % QueryLib._translate_keywords_in(ko)

    @staticmethod
    def _translate_area_place(ap) -> str:
        if not isinstance(ap, str):
            print("WARNING: Argument area_place should me string. Got %s." % type(ap))
            return ""
        return 'place:"%s"' % ap

    @staticmethod
    def _translate_area_country(ac):
        if not isinstance(ac, str):
            print("WARNING: Argument area_country should me string. Got %s." % type(ac))
            return ""
        return 'place_country:"%s"' % ac

