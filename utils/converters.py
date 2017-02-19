import base64


def hex_to_base64(hex_value):
    """
    :param hex_value: string representing hexadecimal value
    :return: string representing base62 encoding of decoded hex_value
    """
    return base64.b64encode(base64.b16decode(hex_value, casefold=True), altchars=b'-_')

