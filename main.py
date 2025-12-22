import asyncio
import logging
from config import Config
from pyrogram import Client as VJ, idle
from plugins.regix import restart_forwards

# Set up logging to help find errors
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize the Bot
VJBot = VJ(
    "VJ-Forward-Bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    sleep_threshold=120,
    plugins=dict(root="plugins")
)  

async def start_vj_bot():
    try:
        await VJBot.start()
        me = await VJBot.get_me()
        logger.info(f"@{me.username} started successfully!")
        
        # This restarts your forwarding tasks
        await restart_forwards(VJBot)
        
        await idle()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
    finally:
        await VJBot.stop()

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(start_vj_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
        
