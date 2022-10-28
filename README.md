# Safe bot

This is silly discord bot, that doesn't allow to read/write in a channel for anyone except one typing person, paroding rust borrow rules.

## Usage
Bash:
```sh
git clone https://github.com/farkon00/safe-bot
cd safe-bot

export SAFE_BOT_TOKEN="<TOKEN>"
pip install -r requirements.txt
python3 bot.py
```
Powershell:  
```powershell
git clone https://github.com/farkon00/safe-bot
cd safe-bot

$Env:SAFE_BOT_TOKEN = '<TOKEN>'
pip install -r requirements.txt
python bot.py
```