def get_tag(hilo_object):
    hi = hilo_object["High"]
    lo = hilo_object["Low"]
    tagCharacters = '0289PYLQGRJCUV'
    id = (lo << 8) + hi
    tag = ""
    while id > 0:
        i = id % 14
        tag = tagCharacters[i] + tag
        id //= 14
    return tag


def get_hilo():
    ""