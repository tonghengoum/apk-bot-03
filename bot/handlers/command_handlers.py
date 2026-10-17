from telegram import Update
from telegram.ext import ContextTypes
from ..research_engine import ResearchEngine

# Initialize research engine (can be done once per bot instance)
research_engine = ResearchEngine()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! I'm a research bot. "
        "Use /help to see what I can do.",
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
    I can help you research topics using Wikipedia.

    Commands:
    /start - Start the bot and see a welcome message
    /help - Show this help message
    /research <topic> - Research a topic and get a summary from Wikipedia

    You can also just send me a message and I'll try to research it for you.
    """
    await update.message.reply_text(help_text)

async def research_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /research command."""
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("Please provide a topic to research. Example: /research Artificial intelligence")
        return

    # Let the user know we're researching
    await update.message.reply_text(f"Researching '{query}'... Please wait.")

    # Do the research
    result = research_engine.research(query)

    # Send the result (might be long, so we split if necessary)
    # Telegram message limit is 4096 characters
    if len(result) > 4096:
        # Split into multiple messages
        for i in range(0, len(result), 4096):
            await update.message.reply_text(result[i:i+4096])
    else:
        await update.message.reply_text(result)

# We can also define a function to handle unknown commands
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown commands."""
    await update.message.reply_text(
        "Sorry, I didn't understand that command. Use /help to see available commands."
    )