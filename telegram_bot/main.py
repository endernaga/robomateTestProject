import os

from load_dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from scrapy.workua.filtering import add_filter
from scrapy.workua.scrap import get_resumes_pages_with_pagination

load_dotenv("../.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")


class TelegramBot:
    SALARYFROM, SALARYTO, EXPERIENCE, TOWN, CATEGORY, KEYWORDS = range(6)

    def __init__(self, bot_token):
        application = Application.builder().token(bot_token).build()
        conversation = self.compile_conversation()
        application.add_handler(conversation)
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("parse", self.parse))
        application.add_handler(CommandHandler("next", self.next))
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def get_min_salary(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["filters"]["salaryfrom"] = update.message.text
        await update.message.reply_text("enter a max salary or /skip to skip")
        print(update.message.text)

        return self.SALARYTO

    async def skip_min_salary(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("skipping min salary")
        if context.user_data["filters"].get("salaryfrom"):
            del context.user_data["filters"]["salaryfrom"]
        await update.message.reply_text("you skipped min salary")
        await update.message.reply_text("enter a max salary or /skip to skip")

        return self.SALARYTO

    async def get_max_salary(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["filters"]["salaryto"] = update.message.text
        await update.message.reply_text("enter a expirience or /skip to skip")

        return self.EXPERIENCE

    async def skip_max_salary(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("skipping max salary")
        if context.user_data["filters"].get("salaryto"):
            del context.user_data["filters"]["salaryto"]
        await update.message.reply_text("you skipped max salary")
        await update.message.reply_text("enter a expirience or /skip to skip")

        return self.EXPERIENCE

    async def get_experience(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["filters"]["experience"] = update.message.text
        await update.message.reply_text("enter a town or /skip to skip")
        print(update.message.text)

        return self.TOWN

    async def skip_experience(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("skipping experience")
        if context.user_data["filters"].get("experience"):
            del context.user_data["filters"]["experience"]
        await update.message.reply_text("you skipped experience")
        await update.message.reply_text("enter a town or /skip to skip")
        return self.TOWN

    async def get_town(self, update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["filters"]["town"] = update.message.text
        await update.message.reply_text("enter a category or /skip to skip")

        return self.CATEGORY

    async def skip_town(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("skipping town")
        if context.user_data["filters"].get("town"):
            del context.user_data["filters"]["town"]
        await update.message.reply_text("you skipped town")
        await update.message.reply_text("enter a category or /skip to skip")

        return self.CATEGORY

    async def get_category(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["filters"]["category"] = update.message.text
        await update.message.reply_text("enter a keywords or /skip to skip")

        return self.KEYWORDS

    async def skip_category(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("skipping category")
        if context.user_data["filters"].get("category"):
            del context.user_data["filters"]["category"]
        await update.message.reply_text("you skipped category")
        await update.message.reply_text("enter a keywords or /skip to skip")

        return self.KEYWORDS

    async def get_keywords(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["filters"]["keywords"] = update.message.text
        context.user_data["filtered_url"] = await add_filter(
            "https://www.work.ua/resumes/", **context.user_data["filters"]
        )
        await update.message.reply_text("to start parsing write /parse")

        return ConversationHandler.END

    async def skip_keywords(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("skipping keywords")
        if context.user_data["filters"].get("keywords"):
            del context.user_data["filters"]["keywords"]
        context.user_data["filtered_url"] = await add_filter(
            "https://www.work.ua/resumes/", **context.user_data["filters"]
        )
        await update.message.reply_text("keywords skiped")
        await update.message.reply_text("to start parsing write /parse")

        return ConversationHandler.END

    def compile_conversation(self):
        return ConversationHandler(
            entry_points=[CommandHandler("filter", self.filter)],
            states={
                self.SALARYFROM: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND, self.get_min_salary
                    ),
                    CommandHandler("skip", self.skip_min_salary),
                ],
                self.SALARYTO: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND, self.get_max_salary
                    ),
                    CommandHandler("skip", self.skip_max_salary),
                ],
                self.EXPERIENCE: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND, self.get_experience
                    ),
                    CommandHandler("skip", self.skip_experience),
                ],
                self.TOWN: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_town),
                    CommandHandler("skip", self.skip_town),
                ],
                self.CATEGORY: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_category),
                    CommandHandler("skip", self.skip_category),
                ],
                self.KEYWORDS: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_keywords),
                    CommandHandler("skip", self.skip_keywords),
                ],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Hello! My job is parse a resumes from work.ua ! If you needed to add filter write /filter. To start parsing write /parse"
        )

    async def filter(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["filters"] = {}
        await update.message.reply_text("enter a min salary or /skip to skip")

        return self.SALARYFROM

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("Cancelling...")

    async def parse(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("starting parsing resumes...")
        if context.user_data.get("filtered_url"):
            await update.message.reply_text(
                f"parsing resumes from {context.user_data['filtered_url']}"
            )
        resumes = (
            get_resumes_pages_with_pagination(context.user_data["filtered_url"])
            if context.user_data.get("filtered_url")
            else get_resumes_pages_with_pagination(
                "https://www.work.ua/resumes/?period=6"
            )
        )
        await update.message.reply_text("Sending first 14 resumes...")
        for resume in await anext(resumes):
            await update.message.reply_text(self.format_resume(resume))
        context.user_data["resumes"] = resumes

        await update.message.reply_text("Write /next to get next resumes")

    async def next(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data.get("resumes"):
            for resume in await anext(context.user_data["resumes"]):
                await update.message.reply_text(self.format_resume(resume))
                await update.message.reply_text("Write /next to get next resumes")
        else:
            await update.message.reply_text(
                "To start getting a resumes you need to write /parse"
            )

    @staticmethod
    def format_resume(resume):
        job_position = resume["job_position"]
        years_of_experience = ", ".join(resume["years_of_experience"])
        skills = ", ".join(resume["skills"])
        location = resume["location"]
        salary = resume["salary"] if resume["salary"] else "N/A"
        url = resume["url"]

        return f"""
            Job Position: {job_position}
            Years of Experience: {years_of_experience}
            Skills: {skills}
            Location: {location}
            Salary: {salary}
            Url: {url}
            """


if __name__ == "__main__":
    TelegramBot(BOT_TOKEN)
