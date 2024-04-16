import os
import json
from typing import Dict, Any, List, Union
from pathlib import Path

class MentionsLimiter:
    """
    Mentions object when dealing with messages
    """
    def __init__(self, opts: Dict[str, bool]) -> None:
        self.parse = []
        self.replied_user = opts.get('allowRepliedUser', True)

        if opts.get('allowUsers', True):
            self.parse.append("users")
        if opts.get('allowRoles', True):
            self.parse.append("roles")
        if opts.get('allowEveryone', True):
            self.parse.append("everyone")

class CustomStatus:

    def __init__(self, opts: Dict[str, Any]) -> None:
        self.contents = {
            'expires_at': opts.get('expireAt'),
            'text': opts.get('text'),
            'emoji_name': opts.get('emoji')
        }

        self.contents = {k: v for k, v in self.contents.items() if v is not None}

        if not self.contents:
            self.contents = None

class SendMessage:
    """
    Message send class for sending messages
    """
    def __init__(self, opts: Dict[str, Any]) -> None:
        attachments = []

        if isinstance(opts.get('attachments'), list) and opts['attachments']:
            is_multipart_form_data = True

            for index, item in enumerate(opts['attachments']):
                if not item:
                    continue

                if isinstance(item, str):
                    item = {'path': item}

                if isinstance(item, dict) and item.get('path'):
                    filename = item.get('name') or os.path.basename(item['path']) or f"file-{index}"
                    with open(item['path'], 'rb') as f:
                        attachments.append({
                            'id': index,
                            'filename': filename,
                            'description': item.get('description') or filename
                        })

            opts['attachments'] = attachments

        content = {
            'content': opts.get('content', ""),
            'tts': opts.get('tts', False),
            'embeds': opts.get('embeds', []),
            'allowed_mentions': MentionsLimiter(opts.get('allowed_mentions', {})),
            'message_reference': {'message_id': opts['reply']} if opts.get('reply') is not None else None,
            'components': None,
            'sticker_ids': opts.get('stickers', []),
            **({'attachments': attachments} if attachments else {})
        }

        if 'attachments' in content:
            del content['attachments']

        if attachments and is_multipart_form_data:
            payload_json = json.dumps(content)
            self.content = {'payload_json': payload_json, **{f'file{attach["id"]}': attach['filename'] for attach in attachments}}
        else:
            self.content = content

class BotConfig:
    """
    Bot configuration class
    """
    def __init__(self, api: str = "v9", wsurl: str = "wss://gateway.discord.gg/?encoding=json&v=9",
                 url: str = "https://discord.com", typinginterval: int = 1000, proxy: Union[str, None] = None,
                 auto_reconnect: bool = True) -> None:
        self.api = api
        self.wsurl = wsurl
        self.url = url
        self.typinginterval = typinginterval
        self.proxy = proxy
        self.auto_reconnect = auto_reconnect

FetchRequestOpts: Dict[str, Any] = {
    'method': "GET",
    'body': None,
}

CreateInviteOpts: Dict[str, Union[str, int, bool, None]] = {
    'validate': None,
    'max_age': 0,
    'max_uses': 0,
    'target_user_id': None,
    'target_type': None,
    'temporary': False,
}

BotConfigOpts: Dict[str, Any] = {
    'api': "v9",
    'wsurl': "wss://gateway.discord.gg/?encoding=json&v=9",
    'url': "https://discord.com",
    'typinginterval': 1000,
    'proxy': None,
    'autoReconnect': True,
}

MentionsLimiterOpts: Dict[str, bool] = {
    'allowUsers': True,
    'allowRoles': True,
    'allowEveryone': True,
    'allowRepliedUser': True,
}

CustomStatusOpts: Dict[str, Any] = {
    'text': None,
    'emoji': None,
    'expireAt': None,
}

SendMessageOpts: Dict[str, Any] = {
    'content': "",
    'reply': None,
    'tts': False,
    'embeds': [],
    'allowed_mentions': MentionsLimiterOpts,
    'components': None,
    'stickers': [],
    'attachments': [],
}
