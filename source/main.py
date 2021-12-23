import discordrunner
from yaml import load, YAMLError
import logging
import argparse

# TODO: threading?...

def main() -> None:
    # Parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--credentials", default="discord.credentials", help="Path to credentials file")
    parser.add_argument("--debug", action="store_true", help="If true will log detailed messages on terminal")
    args = parser.parse_args()
    
    # Init path to credentials
    credentials_path = args.credentials

    # Init logger
    logger = logging.getLogger(__name__)
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    console_log_handler = logging.StreamHandler()
    console_log_handler.setLevel(logging.DEBUG)
    console_log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s ')
    console_log_handler.setFormatter(console_log_formatter)
    logger.addHandler(console_log_handler)

    logger.info("A")
    print("b")

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