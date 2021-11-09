from discord import Client, Message
from logging import Logger

class DiscordRunner():
    """
        DiscordRunner that listens to events
        
        Wraps Discord API for personal use

        token: str, individual security token to log into discord
        client: Client, handler to log into discord and manage events
        logger: Logger, to manage a clean output 
    """
    token: str
    client: Client
    logger: Logger

    def __init__(self, token: str,
                 logger: Logger) -> None:
        self.token = token
        self.logger = logger
        self.client = Client()

    def boot(self):
        """
            Boots up the client
        """
        self.logger.info("Booting up discord client...")
        self.client.run(self.token)
        self.logger.info("Successfully booted up discord client" +
                         f" as user {self.client.user()}")   

    @client.event
    async def on_message(self, message: Message) -> int:
        """
            Reacts to a message and delegates to the correct coroutine
        """
        try:
            # Bot is not going to react to itself
            if message.author() == self.client.user():
                return 0

            if message.content.startswith("Hello"):
                await message.channel.send("World!")

        except Exception as exc:
            self.logger.critical(exc)
            await message.channel.send("Oops, an Error occurred...")
            return -1
