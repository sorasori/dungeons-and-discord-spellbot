import discordrunner
from yaml import load, YAMLError
import logging

# TODO: Add argparse to parse token from CLI

def main() -> None:
    # TODO: change credentials path to variable path, add default
    credentials_path = "discord.credentials"
    logger = logging.Logger()
    try:
        # Read out credentials file
        with open(credentials_path, "r") as f:
            credentials_dict = load(f)
            try:
                # read out token
                api_token = credentials_dict["token"]
                # create runner
                runner = discordrunner.DiscordRunner(logger, api_token)
                # boot
                runner.boot()
            except Exception as exc:
                logger.critical("Something went wrong in initializing the discordrunner:" 
                                f" {exc}")
    except YAMLError as exc:
        logger.debug(exc)