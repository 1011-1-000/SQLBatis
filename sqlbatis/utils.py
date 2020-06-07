import re


def camel_to_snake_case(name, exclude_key_words=['']):
    """tanslate the name to the snake case according to the named conventions
    1. split the class name with the capital letter
    2. remove all the spaces and join the elements in the array with '_' sign, and lower the string you get

    :param name: the camel case name
    :type name: str
    :return: snake case name
    :rtype: str
    """

    name_array = re.split('([A-Z][a-z0-9]*)', name)

    # remove all the space
    table_name_array = [
        name for name in name_array if name not in exclude_key_words]
    snake_case_name = '_'.join(table_name_array).lower()
    return snake_case_name
