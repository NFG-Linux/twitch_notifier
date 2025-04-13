import requests, json, time, os
from datetime import datetime, timedelta

CONFIG_FILE = 'config.json'
STATE_FILE = 'state.json'

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"was_live": False, "last_token": "", "token_expiry": 0}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def get_oauth_token(config, state):
    now = time.time()
    if state['last_token'] and now < state['token_expiry']:
        return state['last_token']

    print("Fetching new OAuth token...")
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': config['twitch_client_id'],
        'client_secret': config['twitch_client_secret'],
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params).json()
    token = response['access_token']
    expires_in = response['expires_in']

    state['last_token'] = token
    state['token_expiry'] = now + expires_in - 60
    save_state(state)
    return token

def get_user_id(token, config):
    headers = {
        'Client-ID': config['twitch_client_id'],
        'Authorization': f'Bearer {token}'
    }
    url = f"https://api.twitch.tv/helix/users?login={config['twitch_username']}"
    response = requests.get(url, headers=headers).json()
    return response['data'][0]['id']

def is_live(token, user_id, config):
    headers = {
        'Client-ID': config['twitch_client_id'],
        'Authorization': f'Bearer {token}'
    }
    url = f"https://api.twitch.tv/helix/streams?user_id={user_id}"
    response = requests.get(url, headers=headers).json()
    return len(response['data']) > 0

def notify_discord(webhooks, username):
    for url in webhooks:
        data = {
            'content': f'{username} is now LIVE on Twitch! Check it out: https://twitch.tv/{username}'
        }
        requests.post(url, json=data)

def main():
    config = load_config()
    state = load_state()
    token = get_oauth_token(config, state)
    user_id = get_user_id(token, config)
    currently_live = is_live(token, user_id, config)

    if currently_live and not state['was_live']:
        print("Going live! Sending notifications...")
        notify_discord(config['discord_webhooks'], config['twitch_username'])

    state['was_live'] = currently_live
    save_state(state)

if __name__ == '__main__':
    main()
