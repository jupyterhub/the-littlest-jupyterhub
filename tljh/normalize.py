"""
Functions to normalize various inputs
"""
import hashlib


def generate_system_username(username):
    """
    Generate a posix username from given username.

    If username < 26 char, we just return it.
    Else, we hash the username, truncate username at
    26 char, append a '-' and first add 5char of hash.
    This makes sure our usernames are always under 32char.
    """

    if len(username) < 26:
        return username

    userhash = hashlib.sha256(username.encode("utf-8")).hexdigest()
    return "{username_trunc}-{hash}".format(
        username_trunc=username[:26], hash=userhash[:5]
    )
