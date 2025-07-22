PituBot is a multifunctional bot, it has many useless functions you can try.
This bot is not meant to be integrated anywhere. It is open source just for me to document my learning journey on Python.
If you desire to import it, to make use of it you would need to create the following environment variables:
**DISCORD_TOKEN**: *this is where your bot token goes*. Needed to run the bot.
**OPENROUTER_API_KEY**: *this is where your Openrouter API key goes*. Needed to run mistralai_chat.
**SQL_PASSWORD**: *this is where your SQL password goes*. Needed to run sm command.
**MAL_CLIENT_ID**: *this is where your MyAnimeList client ID goes*. Needed to run mal.


This bot, as of now, 22nd of July 2025, has three functions
- **MudaePitu**: A cheap mudae, made to learn SQL integration and discord embeds, it has an owner system, but you can steal the card even if it has an owner. "sm" to drop.
- **MistralaiChat**: you can chat with Mistralai AI on a discord chat.  Commands are "startchat" and "endchat". If response exceeds discord character limit it will send the response as a .txt instead.
- **mal**: with "anime {arg}" you can get info from myanimelist.net for the anime you specified in the {arg}. It uses MAL APIs.
