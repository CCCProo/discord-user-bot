class DiscordEvents:

    def __init__(self):
        self.readys = False
        
    async def ready(self, func):
        if self.readys:
            func()
            self.readys = False
