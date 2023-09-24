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

print(stock.listing_companies())

class Company:
    def __init__(self, ticker, comGroupCode, organName, organShortName, organTypeCode, comTypeCode, icbName, icbNamePath, sector, industry, group, subgroup):
        self.ticker = ticker
        self.comGroupCode = comGroupCode
        self.organName = organName
        self.organShortName = organShortName
        self.organTypeCode = organTypeCode
        self.comTypeCode = comTypeCode
        self.icbName = icbName
        self.icbNamePath = icbNamePath
        self.sector = sector
        self.industry = industry      
        self.group = group
        self.subgroup = subgroup

list_company = []
print(stock.listing_companies())

for index, row in stock.listing_companies().iterrows():
    if (row['comGroupCode'] == "HOSE"):
        comp = Company(ticker=row['ticker'], 
                    comGroupCode=row['comGroupCode'],
                    organName=row['organName'], 
                    organShortName=row['organShortName'],
                    organTypeCode=row['organTypeCode'], 
                    comTypeCode=row['comTypeCode'],
                    icbName=row['icbName'], 
                    icbNamePath=row['icbNamePath'],
                    sector=row['sector'], 
                    industry=row['industry'],
                    group=row['group'], 
                    subgroup=row['subgroup']
                    )
        list_company.append(comp)

for comp in list_company:
    print(f"ticker: {comp.ticker}, comGroupCode: {comp.comGroupCode}, organName: {comp.organName}, organShortName: {comp.organShortName}")

print(stock.company_overview("NVL"))