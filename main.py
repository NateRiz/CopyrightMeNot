from authenticate import User
from recover import *


def list_results(results):
    [print(F"{i}. {u}") for i, u in enumerate(sorted(results.keys()))]


def get_result(results):
    selected = input()
    if not (selected.isdigit() and 0 <= int(selected) <= (len(results) - 1)):
        return -1
    return results[sorted(results.keys())[int(selected)]]


def copy(client):
    user = ""
    while not user:
        user = input("Username of playlist's owner:")

    found_users = get_matching_users(client, user)
    if not found_users: return
    print("Please select the number of the correct username. (Or anything else to quit")
    list_results(found_users)
    user_id = get_result(found_users)
    if user_id == -1:
        return

    found_playlists = get_user_playlists(client, user_id)
    list_results(found_playlists)
    playlist_id = get_result(found_playlists)
    if playlist_id == -1:
        return

    copy_playlist(client, playlist_id)

def recover():
    pass


def parse():
    command = ""
    while command not in ["c", "r"]:
        try:
            command = input(usage).lower()[0]
        except Exception:
            command = ""

    return "c"


def main():
    """
    HALTED - Youtube API does not currently send deleted video's Ids through api when
    listing videos in a playlist
    :return:
    """
    client = User()
    client.authenticate()
    if parse() == "c":
        copy(client.user)
    else:
        recover()


usage = \
"""
Usage:

{:<16} {}
{:<16} {}
""".format("(c) Copy", "Copy playlist from a user to your account.",
       "(r) Recover", "Attempt to restore missing videos in a playlist.")

if __name__ == '__main__':
    main()
