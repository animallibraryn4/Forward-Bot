<h1 align="center">
    ──「 TG FILE SEQUENCE BOT 」──
</h1>

<p align="center">
  <img src="https://files.catbox.moe/hwt0gl.jpg" alt="Bot Logo">
</p>

<p align="center">
  <a href="https://www.python.org/"> <img src="https://img.shields.io/badge/Language-Python-orange?style=for-the-badge&logo=python" alt="Python" /> </a>
  <a href="https://github.com/RioShin2025/SequenceBot/blob/main/LICENSE"> <img src="https://img.shields.io/badge/License-MIT-blueviolet?style=for-the-badge" alt="License" /> </a>
</p>



---

### ✨ Features
- **Smart Parsing**: Automatically detects Episode numbers, Seasons, and Video Quality (480p, 720p, 1080p, etc.) from filenames.
- **Two Sequencing Modes**:
  - `Episode Flow`: Organized as Season -> Episode -> Quality.
  - `Quality Flow`: Organized as Season -> Quality -> Episode.
- **LS Mode (Batch Processing)**: Sequence entire ranges of files from a channel using message links.
- **Multi-Channel Force Subscribe**: Supports up to 3 channels to boost your community growth.
- **Database Driven**: Uses MongoDB to track user statistics and global settings.
- **Admin Suite**: Includes broadcast tools, real-time status monitoring, and a global leaderboard.
- **Web Server Integration**: Built-in Flask server to keep the bot alive on platforms like Render or Koyeb.

---

### 🛠️ Commands
| Command | Description |
| :--- | :--- |
| `/start` | Initializes the bot and displays the welcome message. |
| `/sequence` | Starts the manual file sequencing process. |
| `/fileseq` | Switch between 'Episode Flow' and 'Quality Flow'. |
| `/ls` | Batch sequence files by providing the start and end message links from a channel. |
| `/leaderboard`| Displays the top contributors/users. |
| `/status` | (Admin) View bot uptime, database health, and user count. |
| `/broadcast`| (Admin) Send a message to all registered users. |

---

### 🚀 Local Deployment

1. **Clone the Repository**:
   ```bash
   git clone [https://github.com/RioShin2025/SequenceBot.git](https://github.com/RioShin2025/SequenceBot.git)
   cd SequenceBot

 * Install Dependencies:
   pip install -r requirements.txt

 * Configure Variables:
   Open config.py and fill in your credentials:
   * API_ID & API_HASH: Get them from my.telegram.org.
   * BOT_TOKEN: Obtain from @BotFather.
   * MONGO_URI: Your MongoDB connection string.
   * OWNER_ID: Your Telegram User ID.
 * Run the Bot:
   python3 sequence.py

🌐 Cloud Deployment
The bot is ready for deployment on Heroku, Render, or VPS:
 * Heroku: Use the provided app.json for one-click deployment.
 * Render/Koyeb: The webserver.py file acts as the entry point to satisfy the port binding requirements. Use python3 webserver.py as your start command.
🤝 Credits & Support
 * Developer: Rio Shin
 * Organization: Bots Kingdom
 * Base Project: Sahil0976
━━━━━━━━━━━━━━━━━━━━
<p align="center">
Built with ❤️ for the Telegram Community
</p>

### Improvements made:

1.  **Professional Tone**: Used clear, technical English suitable for a GitHub repository.
2.  **Deployment Guide**: Specifically mentioned how to use `webserver.py` for platforms like Render, which is often a pain point for users.
3.  **Command Table**: Organized commands into a readable table format.
4.  **Logic Highlights**: Explained the difference between `Episode Flow` and `Quality Flow` based on your `sequence.py` logic.


━━━━━━━━━━━━━━━━━━━━

Perfect, maine poora project deeply analyze kar liya hai. Neeche ek clean, professional, step-by-step README.md de raha hoon jo tum direct copy-paste kar sakte ho.
Isme introduction → features → working flow → commands → config → deploy → troubleshooting → community support sab kuch covered hai.




