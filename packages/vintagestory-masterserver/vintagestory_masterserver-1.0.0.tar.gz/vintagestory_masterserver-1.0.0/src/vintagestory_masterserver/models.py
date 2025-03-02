import base64
import secrets
from typing import TypedDict, List
from django.db import models




class VSplaystyleData(TypedDict):
    id: str
    langCode: str


class VSmodData(TypedDict):
    id: str
    version: str

class VSServerData(TypedDict):
    port: int
    name: str
    icon: str
    playstyle: VSplaystyleData
    maxPlayers: int
    gameVersion: str
    hasPassword: bool
    Mods: List[VSmodData]
    serverUrl: str | None
    gameDescription: str
    whitelisted: bool


class VSServerManager(models.Manager):
    def create_server(self, data: VSServerData, ip_addr: str):
        server = self.create(
            vs_server_name = data['name'],
            address = ip_addr,
            port=data['port'],
            play_style_id=data['playstyle']['id'],
            play_style_lang_code=data['playstyle']['langCode'],
            is_whitelisted=data['whitelisted'],
            description=data['gameDescription'],
            max_players=data['maxPlayers'],
            game_version=data['gameVersion'],
            has_password=data['hasPassword'],
            server_url=data['serverUrl'],
            token=base64.b64encode(secrets.token_bytes(32)).decode('utf-8')
        )
        server.save()
        mods = [VSMod(_id=mod['id'], version=mod["version"], server=server) for mod in data['Mods']]
        for mod in mods: mod.save()
        return server



class VSServer(models.Model):
    objects = VSServerManager()

    vs_server_name = models.CharField(max_length=512)
    address = models.CharField(max_length=256)  # IP, URL probably acceptable so 256
    port = models.PositiveIntegerField()

    play_style_id = models.CharField(max_length=64)
    play_style_lang_code = models.CharField(max_length=64)
    is_whitelisted = models.BooleanField()
    description = models.TextField()
    max_players = models.SmallIntegerField()
    game_version = models.CharField(max_length=64)
    has_password = models.BooleanField()
    server_url = models.CharField(max_length=256, null=True)
    last_heartbeat = models.DateTimeField(auto_now_add=True)
    players = models.SmallIntegerField(default=0)

    token = models.CharField(max_length=64)


    def as_dict(self):
        return {
            "serverName": self.vs_server_name,
            "serverIP": f"{self.address}:{self.port}",
            "playstyle": {
                "id": self.play_style_id,
                "langCode": self.play_style_lang_code
            },
            "Mods": [{"id": mod._id, "version": mod.version} for mod in self.mods.all()],
            "maxPlayers": self.max_players,
            "gameVersion": self.game_version,
            "hasPassword": self.has_password,
            "whitelisted": self.is_whitelisted,
            "gameDescription": self.description,
        }

    def __repr__(self):
        return f"{self.vs_server_name}@{self.address}"

    def __str__(self):
        return f"{self.vs_server_name}@{self.address}"

# class VSModManager(models.Manager):
#     def create_mod(self, data: VSmodData):
#


class VSMod(models.Model):
    _id = models.CharField(max_length=64)
    version = models.CharField(max_length=64)
    server = models.ForeignKey(VSServer, on_delete=models.CASCADE, related_name='mods')

    def __str__(self):
        return f"{self._id} v{self.version}"

