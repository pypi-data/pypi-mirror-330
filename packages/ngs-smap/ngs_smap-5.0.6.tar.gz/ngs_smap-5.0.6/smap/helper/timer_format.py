def convert_to_preferred_format(sec):
    """
    This function converts the measured runtime to a human readable format
    in hours, minutes, seconds

    Args:
        sec (int): the elapsed time in seconds

    Returns:
        string: strig the the execution runtime
    """
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60

    return "%02d:%02d:%02d" % (hour, min, sec)
