def which_ele_is_in_str(list, string):
    """
    Returns the first element from list that is in string.
    """
    return next((x for x in list if x in string), None)


def lists_both_have_ele_in_str(list1, list2, string):
    """
    Returns if string is in both list1 and list2.
    """
    return which_ele_is_in_str(list1, string) and which_ele_is_in_str(list2, string)


def remove_TBAs_and_dups(competitor_name_elements_with_TBAs_and_dups):
    """
    Removes entries that start with TBA (case-sensitive) and duplicate names.

    competitor_name_elements_with_TBAs_and_dups : list of beautiful soup elements
    """
    competitor_names = []
    competitor_name_elements = []
    for ele in competitor_name_elements_with_TBAs_and_dups:
        if ele.text[:3] != "TBA" and ele.text not in competitor_names:
            competitor_name_elements.append(ele)
            competitor_names.append(ele.text)
    return competitor_name_elements
