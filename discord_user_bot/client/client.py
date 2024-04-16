import json
import websocket
import asyncio

from .constructs import FetchRequestOpts, SendMessageOpts, CustomStatusOpts, CreateInviteOpts, BotConfigOpts, SendMessage
from ..util.error import DiscordUserBotsError, DiscordAPIError, DiscordUserBotsInternalError

from ..util.enums import ReadyStates
from .events import DiscordEvents

from ..auth.data import ClientData
from ..auth.fetch import Requester

from urllib.parse import quote

class Client:
    def __init__(self, token, config=BotConfigOpts):
        if not isinstance(token, str):
            raise DiscordUserBotsError("Invalid token")
        
        self.config = {**BotConfigOpts}
        self.token = token
        self.message_counter = 0
        self.ready_status_callback = lambda: None
        self.ready_status = ReadyStates.OFFLINE
        self.typing_loop = lambda: None
        self.on = DiscordEvents()
        self.requester = Requester()
        self.client_data = ClientData()
        self.client_data.authorization = self.token
        self.set_config(config)
            
    async def _handle_token_check(self, res):
        if res:
            await self.client_data.gen(self.requester)
            self.create_ws()
        else:
            raise DiscordAPIError(f'Discord rejected token "{self.token}" (Not valid)')
    
    def create_ws(self):
        self.ready_status = ReadyStates.CONNECTING

        ws = websocket.create_connection(self.config['wsurl'], header={
            'Origin': self.requester.url,
            'User-Agent': 'Python'
        })
        
        def on_message(ws, message):
            message = json.loads(message)
            self.message_counter += 1
            self._handle_message(message)
        
        ws.on_message = on_message
        
        def on_close(ws):
            self.on.discord_disconnect()
            if self.config['autoReconnect']:
                self.create_ws()
                self.on.discord_reconnect()
        
        ws.on_close = on_close

    def _handle_message(self, message):
        if message['t'] is None:

            if self.ready_status != ReadyStates.CONNECTED:
                
                if message['d'] is None:
                    raise DiscordAPIError("Discord refused a connection.")
                
                self.heartbeattimer = message['d']['heartbeat_interval']


    async def check_token(self):
        
        res = await self.requester.fetch_request('users/@me', None, self.client_data, 'GET')
        return res['message'] != '401: Unauthorized'

    def set_config(self, config):
        
        self.config.update(config)
        self.requester.api = self.config['api']
        self.requester.url = self.config['url']
        
        if isinstance(self.config['proxy'], str):
            
            self.requester.proxy = self.config['proxy']
    
    async def fetch_request(self, link, options=FetchRequestOpts):
        
        options = {**FetchRequestOpts, **options}
        
        if not isinstance(link, str):
            raise DiscordUserBotsInternalError("Invalid URL")
        
        headers = {}
        
        return await self.requester.fetch_request(
            link,
            options['body'],
            self.client_data,
            options['method'],
            headers
        )
    
    async def fetch_messages(self, limit, channel_id, before_message_id=False):
        
        if limit > 100:
            raise DiscordUserBotsError("Cannot fetch more than 100 messages at a time.")
        
        link = f"channels/{channel_id}/messages?{'before=' + before_message_id + '&' if before_message_id else ''}limit={limit}"
        
        return await self.fetch_request(link, {'method': 'GET', 'body': None})
    
    async def get_guild(self, guild_id):
        
        return await self.fetch_request(f"guilds/{guild_id}", {'method': 'GET', 'body': None})
    
    async def join_guild(self, invite):
        
        invite = self.parse_invite_link(invite)
        return await self.fetch_request(f"invites/{invite}", {'body': {}, 'method': 'POST'})
    
    async def get_invite_info(self, invite):
        
        code = self.parse_invite_link(invite)
        
        return await self.fetch_request(
            f"invites/{code}?inputValue=https%3A%2F%2Fdiscord.gg%2F{code}&with_counts=true&with_expiration=true",
            {'method': 'GET', 'body': None}
        )
    
    async def leave_guild(self, guild_id):
        
        return await self.fetch_request(f"users/@me/guilds/{guild_id}", {'method': 'DELETE', 'body': {'lurking': False}})
    
    async def delete_guild(self, guild_id):
        
        return await self.fetch_request(f"guilds/{guild_id}", {'method': 'DELETE', 'body': None})
    
    async def send(self, text=str, channel_id=int):
        
        data = SendMessage({})
        data.content['content'] = text
        print(f"{data.content}")
        return await self.fetch_request(
            f"channels/{channel_id}/messages",
            {'body': data.content, 'method': 'POST'}
        )
    async def edit(self, message_id, channel_id, content):
        
        return await self.fetch_request(f"channels/{channel_id}/messages/{message_id}", {
            "content": content
        }, "PATCH")

    async def delete_message(self, target_message_id, channel_id):
        
        return await self.fetch_request(f"channels/{channel_id}/messages/{target_message_id}", None, "DELETE")
    
    async def call_check(self, args):
        
        if self.ready_status == ReadyStates.CONNECTING:

            await asyncio.Future()  

            self.ready_status_callback = None

        if self.ready_status != ReadyStates.CONNECTED:
            raise DiscordUserBotsError(f"Client is in a {ReadyStates.get_v(self.ready_status)} state")

        for arg in args:
            if not arg:
                raise DiscordUserBotsError(f"Invalid parameter \"{arg}\"")
    async def type(self, channel_id):
        
        async def typing_task():
            while True:
                await self.fetch_request(f"channels/{channel_id}/typing", None, "POST")
                await asyncio.sleep(self.config["typinginterval"])

        self.typingLoop = asyncio.create_task(typing_task())

        return await self.fetch_request(f"channels/{channel_id}/typing", None, "POST")

    async def stop_type(self):
        
        if self.typingLoop:
            self.typingLoop.cancel()
        
        return True
    async def group(self, recipients):
        
        return await self.fetch_request("users/@me/channels", {
            "recipients": recipients
        }, "POST")

    async def leave_group(self, group_id):
        
        return await self.fetch_request(f"channels/{group_id}", None, "DELETE")

    async def remove_person_from_group(self, person_id, channel_id):
        
        return await self.fetch_request(f"channels/{channel_id}/recipients/{person_id}", None, "DELETE")

    async def rename_group(self, name, group_id):
        
        return await self.fetch_request(f"channels/{group_id}", {
            "name": name
        }, "PATCH")

    async def create_server(self, name, guild_template_code="2TffvPucqHkN", icon=None):
        
        return await self.fetch_request(f"guilds/templates/{guild_template_code}", {
            "name": name,
            "icon": icon,
            "guild_template_code": guild_template_code
        }, "POST")

    async def create_thread_from_message(self, message_id, channel_id, name, auto_archive_duration=1440):
        
        return await self.fetch_request(f"channels/{channel_id}/messages/{message_id}/threads", {
            "name": name,
            "type": 11,
            "auto_archive_duration": auto_archive_duration,
            "location": "Message"
        }, "POST")

    async def create_thread(self, channel_id, name, auto_archive_duration=1440):
        
        return await self.fetch_request(f"channels/{channel_id}/threads", {
            "name": name,
            "type": 11,
            "auto_archive_duration": auto_archive_duration,
            "location": "Thread Browser Toolbar"
        }, "POST")

    async def delete_thread(self, thread_id):
        
        return await self.fetch_request(f"channels/{thread_id}", None, "DELETE")

    async def join_thread(self, thread_id):
        
        return await self.fetch_request(f"/channels/{thread_id}/thread-members/@me", None, "PUT")

    async def add_reaction(self, message_id, channel_id, emoji):
        
        return await self.fetch_request(
            f"channels/{channel_id}/messages/{message_id}/reactions/{quote(emoji)}/@me",
            {'method': 'PUT'}
        )

    async def remove_reaction(self, message_id, channel_id, emoji):
        
        return await self.fetch_request(f"channels/{channel_id}/messages/{message_id}/reactions/{quote(emoji)}/@me", None, "DELETE")

    async def change_status(self, status):
        
        if status not in ["online", "idle", "dnd", "invisible"]:
            raise ValueError("Status must be 'online', 'idle', 'dnd', or 'invisible'")
        return await self.fetch_request("users/@me/settings", {
            "status": status
        }, "PATCH")

    async def set_custom_status(self, custom_status):
        
        return await self.fetch_request("users/@me/settings", {
            "custom_status": custom_status
        }, "PATCH")

    async def create_invite(self, channel_id, inviteOpts={}):
        
        opts = {
            "createInviteOpts": {},
            **inviteOpts
        }
        return await self.fetch_request(f"/channels/{channel_id}/invites", opts, "POST")

    async def accept_friend_request(self, user_id):
        
        return await self.fetch_request(f"/users/@me/relationships/{user_id}", None, "PUT")