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
