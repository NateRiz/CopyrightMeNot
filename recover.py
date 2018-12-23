from time import sleep


def get_matching_users(client, user):
    response = client.search().list(
        part="snippet",
        q=user,
        maxResults=10,
        type="channel"
    ).execute()
    found_users = {}
    for i in response["items"]:
        found_users[i["snippet"]["channelTitle"]] = i["id"]["channelId"]

    if not found_users:
        print(F"Could not find {user}. Please double check the spelling and try again.")

    return found_users


def get_user_playlists(client, user_id):
    response = client.playlists().list(
        part='snippet,contentDetails',
        channelId=user_id
    ).execute()
    playlists = {}
    for p in response["items"]:
        playlists[p["snippet"]["title"]] = p["id"]

    if not playlists:
        print(F"Could not find any playlists for the given user.")

    return playlists


def get_video_ids(client, playlist_id):
    response = client.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    ).execute()
    videos = []

    for v in response["items"]:
        videos.append(v["snippet"]["resourceId"]["videoId"])

    while "nextPageToken" in response:
        response = client.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=response["nextPageToken"]
        ).execute()
        for v in response["items"]:
            videos.append(v["snippet"]["resourceId"]["videoId"])

    return videos


def create_playlist(client, title):
    body = {"snippet": {
        "title": title
    },
        "status": {
            "privacyStatus": "private"
        }}
    response = client.playlists().insert(
        body=body,
        part="snippet,status"
    ).execute()
    print(F"Created new private playlist: {response['snippet']['title']}")
    print(response["id"])
    return response["id"]


def add_video_to_new_playlist(client, video_id, playlist_id):
    try:
        resource={'snippet': {'playlistId': playlist_id, 'resourceId': {'kind': 'youtube#video', 'videoId': video_id}}}

        response = client.playlistItems().insert(
            body=resource,
            part="snippet"
        ).execute()
    except Exception as e:
        print(F"Couldn't add video: {video_id}.\n{e}")

def copy_playlist(client, playlist_id):
    videos = get_video_ids(client, playlist_id)
    new_playlist_id = create_playlist(client, F"{playlist_id}-Copy")
    for i, v in enumerate(videos):
        print(F"Adding {v}. ({i} / {len(videos)})")
        add_video_to_new_playlist(client, v, new_playlist_id)
        sleep(.3)