import os
import re
from flask import request
from pathlib import Path

# Load bot substrings from a file or environment variable
def load_known_bots(file_path='bots.txt'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            bots = {line.strip().lower() for line in f if line.strip()}
        return bots
    else:
        # Fallback to default set if file not found
        return {
            "bot", "crawl", "slurp", "spider", "curl", "wget", "python-requests",
            "httpclient", "phpcrawl", "bingbot", "yandex", "facebookexternalhit",
            "mediapartners-google", "adsbot-google", "duckduckbot", "baiduspider",
            "sogou", "exabot", "facebot", "ia_archiver", "linkedinbot", "twitterbot",
            "applebot", "rogerbot", "petalbot", "ahrefsbot", "semrushbot",
            "mj12bot", "dotbot", "gigabot", "openbot", "netcraftsurveyagent"
        }

# Load known bots at startup
KNOWN_BOTS = load_known_bots()

# Precompile a regular expression pattern for known bots for efficiency
BOT_REGEX = re.compile(
    r'(' + '|'.join(re.escape(bot) for bot in KNOWN_BOTS) + r')',
    re.IGNORECASE
)

# Headers that are considered necessary for non-bot requests
NECESSARY_HEADERS = {"accept"}

def is_bot():
    """
    Determines whether the incoming request is likely from a bot.

    Returns:
        bool: True if the request is from a bot, False otherwise.
    """
    user_agent = request.headers.get('User-Agent', '')

    # Early exit if User-Agent is missing
    if not user_agent:
        return True

    # Check if User-Agent matches any known bot substrings
    if BOT_REGEX.search(user_agent):
        return True

    # Check for the presence of necessary headers
    # Flask's request.headers is case-insensitive
    missing_headers = NECESSARY_HEADERS - set(k.lower() for k in request.headers.keys())
    if missing_headers:
        return True

    return False
