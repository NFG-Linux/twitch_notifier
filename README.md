# twitch_notifier
windows daemon to notify discord channels when you go live

NOT INCLUDED FILES:

-state.json
auto created and stores live state (don't manually create this file)

-config.json
should have the below syntax:

{
  "twitch_client_id": "your_twitch_client_id",
  "twitch_client_secret": "your_twitch_client_secret",
  "twitch_username": "your_username",
  "discord_webhooks": [
    "https://discord.com/api/webhooks/xxx/yyy",
    "https://discord.com/api/webhooks/aaa/bbb"
  ]
}
