import logging
import os
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import requests

BAR_CHART = u"\U0001F4CA"
CALENDAR = u"\U0001F4C5"
COUNTRY = u"\U0001F1EE" + u"\U0001F1F9"
GRINNING_FACE = u"\U0001F601"
HEAD_BANDAGE = u"\U0001F915"
HOSPITAL = u"\U0001F3E5"
HOUSE = u"\U0001F3E0"
MAN_TECHOLOGIS = u"\U0001F468" + u"\U0001F3FB" + u"\u200D" + u"\U0001F4BB"
MEDICAL_MASK = u"\U0001F637"
MICROBE = u"\U0001F9A0"
THERMOMETER = u"\U0001F912"
TEST = u"\U0001F9EA"
TOMB = u"\u26B0"
WARNING = u"\u26A0"
WAVING_HAND = u"\U0001F44B"
URL_NAZIONE = "https://corona.lmao.ninja/v2/countries/italy"
URL_REGIONI = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json"

TOKEN = os.getenv("TOKEN")
MODE = os.getenv("MODE")


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def button(update, context):
    query = update.callback_query

    regioni = {
        "1": "Abruzzo",
        "2": "Basilicata",
        "3": "Calabria",
        "4": "Campania",
        "5": "Emilia Romagna",
        "6": "Friuli Venezia Giulia",
        "7": "Lazio",
        "8": "Liguria",
        "9": "Lombardia",
        "10": "Marche",
        "11": "Molise",
        "12": "Piemonte",
        "13": "Puglia",
        "14": "Sardegna",
        "15": "Sicilia",
        "16": "Toscana",
        "17": "Trentino Alto Adige",
        "18": "Umbria",
        "19": "Valle d'Aosta",
        "20": "Veneto"
    }

    r = requests.get(url=URL_REGIONI)
    data = r.json()
    for regione in data:
        if regioni[query.data] == regione['denominazione_regione']:
            stats = COUNTRY + " *Regione*: " + regioni[query.data] + \
                "\n\n" + THERMOMETER + " *Casi:* " + \
                str(format(regione["totale_casi"], ',d')) + " (_+" + \
                str(format(regione["nuovi_positivi"], ',d')) + \
                " contagi oggi_)" + "\n" + TOMB + " *Deceduti:* " + \
                str(format(regione["deceduti"], ',d')) + "\n" + TEST + \
                " *Tamponi:* " + str(format(regione["tamponi"], ',d')) + \
                "\n" + HOSPITAL + " *Totale ospedalizzati:* " + \
                str(format(regione["totale_ospedalizzati"], ',d')) + \
                "\n" + THERMOMETER + " *Ricoverati con sintomi:* " + \
                str(format(regione["ricoverati_con_sintomi"], ',d')) + \
                "\n" + WARNING + " *Terapia intensiva:* " + \
                str(format(regione["terapia_intensiva"], ',d')) + \
                "\n"+ HOUSE + " *Isolamento domiciliare:* " + \
                str(format(regione["isolamento_domiciliare"], ',d')) + \
                "\n" + GRINNING_FACE + " *Dimessi guariti:* " + \
                str(format(regione["dimessi_guariti"], ',d')) + \
                "\n\n" + CALENDAR + " Ultimo aggiornamento: _" + \
                regione["data"].replace("T", " alle ") + "_"
            query.edit_message_text(text=stats, parse_mode='Markdown')


def stats_regioni(update, context):
    keyboard = [[InlineKeyboardButton("Abruzzo", callback_data='1'),
                 InlineKeyboardButton("Basilicata", callback_data='2')],
                [InlineKeyboardButton("Calabria", callback_data='3')],
                [InlineKeyboardButton("Campania", callback_data='4')],
                [InlineKeyboardButton("Emilia Romagna", callback_data='5')],
                [InlineKeyboardButton("Friuli Venezia Giulia", callback_data='6')],
                [InlineKeyboardButton("Lazio", callback_data='7')],
                [InlineKeyboardButton("Liguria", callback_data='8')],
                [InlineKeyboardButton("Lombardia", callback_data='9')],
                [InlineKeyboardButton("Marche", callback_data='10')],
                [InlineKeyboardButton("Molise", callback_data='11')],
                [InlineKeyboardButton("Piemonte", callback_data='12')],
                [InlineKeyboardButton("Puglia", callback_data='13')],
                [InlineKeyboardButton("Sardegna", callback_data='14')],
                [InlineKeyboardButton("Sicilia", callback_data='15')],
                [InlineKeyboardButton("Toscana", callback_data='16')],
                [InlineKeyboardButton("Trentino Alto Adige", callback_data='17')],
                [InlineKeyboardButton("Umbria", callback_data='18')],
                [InlineKeyboardButton("Valle d'Aosta", callback_data='19')],
                [InlineKeyboardButton("Veneto", callback_data='20')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Scegliere una regione:', reply_markup=reply_markup)


def stats_nazione(update, context):
    r = requests.get(url=URL_NAZIONE)
    data = r.json()
    stats = COUNTRY + " *Paese*: Italia\n\n" + THERMOMETER +" *Casi:* " + \
        str(format(data["cases"], ',d')) + "\n" + MEDICAL_MASK + \
        " *Casi giornalieri:* " + str(format(data["todayCases"], ',d')) + \
        "\n" + TOMB + " *Deceduti:* " + str(format(data["deaths"], ',d')) + \
        "\n" + TOMB + " *Morti giornaliere:* " + \
        str(format(data["todayDeaths"], ',d')) + \
        "\n" + THERMOMETER + " *Ricoverati:* " + \
        str(format(data["recovered"], ',d')) + \
        "\n" + HEAD_BANDAGE + " *Casi attivi:* " + \
        str(format(data["active"], ',d')) + \
        "\n" + MEDICAL_MASK + " *Casi critici:* " + \
        str(format(data["critical"], ',d')) + \
        "\n" + TEST + " *Test effettuati:* " + \
        str(format(data["tests"], ',d')) + \
        "\n\n" + CALENDAR + " Ultimo aggiornamento: " + \
        time.strftime('_%Y-%m-%d alle %H:%M:%S_', \
        time.localtime(data["updated"]/1000))
    update.message.reply_text(stats, parse_mode='Markdown')


def start(update, context):
    user = update.message.from_user
    print(user)

    update.message.reply_text(WAVING_HAND + " Ciao " + \
        user["first_name"] + \
        ", questo bot ti mostra le statistiche aggiornate sul Coronavirus " + \
        "in Italia. " + MICROBE)
    update.message.reply_text("Puoi controllarmi cliccando i seguenti " + \
        "comandi:\n\n/statsnazione - Mostra le statistiche nazionali del " + \
        "Coronavirus in Italia\n" + "/statsregioni - Mostra le statistiche" + \
        " per regione del Coronavirus in Italia\n\n\n" + \
        BAR_CHART + "Datasource:\n\t\t\t\t\t\t\t - " + \
        "https://github.com/NovelCOVID/API \n\t\t\t\t\t\t\t\t- " + \
        "https://github.com/pcm-dpc/COVID-19\n\n" + \
        MAN_TECHOLOGIS + "Bot creato da: @stefanomart", \
        disable_web_page_preview=True)


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN, use_context=True)

    # add handlers
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('statsnazione', stats_nazione))
    updater.dispatcher.add_handler(CommandHandler('statsregioni', stats_regioni))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    print('Listening ...')

    if MODE == "dev":
        updater.start_polling()
    elif MODE == "prod":
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))