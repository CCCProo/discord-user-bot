from discord_user_bot import Client

import asyncio


async def main():
    client = Client(
        "OTM3MDI4NTI5MTMwOTk1Nzgz.Gfk4tG.Z6NoJKnibTlb9hKWJUF0PuRkzDoNxwXWyP1n-Q",
        {
            "api": "v9",
            "wsurl": "wss://gateway.discord.gg/?encoding=json&v=9",
            "os": "linux",
            "bd": "holy",
            "language": "en-US",
            "typinginterval": 1000,
            "proxy": None,
            "autoReconnect": True,
        }
    )    

    def mains():
        print('go')

    await client.on.ready(mains())

if __name__ == "__main__":
    asyncio.run(main())
