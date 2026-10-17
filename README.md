# IT Bot Remote Control System

A complete system consisting of:
1. A Telegram bot that helps with IT topics, backed by live internet research.
2. A control API for managing the bot.
3. An Android app (built with Kivy) as a remote control for the bot.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Services](#running-the-services)
- [Building the Android APK](#building-the-android-apk)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Credits](#credits)
- [License](#license)

## Features

### Telegram Bot
- IT-only question answering with live research
- Code review and debugging
- Multi-language support (including Khmer)
- Per-user state and rate limiting
- Owner-only commands for administration
- Professional, structured responses

### Control API
- Secure authentication with JWT
- Bot management (start, stop, restart, status)
- Logs viewing (with sensitive data masked)
- Statistics and metrics
- Password change functionality
- Rate limiting and login attempt tracking

### Android App (Remote Control)
- Login screen with secure credential storage
- Dashboard with Start/Stop bot controls
- Real-time status and logs
- Settings for server configuration
- Dark/Light theme support
- Built and signed via GitHub Actions

## Architecture

### Overall Design
```
[User] <--> [Android App] <--> [Control API] <--> [Telegram Bot]
                              |
                              | (Direct communication)
                              v
                    [Telegram Servers]
```

The Android app communicates only with the Control API. The Control API communicates with the Telegram Bot via direct function calls (same process) or via a message queue (if scaled). For simplicity, the bot and API are designed to run as separate services on the same server, with the API managing the bot's lifecycle.

### Components
- **Telegram Bot** (`bot/`): Handles all Telegram interactions, research, and responses.
- **Control API** (`api/`): FastAPI service providing endpoints for bot management.
- **Android App** (`app/`): Kivy-based remote control interface.
- **Tests** (`tests/`): Unit tests for bot and API components.
- **Build Automation** (`.github/workflows/build-apk.yml`): GitHub Actions workflow for building and signing the APK.

## Installation

### Prerequisites
- Python 3.9+
- Git
- (For Android APK build) Java JDK 11, Android SDK, NDK (handled by GitHub Actions)
- A Telegram Bot Token (from @BotFather)
- A server to host the bot and API (Linux recommended)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd <repository-directory>
   ```

2. **Set up environment variables**
   Copy `.env.example` to `.env` and fill in the required values:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

   Required variables:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram Bot token from @BotFather
   - `SECRET_KEY`: A strong secret key for JWT encryption (use `openssl rand -hex 32` to generate)
   - `API_URL`: The URL where the API will be accessible (for the Android app)

   Optional variables (for research enhancement):
   - `TAVILY_API_KEY`: For Tavily search API (if available)

3. **Install Python dependencies**
   ```bash
   # For the bot
   cd bot
   pip install -r requirements.txt
   
   # For the API
   cd ../api
   pip install -r requirements.txt
   
   # For tests (optional)
   cd ../tests
   pip install -r test_requirements.txt
   ```

4. **Initialize the database** (if applicable)
   The API uses a fake user database for simplicity. In production, replace with a real database.

## Configuration

### Environment Variables
All configuration is done via environment variables in the `.env` file:

| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot token | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `SECRET_KEY` | Secret key for JWT signing | `your-256-bit-secret` |
| `API_URL` | Base URL of the API (for Android app) | `https://yourdomain.com` |
| `TAVILY_API_KEY` | (Optional) Tavily API key for enhanced search | `tvly-...` |

### Bot Configuration
The bot configuration is in `bot/config.py`:
- Research engine settings
- Handler configurations
- Telegram bot initialization

### API Configuration
The API configuration is in `api/main.py`:
- JWT settings (expiration, algorithm)
- CORS and security middleware
- Fake user database (replace with real DB in production)

### Android App Configuration
The Android app configuration is handled via:
- Buildozer specification (`buildozer.spec`)
- Runtime settings stored in Android Keystore (simulated in the app)

## Running the Services

### Option 1: Direct Execution (Development)
```bash
# In one terminal, start the bot:
cd bot
python main.py

# In another terminal, start the API:
cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Systemd Services (Production)
The repository includes systemd service files for running the bot and API as services.

1. Copy the service files to `/etc/systemd/system/`:
   ```bash
   sudo cp bot/bot.service /etc/systemd/system/
   sudo cp api/api.service /etc/systemd/system/
   ```

2. Reload systemd and start the services:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable bot.service api.service
   sudo systemctl start bot.service api.service
   ```

3. Check status:
   ```bash
   sudo systemctl status bot.service api.service
   ```

### Option 3: Docker (Alternative)
A Dockerfile is provided for containerized deployment (see [Dockerfile](#dockerfile)).

## Building the Android APK

The Android APK is built and signed automatically via GitHub Actions.

### Manual Build (for testing)
1. Install Buildozer dependencies:
   ```bash
   # Follow the Buildozer installation guide: https://kivy.org/doc/stable/guide/packaging-android.html
   ```

2. Build the APK:
   ```bash
   buildozer android debug
   # For release build:
   # buildozer android release
   ```

3. The APK will be located in `./bin/`.

### GitHub Actions
The workflow in `.github/workflows/build-apk.yml` automatically:
- Triggers on push to `main` branch
- Sets up the Android build environment
- Checks for signing secrets in GitHub Secrets
- Builds a debug APK if no secrets are provided
- Builds and signs a release APK if the following secrets are set:
  - `KEYSTORE`: Base64-encoded keystore file
  - `KEYSTORE_PASSWORD`: Keystore password
  - `KEY_ALIAS`: Key alias
  - `KEY_PASSWORD`: Key password
- Uploads the APK as a workflow artifact

### First-Build Checklist
1. Create a keystore for release signing (if desired):
   ```bash
   keytool -genkey -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-key-alias
   ```
2. Convert the keystore to Base64 for GitHub Secrets:
   ```bash
   base64 my-release-key.jks
   # Copy the output
   ```
3. Add the following secrets to your GitHub repository:
   - `KEYSTORE`: (Base64 output from above)
   - `KEYSTORE_PASSWORD`: (your keystore password)
   - `KEY_ALIAS`: (your key alias, e.g., `my-key-alias`)
   - `KEY_PASSWORD`: (your key password, if different from keystore password)
4. Push to the `main` branch to trigger the workflow.

## Usage

### Telegram Bot
- Start a chat with your bot on Telegram
- Use `/start` to see the main menu
- Ask IT-related questions in any language
- Use `/help` for a list of commands
- Owner-only commands (for @YourTelegramUsername):
  - `/stats`: View bot usage statistics
  - `/broadcast <message>`: Send a message to all users
  - `/ban <user_id>`: Ban a user
  - `/unban <user_id>`: Unban a user

### Control API
Access the API at `http://your-server:8000`:
- Interactive docs: `http://your-server:8000/docs`
- Alternative docs: `http://your-server:8000/redoc`

### Android App
1. Install the APK on your Android device
2. Launch the app
3. Enter your server URL (from `API_URL` in `.env`)
4. Log in with your API credentials (same as used in the API's fake user database):
   - Username: `admin`
   - Password: `adminpassword`
5. Use the dashboard to start/stop the bot and view logs
6. Adjust settings in the Settings screen

## Troubleshooting

### Common Issues

#### Bot fails to start
- Check that `TELEGRAM_BOT_TOKEN` is set correctly in `.env`
- Ensure the bot has internet access to reach Telegram servers
- Look at the bot's logs for specific error messages

#### API returns 500 errors
- Check the API logs for tracebacks
- Verify that the `SECRET_KEY` is set and is a strong string
- Ensure the bot is running if the API tries to manage it

#### Android app cannot connect to API
- Verify the `API_URL` in the app settings matches where the API is hosted
- Ensure the API is reachable from the device network
- Check that the API's CORS settings allow the device's origin
- Confirm login credentials are correct (default: admin/adminpassword)

#### APK build fails in GitHub Actions
- Check the workflow logs for specific errors
- Ensure all required Android SDK/NDK components are installed
- Verify that the signing secrets are correctly formatted if using release build

### Logs
- Bot logs: Standard output when running `bot/main.py` or via systemd journal (`journalctl -u bot.service`)
- API logs: Standard output when running `uvicorn` or via systemd journal (`journalctl -u api.service`)
- Build logs: Available in the GitHub Actions workflow run details

## Credits

Created by [@Unknown_user_error_404](https://t.me/Unknown_user_error_404)

This credit must be displayed in:
- Bot: `/start` footer, `/about` section (with "Contact the creator" button), `/help` footer
- APK: Splash screen (under logo), login screen footer, dashboard footer, Settings > About card
- Repository: README header and footer, LICENSE header, API's /docs title

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Last updated: 2026-10-17*