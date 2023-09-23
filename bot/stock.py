import pandas as pd
import requests as rq
import vnstock as stock

import telegram
from telegram import (
    Update,
    User,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    AIORateLimiter,
    filters
)
from telegram.constants import ParseMode, ChatAction

# def get_hose_company_only(x):
#     return x.comGroupCode == "HOSE"

# listing_companies = stock.listing_companies().values.tolist();
# # hose_companies = filter(get_hose_company_only, listing_companies)

# for comp in listing_companies:
#     print(type(comp))

# print(listing_companies)

print(stock.listing_companies())

class Company:
    def __init__(self, ticker, comGroupCode):
        self.ticker = ticker
        self.comGroupCode = comGroupCode

list_company = []

for index, row in stock.listing_companies().iterrows():
    comp = Company(ticker=row['ticker'], comGroupCode=row['comGroupCode'])
    list_company.append(comp)

for comp in list_company:
    print(f"ticker: {comp.ticker}, comGroupCode: {comp.comGroupCode}")