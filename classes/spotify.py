import base64
import time

import requests
import json


def check_status_codes(status_code):
    if status_code == 400:
        raise Exception("Bad Request - The request could not be understood by the server due to malformed syntax.")
    if status_code == 401:
        raise Exception("Unauthorized - The request requires user authentication or, if the request included authorization credentials, authorization has been refused for those credentials.")
    if status_code == 403:
        raise Exception("Forbidden - The server understood the request, but is refusing to fulfill it.")
    if status_code == 404:
        raise Exception("Not Found - The requested resource could not be found. This error can be due to a temporary or permanent condition.")
    if status_code == 503:
        raise Exception("Service Unavailable - The server is currently unable to handle the request due to a temporary condition which will be alleviated after some delay. You can choose to resend the request again.")


def get_access_token(client_id, client_secret):
    authorization = base64.b64encode(bytes(client_id + ":" + client_secret, "ISO-8859-1")).decode("ascii")

    headers = {
        "Authorization": f"Basic {authorization}",
    }

    body = {
        "grant_type": "client_credentials"
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=body)

    check_status_codes(response.status_code)
    if response.status_code == 429:
        # when getting rate limited
        time.sleep(1)
        get_access_token(client_id, client_secret)

    return json.loads(response.text)['access_token']


def post_api_request(access_token, api_path):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(f'http://api.spotify.com/v1/{api_path}', headers=headers)

    check_status_codes(response.status_code)
    if response.status_code == 429:
        # when getting rate limited
        time.sleep(1)
        post_api_request(access_token, api_path)

    return response


def get_playlist(access_token, playlist):
    response = post_api_request(access_token, f'playlists/{playlist}')
    return json.loads(response.content)


def get_album(access_token, album):
    response = post_api_request(access_token, f'albums/{album}')
    return json.loads(response.content)


def get_track(access_token, track):
    response = post_api_request(access_token, f'tracks/{track}')
    return json.loads(response.content)


def get_artist(access_token, artist):
    response = post_api_request(access_token, f'artists/{artist}')
    return json.loads(response.content)


def get_artist_albums(access_token, artist):
    response = post_api_request(access_token, f'artists/{artist}/albums')
    return json.loads(response.content)
