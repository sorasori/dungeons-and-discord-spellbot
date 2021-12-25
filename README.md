# dungeons-and-discord-spellbot
Discord chatbot to scrape off spell information from dndbeyond and do other tasks such as roll damage and get combat turns.

# Install and run
Old project code (first revision) is working but needs heavy refactoring e.g a container or shell script to set dependencies, intermediate logging, support for a credentials file and overall cleanup.
To use it:
  1. Make sure, discord and BeautifulSoup package are installed on your machine. (Otherwise enter `pip install discord` and `pip install beautifulsoup4`)
  2. Assuming you already made a discordbot once, retrieve its token.
  3. Save its token in source/old/main_bot.py as a string under the variable name discord_token. `discord_token = "[YOUR TOKEN HERE]"
  4. Run main_bot.py in a terminal/as an executable, no CLI Arguments needed.
  5. Test your bot by chatting it up on discord with a message such as "roll 3d8" or "spell moonbeam"

### Important
Revision is a work in progress.
