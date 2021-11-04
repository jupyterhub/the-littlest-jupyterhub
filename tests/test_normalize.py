"""
Test functions for normalizing various kinds of values
"""
from tljh.normalize import generate_system_username


def test_generate_username():
    """
    Test generating system usernames from hub usernames
    """
    usernames = {
        # Very short
        "jupyter-test": "jupyter-test",
        # Very long
        "jupyter-aelie9sohjeequ9iemeipuimuoshahz4aitugiuteeg4ohioh5yuiha6aei7te5z": "jupyter-aelie9sohjeequ9iem-4b726",
        # 26 characters, just below our cutoff for hashing
        "jupyter-abcdefghijklmnopq": "jupyter-abcdefghijklmnopq",
        # 27 characters, just above our cutoff for hashing
        "jupyter-abcdefghijklmnopqr": "jupyter-abcdefghijklmnopqr-e375e",
    }
    for hub_user, system_user in usernames.items():
        assert generate_system_username(hub_user) == system_user
        assert len(system_user) <= 32
