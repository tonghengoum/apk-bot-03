from telegram import Update
from telegram.ext import ContextTypes
from ..research_engine import ResearchEngine

# Use the same research engine instance
research_engine = ResearchEngine()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages that are not commands."""
    # Ignore messages from the bot itself
    if update.message.from_user.is_bot:
        return

    query = update.message.text
    if not query:
        return

    # Let the user know we're researching
    await update.message.reply_text(f"Researching '{query}'... Please wait.")

    # Do the research
    result = research_engine.research(query)

    # Send the result (split if too long)
    if len(result) > 4096:
        for i in range(0, len(result), 4096):
            await update.message.reply_text(result[i:i+4096])
    else:
        await update.message.reply_text(result)