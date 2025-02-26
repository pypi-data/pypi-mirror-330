# ValhallaBot
```
What This
ValhallaBot is a Telegram bot designed to send emails with customizable settings. It allows users to add recipient and sender emails, set email subjects and messages, and control the sending interval.
```

## Installation

You can install ValhallaBot using pip:

```bash
pip install valhallabot
```

Usage
```
After installing the package, you can use the bot by creating an instance of ValhallaBot and running it. Here's an example:
```

```
#code
from valhallabott import ValhallaBot
bot = ValhallaBot(bot_token="YOUR_BOT_TOKEN", admin_id=YOUR_ADMIN_ID)
bot.run()
```
```valhalla
Parameters:
bot_token: Your Telegram bot token.

admin_id: Your Telegram user ID (to identify the admin).

Make sure to replace "YOUR_BOT_TOKEN" and YOUR_ADMIN_ID with your actual bot token and admin ID.
```