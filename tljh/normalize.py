"""
Functions to normalize various inputs
"""
import hashlib
import re

def generate_system_username(username):
    """
    Generate a posix username from given username.

    If username < 26 char and looks like a legal linux username*, 
    we just return it.
    Else, we take the first 26 chars of the username minus any 
    illegal characters, append a '-' and the first 5 chars of 
    the hash of the username.
    This makes sure our usernames are always under 32char and
    are legal unix usernames.

    * using the debian/ubuntu iusername username spec, which
    seems like the most restrictive one
    """

    legal_username = re.sub("[^a-z0-9_-]", "", username.lower())
    if legal_username == username and len(username) < 26:
        return username

    userhash = hashlib.sha256(username.encode("utf-8")).hexdigest()
    return "{username_trunc}-{hash}".format(
        username_trunc=legal_username[:26], hash=userhash[:5]
    )
