from telethon import events, Button

from ebook_converter_bot import LOCALES
from ebook_converter_bot.bot import BOT
from ebook_converter_bot.db.curd import update_language, get_lang
from ebook_converter_bot.utils.i18n import translate as _
from ebook_converter_bot.utils.telegram import tg_exceptions_handler


@BOT.on(events.NewMessage(pattern='/settings|/preferences'))
@BOT.on(events.CallbackQuery(pattern='update_preferences'))
@tg_exceptions_handler
async def preferences_handler(event: events.NewMessage.Event):
    """Set chat preferences."""
    buttons = [Button.inline("Language", data="update_language")]
    message = _("**Available bot preferences:**", lang=get_lang(event.chat_id))
    await event.respond(message, buttons=buttons) \
        if not hasattr(event, 'data') else await event.edit(message, buttons=buttons)


@BOT.on(events.CallbackQuery(pattern='update_language'))
@tg_exceptions_handler
async def update_language_callback(event: events.CallbackQuery.Event):
    """Update language handler"""
    lang = get_lang(event.chat_id)
    buttons = [Button.inline(f"{i['name']} ({i['nativeName']})", data=f"setlanguage_{i['code']}") for i in LOCALES
               ] + [Button.inline(_("Back", lang=lang), data="update_preferences")]
    await event.edit(_("**Select Bot language**", lang=lang),
                     buttons=[buttons[i::5] for i in range(5)])


@BOT.on(events.CallbackQuery(pattern=r'setlanguage_\w+'))
@tg_exceptions_handler
async def set_language_callback(event: events.CallbackQuery.Event):
    """Set language handler"""
    language_code = event.data.decode().split('_')[-1]
    update_language(event.chat_id, language_code)
    language = list(filter(lambda x: x["code"] == language_code, LOCALES))[0]
    language_name = language['name']
    language_native_name = language['nativeName']
    await event.edit(_("**Language has been set to**: {} ({})",
                       lang=get_lang(event.chat_id)).format(language_name, language_native_name),
                     buttons=[Button.inline(_("Back"), data="update_language")])
