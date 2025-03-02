VintageStory MasterServer
=========================

A homemade reproduction of the VintageStory Master Server as a Django app, making the server list available to the rest of your project. 

**_What is a "master server"?_** It's what allows the server browser to work. Essentially a catalogue that game servers register with so players can find out them.

_**Why?**_ Besides haunting some individuals on the VS Discord server? Because I can. Personally, I use this to show a marker on my personal website for when my game server is online.

***Why not Python 3.xyz?*** More than likely this will work on your Python version, I've just not tested it. Please tell me if it works for you! 

## Installation

```shell
pip install vintagestory-masterserver
```

Add to your installed apps in `project/settings.py`:

```py
INSTALLED_APPS = [
    ...,
    'vintagestory_masterserver',
]
```
Modify `project/urls.py` to add the urls: 

```py
urlpatterns = [
    ...,
    path("vsmaster/", include("vsmaster.urls"))
]
```
Obviously you can change `"vsmaster/"` to your preferred choice, but be aware this readme will use this in all examples.

Please remember to then run `python manage.py makemigrations` and `migrate`. 

## Usage

Verify it is working:
```shell
curl http://127.0.0.1:8000/vsmaster/list
```
example output:
```json
{"status": "ok", "data": [{"serverName": "VintageStory Server", "serverIP": "127.0.0.1:42420", "playstyle": {"id": "surviveandbuild", "langCode": "surviveandbuild-bands"}, "Mods": [{"id": "game", "version": "1.20.3"}, {"id": "betterruins", "version": "0.4.6"}], "maxPlayers": 16, "gameVersion": "1.20.3", "hasPassword": true, "whitelisted": true, "gameDescription": "A Vintage Story Server"}]}
```

Get a list of all servers with heartbeats within the last 6 minutes:
```python
 servers = VSServer.objects.filter(last_heartbeat__gte=timezone.now()-timezone.timedelta(minutes=6))
```

### Modifying game server config

In `serverconfig.json`, modify the `MasterserverUrl` line to point to your base url.

e.g. `"MasterserverUrl": "http://127.0.0.1:8000/vsmaster/"`.

The location of the config file will depend on your operating system and the particulars of your set up, but if you're reading this I sure hope you've figured that out already. 

### Modifying game client config

There is no in-game UI to change this so you'll need to locate your settings file. 

On Windows, this defaults to `%APPDATA%\VintageStoryData\clientsettings.json`.

Change the `masterserverUrl` line to direct to your own root url, e.g.: `"masterserverUrl": "http://127.0.0.1:8000/vsmaster/"`

## Background

This API attempts to replicate everything I could observe the game server and client querying, and the sort of responses I could get from the official master server.  

I should say I had some light assistance from a couple of people in the official VintageStory Discord guild whilst figuring this out.

## Contributing

While I've tried to imagine the sorts of odd situations that could cause errors, and test/correct them I will surely have missed something, in which case please do raise an issue or pull request!

Also if you have any idea how to write proper tests, that would be grand. 

Thank you.