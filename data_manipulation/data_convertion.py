def pipe_to_tab_delimited(csv_str):
    """
    Converts a pipe-delimited string to a tab-delimited string.

    Parameters:
    csv_str (str): A string containing CSV data with pipe '|' as the delimiter.

    Returns:
    str: A string with the data converted to tab '\t' delimited format.
    """
    return csv_str.replace("|", "\t")


def tab_to_pipe_delimited(tab_str):
    """
    Converts a tab-delimited string to a pipe-delimited string.

    Parameters:
    tab_str (str): A string containing data with tab '\t' as the delimiter.

    Returns:
    str: A string with the data converted to pipe '|' delimited format.
    """
    return tab_str.replace("\t", "|")
