import asyncio
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

API_TOKEN = ""
GROUP_CHAT_ID = 111111111
SCHOOL_NAME_UZ = "Anonim"
SCHOOL_NAME_RU = "Аноним"
SCHOOL_TIME_START = "8:00"
SCHOOL_TIME_END = "16:00"
SCHOOL_WORKING_DAYS = "5"
SCHOOL_ACCEPTS_FROM_GRADE = "1"
SCHOOL_ACCEPTS_TO_GRADE = "11"
SCHOOL_PHONE = "+99893-000-00-00"
SCHOOL_LOCATION_URL = "https://maps.app.goo.gl/"
SCHOOL_YOUTUBE_URL = "https://youtu.be/D79flAtyUPY"
SCHOOL_INSTAGRAM_URL = "https://www.instagram.com/"
SCHOOL_TELEGRAM_URL = "https://t.me/"
SCHOOL_ADRRESS_UZ = "Farobiy koʻchasi 259-uy"
SCHOOL_ADRRESS_RU = "ул. Фараби, 259"
SCHOOL_PRICE_PRIMARY = "4,700,000"
SCHOOL_PRICE_SENIOR = "4,900,000"
SCHOOL_LATITUDE = 41.340184
SCHOOL_LONGITUDE = 69.217025

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

class Contact(StatesGroup):
    name = State()
    phone = State()
    message = State()

class Work(StatesGroup):
    full_name = State()
    phone = State()
    cv = State()

class Admission(StatesGroup):
    region = State()
    classes = State()
    full_name = State()
    phone = State()

ALLOWED_MIME_TYPES = {
    'application/pdf', 'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/jpeg', 'image/png'
}

REGIONS_UZ = [
    "Mirzo Ulugʻbek tumani", "Yunusobod tumani", "Qibray tumani", "Yashnabod tumani",
    "Mirobod tumani", "Yakkasaroy tumani", "Chilonzor tumani", "Uchtepa tumani",
    "Olmazor tumani", "Shayxontohur tumani", "Sergeli tumani", "Bektemir tumani"
]

REGIONS_RU = [
    "Мирзо-Улугбекский район", "Юнусабадский район", "Кибрайский район", "Яшнабадский район",
    "Мирабадский район", "Яккасарайский район", "Чиланзорский район", "Учтепинский район",
    "Алмазарский район", "Шайхонтохурский район", "Сергелийский район", "Бектемирский район"
]

async def get_lang(state: FSMContext) -> str:
    data = await state.get_data()
    return data.get("language", "uz")

async def reset_state_keep_lang(state: FSMContext):
    lang = await get_lang(state)
    await state.clear()
    await state.update_data(language=lang)

def get_main_keyboard(lang: str) -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    if lang == "ru":
        buttons = [
            types.KeyboardButton(text="🌟 Общая информация"),
            types.KeyboardButton(text="📍 Наш адрес"),
            types.KeyboardButton(text="💰 Наши цены"),
            types.KeyboardButton(text="💼 Работа"),
            types.KeyboardButton(text="🎉 Преимущества школы"),
            types.KeyboardButton(text="📞 Связаться с нами"),
            types.KeyboardButton(text="📚 Прием в школу"),
            types.KeyboardButton(text="🇷🇺 Русский"),
            types.KeyboardButton(text="🇺🇿 O'zbekcha")
        ]
    else:
        buttons = [
            types.KeyboardButton(text="🌟 Umumiy ma'lumot"),
            types.KeyboardButton(text="📍 Manzilimiz"),
            types.KeyboardButton(text="💰 Narxlarimiz"),
            types.KeyboardButton(text="💼 Ish bo'yicha"),
            types.KeyboardButton(text="🎉 Maktab afzalliklari"),
            types.KeyboardButton(text="📞 Biz bilan bog'lanish"),
            types.KeyboardButton(text="📚 Maktabga qabul"),
            types.KeyboardButton(text="🇷🇺 Русский"),
            types.KeyboardButton(text="🇺🇿 O'zbekcha")
        ]
    for btn in buttons:
        builder.add(btn)
    builder.adjust(2, 2, 2, 1, 2)
    return builder.as_markup(resize_keyboard=True)

def get_contact_keyboard(lang: str) -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    if lang == "ru":
        builder.add(types.KeyboardButton(text="📞 Отправить контакт", request_contact=True))
    else:
        builder.add(types.KeyboardButton(text="📞 Kontaktni yuborish", request_contact=True))
    return builder.as_markup(resize_keyboard=True)

@dp.startup()
async def on_startup(bot: Bot):
    await bot.set_my_commands([
        types.BotCommand(command="/start", description="Botni ishga tushirish"),
        types.BotCommand(command="/info", description="Umumiy ma'lumot"),
        types.BotCommand(command="/location", description="Bizning manzil"),
        types.BotCommand(command="/price", description="Narhlar haqida ma'lumot"),
        types.BotCommand(command="/advantage", description="Maktab afzaliklari"),
        types.BotCommand(command="/contact", description="Biz bilan bog'lanish"),
        types.BotCommand(command="/work", description="Ish bo'yicha"),
    ])

@dp.message(F.text.in_(["/start"]))
async def send_start_menu(message: types.Message, state: FSMContext):
    await reset_state_keep_lang(state)
    lang = await get_lang(state)
    if lang == "ru":
        text = "Здравствуйте, пожалуйста, выберите один из следующих вариантов для более быстрого получения информации по вашему вопросу:"
    else:
        text = "Assalomu alaykum, savolingiz bo'yicha tezroq ma'lumot olish uchun quyidagilardan birini tanlang:"
    await message.answer(text, reply_markup=get_main_keyboard(lang))

@dp.message(F.text.in_(["🇷🇺 Русский", "🇺🇿 O'zbekcha"]))
async def handle_language_selection(message: types.Message, state: FSMContext):
    lang = "ru" if message.text == "🇷🇺 Русский" else "uz"
    await state.clear()
    await state.update_data(language=lang)
    await send_start_menu(message, state)

@dp.message(F.text.in_(["🌟 Общая информация", "🌟 Umumiy ma'lumot", "/info"]))
async def all_info(message: types.Message, state: FSMContext):
    await reset_state_keep_lang(state)
    lang = await get_lang(state)
    if lang == 'ru':
        text = (f""
            f"<b>🏫 Школа {SCHOOL_NAME_RU} принимает учеников с {SCHOOL_ACCEPTS_FROM_GRADE} по {SCHOOL_ACCEPTS_TO_GRADE} класс.</b>\n\n"
            f"⏰ График работы школы: с {SCHOOL_TIME_START} до {SCHOOL_TIME_END}. / {SCHOOL_WORKING_DAYS} дней\n"
            f"🎯 Все предметы проводятся углубленно! \n\n"
            f"📚 <b>Языкоориентированные уроки</b>\n🇬🇧 Английский язык\n🇷🇺 Русский язык\n🇨🇳 Китайский язык\n🇹🇷 Турецкий язык\n🇰🇷 Корейский язык\n🇸🇦 Арабский язык\n\n"
            f"🙍‍♂️ <b>Для мальчиков</b>\n🥋 Таеквандо\n⚽️ Футбол\n🎾 Теннисный корт\n🏇🏻 Верховая езда\n🏊🏻 Бассейн\n🏹 Стрельба из лука\n💻 Киберспорт\n\n"
            f"🙎‍♀️ <b>Для девочек</b>\n👩🏻‍⚕️ Медицинский курс\n👩🏻‍🍳 Курс национальной и европейской кухни\n🧵 Пошив одежды\n🖌️ Курс дизайна\n🦋 Курс этики и эстетики\n🧕🏼 Курс психологии\n🤸🏻 Гимнастика\n\n"
            f"📙 <b>Общий</b>\n📱 СММ (Мобилография)\n🎾 Теннис\n🏀 Баскетбол\n🏐 Волейбол\n📝 Архитектура\n🧑🏻‍💻 ИТ-программирование\n🧮 Бухгалтерский учет (Аудит)\n🏁 Шахматы и шашки\n🤖 Робототехника\n🚛 Логистика\n\n"
            f"<blockquote>🏢 Наша школа – это процветающее учебное заведение, в котором учатся более 700 учеников, и наша учебная программа разработана так, чтобы предлагать широкий спектр предметов и навыков, чтобы обеспечить всестороннюю подготовку учащихся</blockquote>\n"
            f"<blockquote>🍛 Кухня призвана предлагать здоровую, халяльную еду, чтобы поддержать концентрацию учащихся и уровень энергии в течение дня</blockquote>\n"
            f"<blockquote>🗞 Большинство наших выпускников поступили в ТОП университеты мира с результатами IELTS 7-7,5</blockquote>\n"
            f"<b>📌 Дополнительной информации:</b>\n"
            f"☎️ {SCHOOL_PHONE} 📍 <a href='{SCHOOL_LOCATION_URL}'>Наш адрес</a>\n\n"
            f"🔗 <b>Страницы в социальных сетях</b>\n"
            f"👉 <a href='{SCHOOL_YOUTUBE_URL}'>Youtube</a> | <a href='{SCHOOL_INSTAGRAM_URL}'>Instagram</a> | <a href='{SCHOOL_TELEGRAM_URL}'>Telegram</a>")
    else:
        text = (f""
            f"<b>🏫 {SCHOOL_NAME_UZ} School maktabi {SCHOOL_ACCEPTS_FROM_GRADE}-sinfdan {SCHOOL_ACCEPTS_TO_GRADE}-sinfgacha bo'lgan o'quvchilarni qabul qiladi</b>\n\n"
            f"⏰ Maktab soatlari: {SCHOOL_TIME_START} dan {SCHOOL_TIME_END} gacha / {SCHOOL_WORKING_DAYS} kun\n"
            f"🎯 Barcha fanlar chuqurlashtirilgan tarzda olib boriladi \n\n"
            f"📚 <b>Tilga yo'naltirilgan darslarimiz</b>\n🇬🇧 Ingliz tili\n🇷🇺 Rus tili\n🇨🇳 Xitoy tili\n🇹🇷 Turk tili\n🇰🇷 Koreys tili\n🇸🇦 Arab tili\n\n"
            f"🙍‍♂️ <b>O'g'il bolalar uchun</b>\n🥋 Taekwondo\n⚽️ Futbol\n🎾 Tenis ko'rt\n🏇🏻 Ot minish\n🏊🏻 Basseyn (suv havzasi)\n🏹 Kamondan oʻq otish\n💻 Kiber sport\n\n"
            f"🙎‍♀️ <b>Qizlar uchun</b>\n👩🏻‍⚕️ Tibbiyot kursi\n👩🏻‍🍳 Milliy va yevropa taomlari\n🧵 Tikuvchilik\n🖌️ Dizaynerlik\n🦋 Etika va Estetika\n🧕🏼 Psixologiya\n🤸🏻 Gimnastika\n\n"
            f"📙 <b>Umumiy</b>\n📱 SMM(Mobilografia)\n🎾 Tenis ko’rt\n🏀 Basketbol\n🏐 Voleybol\n📝 Arxitektura\n🧑🏻‍💻 IT Dasturlash\n🧮 Buxgalteriya(Audit)\n🏁 Shaxmat Shashka\n🤖 Robototexnika\n🚛 Logistika\n\n"
            f"<blockquote>🏢 Bizning maktab 700 dan ortiq o'quvchilarga ega bo'lgan rivojlanayotgan ta'lim muassasasi bo'lib, Bizning o'quv dasturimiz o'quvchilarning har tomonlama ta'lim olishlarini ta'minlaydigan keng ko'lamli fanlar va ko'nikmalarni taklif qilishga mo'ljallangan</blockquote>\n"
            f"<blockquote>🍛 Oshxona kun davomida o'quvchilarning konsentratsiyasi va energiya darajasini qo'llab-quvvatlash uchun sog'lom, halol, oziq-ovqat tanlovlarini taklif qilishni maqsad qilgan</blockquote>\n"
            f"<blockquote>🗞 Bitiruvchilarimizning aksari IELTS 7-7.5 natija ko'rsatib dunyoning TOP universitetlariga kirishdi</blockquote>\n"
            f"<b>📌 Batafsil ma’lumot uchun:</b>\n"
            f"☎️ {SCHOOL_PHONE} 📍 <a href='{SCHOOL_LOCATION_URL}'>Manzil</a>\n\n"
            f"🔗 <b>Ijtimoiy tarmoqdagi sahifalarimiz</b>\n"
            f"👉 <a href='{SCHOOL_YOUTUBE_URL}'>Youtube</a> | <a href='{SCHOOL_INSTAGRAM_URL}'>Instagram</a> | <a href='{SCHOOL_TELEGRAM_URL}'>Telegram</a>")
    await message.answer(text)

@dp.message(F.text.in_(["📍 Наш адрес", "📍 Manzilimiz", "/location"]))
async def location_info(message: types.Message, state: FSMContext):
    await reset_state_keep_lang(state)
    lang = await get_lang(state)
    if lang == 'ru':
        text = (f""
            f"<b>Наша школа расположена в Алмазорском районе города Ташкента</b>\n"
            f"<b>Место назначения: {SCHOOL_ADRRESS_RU}</b>\n"
            f"📌 <b>Дополнительной информации:</b>\n"
            f"☎️ {SCHOOL_PHONE} | <a href='{SCHOOL_LOCATION_URL}'>📍 Наш адрес</a>\n\n"
            f"🔗 <b>Страницы в социальных сетях</b>\n👉 <a href='{SCHOOL_YOUTUBE_URL}'>Youtube</a> | <a href='{SCHOOL_INSTAGRAM_URL}'>Instagram</a> | <a href='{SCHOOL_TELEGRAM_URL}'>Telegram</a>")
    else:
        text = (f""
            f"<b>Maktabimiz Toshkent shahrining Olmazor tumanida joylashgan</b>\n"
            f"<b>Mo’ljal: {SCHOOL_ADRRESS_UZ}</b>\n"
            f"📌 <b>Batafsil ma’lumot uchun:</b>\n"
            f"☎️ {SCHOOL_PHONE} | <a href='{SCHOOL_LOCATION_URL}'>📍 Manzil</a>\n\n"
            f"🔗 <b>Ijtimoiy tarmoqdagi sahifalarimiz</b>\n👉 <a href='{SCHOOL_YOUTUBE_URL}'>Youtube</a> | <a href='{SCHOOL_INSTAGRAM_URL}'>Instagram</a> | <a href='{SCHOOL_TELEGRAM_URL}'>Telegram</a>")
    await message.answer(text)
    await bot.send_location(chat_id=message.chat.id, latitude=SCHOOL_LATITUDE, longitude=SCHOOL_LONGITUDE)

@dp.message(F.text.in_(["💰 Наши цены", "💰 Narxlarimiz", "/price"]))
async def price_info(message: types.Message, state: FSMContext):
    await reset_state_keep_lang(state)
    lang = await get_lang(state)
    if lang == 'ru':
        text = (f"<blockquote><b>Стоимость ежемесячной оплаты:</b>\n"
            f"• {SCHOOL_PRICE_PRIMARY} сум для начальных классов\n"
            f"• Для высших классов – {SCHOOL_PRICE_SENIOR} сумов\n\n"
            f"❗️ Наша школа предлагает различные скидки, чтобы сделать обучение более удобным. "
            f"В нашей школе действуют скидки до 5%, 10% и 15%. Наши скидки составляют 5% от абонентской платы, если из 1 семьи приезжают 2 ребенка. "
            f"А при оплате раз в полгода (независимо от того, сколько детей) действует скидка 10 процентов. "
            f"При наличии 3 и более детей из 1 семьи действует скидка 15%</blockquote>\n\n"
            f"📌 <b>Дополнительной информации:</b>\n"
            f"☎️ {SCHOOL_PHONE} | <a href='{SCHOOL_LOCATION_URL}'>📍 Наш адрес</a>\n\n"
            f"🔗 <b>Страницы в социальных сетях</b>\n👉 <a href='{SCHOOL_YOUTUBE_URL}'>Youtube</a> | <a href='{SCHOOL_INSTAGRAM_URL}'>Instagram</a> | <a href='{SCHOOL_TELEGRAM_URL}'>Telegram</a>")
    else:
        text = (f"<blockquote><b>Oylik to’lov narxlari:</b>\n"
            f"• Boshlang'ich sinflar uchun {SCHOOL_PRICE_PRIMARY} so'm\n"
            f"• Yuqori sinflar uchun esa {SCHOOL_PRICE_SENIOR} so’mni tashkil qiladi\n\n"
            f"❗️ Maktabimiz ta'limni yanada qulay qilish uchun turli chegirmalar taklif qilmoqda. "
            f"Bizning maktabda 5 foiz, 10 foiz va 15 foizgacha chegirmalar bor Chegirmalarimiz, agar 1 ta oiladan 2 farzand keladigan bo'lsa, oylik to'lovdan 5 foizga chegirmasi bor. "
            f"Va yarim yillik tol'ov amalga oshirilsa 10 foiz chegirma bo'ladi (nechta farzand bo'lishidan qat'iy nazar). "
            f"Agarda 1 ta oiladan, 3 yoki undan ortiqroq farzand keladigan bo'lsa, 15 foizgacha chegirma bor</blockquote>\n\n"
            f"📌 <b>Batafsil ma’lumot uchun:</b>\n"
            f"☎️ {SCHOOL_PHONE} | <a href='{SCHOOL_LOCATION_URL}'>📍 Manzil</a>\n\n"
            f"🔗 <b>Ijtimoiy tarmoqdagi sahifalarimiz</b>\n👉 <a href='{SCHOOL_YOUTUBE_URL}'>Youtube</a> | <a href='{SCHOOL_INSTAGRAM_URL}'>Instagram</a> | <a href='{SCHOOL_TELEGRAM_URL}'>Telegram</a>")
    await message.answer(text)

@dp.message(F.text.in_(["🎉 Преимущества школы", "🎉 Maktab afzalliklari", "/advantage"]))
async def advantage_info(message: types.Message, state: FSMContext):
    await reset_state_keep_lang(state)
    lang = await get_lang(state)
    if lang == "ru":
        text = (f""
            f"<b>Основные сильные стороны нашей школы\n\n"
            f"Нашу школу отличает ориентация на десять важных направлений:</b>\n\n"
            f"<blockquote><b>1 • Здание и сооружения</b>\n"
            f"Инфраструктура школы тщательно спроектирована для создания оптимальной образовательной среды. "
            f"Учебные классы светлые, хорошо проветриваемые и оснащены современным оборудованием. "
            f"В здании есть полностью оборудованный спортивный зал, многофункциональный зал для занятий, стадион, специализированные лаборатории, технологический центр, просторный внутренний двор и зеленый сад\n\n"
            f"<b>2 • Преподавательский состав</b>\n"
            f"Наши преподаватели отобраны из более чем 2000 кандидатов и представляют собой лучших специалистов в своих областях. "
            f"Они проходят строгий отборочный процесс, где оцениваются их опыт, знания и педагогические навыки. "
            f"Мы поощряем непрерывное профессиональное развитие, и большинство наших учителей регулярно участвуют в программах повышения квалификации.\n\n"
            f"<b>3 • Отбор учеников</b>\n"
            f"Мы поддерживаем высокий академический стандарт, принимая учеников на основе собеседования. "
            f"За исключением учеников 1-4 классов, все школьники должны пройти строгий вступительный экзамен. "
            f"Также мы подчеркиваем важность участия родителей в процессе отбора для обеспечения поддерживающей учебной среды\n\n"
            f"<b>4 • Комплексная учебная программа</b>\n"
            f"Наша учебная программа не только соответствует государственным образовательным требованиям, но и включает дополнительные программы для обогащения учебного опыта учеников. "
            f"Международно признанная программа Оксфорда дополняет изучение английского языка, а расширенные учебные программы, такие как программы Петерсона и Рамзаевой, внедряются на начальных этапах\n\n"
            f"<b>5 • Внеклассные программы</b>\n"
            f"Мы предлагаем широкий спектр внеклассных мероприятий, направленных на развитие интересов и талантов учеников. "
            f"В наши кружки входят направления такие как: «SMM (Мобилография)», «Бухгалтерия (Аудит)», «Логистика», «Архитектура», «Робототехника», «Информационные технологии», «Шахматы», «Гимнастика», «Тхэквондо», «Айкидо», «Кулинария», «Физическая культура», а также изучение языков (русского, английского, китайского, корейского, турецкого и арабского)\n\n"
            f"<b>6 • Качественное питание</b>\n"
            f"Школьная столовая управляется опытными поварами, что обеспечивает сбалансированное и питательное питание учеников в течение дня. "
            f"Программа питания включает в себя четырехразовое питание в день с акцентом на здоровые привычки питания и использование высококачественных ингредиентов\n\n"
            f"<b>7 • Участие сообщества</b>\n"
            f"Мы активно сотрудничаем с родителями и местными организациями для поддержки развития наших учеников. "
            f"Постоянные мероприятия, семинары и открытые форумы способствуют укреплению связи между школой и её сообществом\n\n"
            f"<b>8 • Технологическое развитие</b>\n"
            f"Технологии глубоко интегрированы в наш образовательный подход. "
            f"Учебные классы оснащены новейшим цифровым оборудованием, а ученики могут пользоваться современным информационно-технологическим центром. "
            f"Мы ставим в приоритет цифровую грамотность и гарантируем, что наши ученики будут готовы к требованиям будущего в области технологий\n\n"
            f"<b>9 • Безопасная среда</b>\n"
            f"Безопасность наших учеников стоит на первом месте. "
            f"Школа оснащена комплексными мерами безопасности, включая системы наблюдения и контролируемые точки входа. "
            f"Наш персонал обучен поддерживать безопасную и поддерживающую среду для всех учеников\n\n"
            f"<b>10 • Личностное развитие и поддержка</b>\n"
            f"Мы уделяем особое внимание личностному росту учеников, помогая им развивать уверенность в себе, стойкость и важные жизненные навыки. "
            f"Регулярная обратная связь и индивидуальная поддержка обеспечивают получение каждым учеником необходимой мотивации и ресурсов для академического и личностного роста</blockquote>\n\n"
            f"📌 <b>Дополнительной информации:</b>\n"
            f"☎️ {SCHOOL_PHONE} | <a href='{SCHOOL_LOCATION_URL}'>📍 Наш адрес</a>\n\n"
            f"🔗 <b>Страницы в социальных сетях</b>\n👉 <a href='{SCHOOL_YOUTUBE_URL}'>Youtube</a> | <a href='{SCHOOL_INSTAGRAM_URL}'>Instagram</a> | <a href='{SCHOOL_TELEGRAM_URL}'>Telegram</a>")
    else:
        text = (f""
            f"<b>Maktabimizning asosiy kuchli tomonlari\n\n"
            f"Bizning maktab o'nta muhim yo'nalishga qaratilganligi bilan ajralib turadi:</b>\n\n"
            f"<blockquote><b>1 • Bino Inshootlari</b>\n"
            f"Maktab infratuzilmasi optimal ta'lim muhitini yaratish uchun puxta ishlab chiqilgan. "
            f"O‘quv xonalari yorug‘, havosi yaxshi, zamonaviy jihozlar bilan ta’minlangan. "
            f"Binoda to‘liq jihozlangan sport zali, ko‘p funksiyali mashg‘ulotlar zali, sport stadioni, ixtisoslashtirilgan fan laboratoriyalari, texnologiya markazi, keng ochiq hovli va yam-yashil bog‘ mavjud.\n\n"
            f"<b>2 • Maktab O'qtuvchilari</b>\n"
            f"Bizning professor-o'qituvchilar tarkibi 2000 dan ortiq nomzodlar orasidan tanlangan eng yaxshi mutaxassislardan iborat. "
            f"Ularning tajribasi, fanlarni o'zlashtirishi va o'qituvchilik qobiliyatlari baholanadigan qattiq tanlov jarayonidan o'tadilar. "
            f"Uzluksiz kasbiy o'sish rag'batlantiriladi, aksariyat o'qituvchilarimiz malaka oshirish dasturlarida muntazam qatnashadilar.\n\n"
            f"<b>3 • O'quvchi Tanlo'vi</b>\n"
            f"Biz O'quvchilarni savol-javov asosida qabul qilish orqali yuqori akademik standartlarni saqlab qolamiz. "
            f"1-4  sinf o'quvchilari bundan mustasno, barcha o'quvchilar qattiq kirish imtihonidan o'tishlari kerak. "
            f"Shuningdek, biz qo'llab-quvvatlovchi o'quv muhitini ta'minlash uchun qabul jarayonida ota-onalarning ishtiroki muhimligini ta'kidlaymiz\n\n"
            f"<b>4 • Kompleks o'quv dasturi</b>\n"
            f"Bizning o'quv dasturimiz nafaqat davlat ta'lim talablariga javob beradi, balki talabalarning o'rganish tajribasini boyitish uchun qo'shimcha dasturlarni ham o'z ichiga oladi. "
            f"Xalqaro miqyosda tan olingan Oksford dasturi ingliz tilini o'qitishni to'ldiradi, Peterson va Ramzaeva dasturlari kabi kengaytirilgan o'quv dasturlari boshlang'ich bosqichda amalga oshiriladi\n\n"
            f"<b>5 • Turli sinfdan tashqari dasturlar</b>\n"
            f"Biz o‘quvchilarning qiziqish va iste’dodini rivojlantirishga qaratilgan keng ko‘lamli sinfdan tashqari tadbirlarni taklif etamiz. "
            f"To‘garaklarimizda  “SMM(Mobilografia)”, “Buxgalteriya(Audit)”, “Logistika”, “Arxitektura”, “Robotexnika”, “Axborot texnologiyalari”, “Shaxmat”, “Gimnastika”, “Taekvondo”, “Aykido”, “Pazandachilik”, “Jismoniy tarbiya”, “Rus, Ingliz, Xtoy, Koreys, Turk va Arab tillarida til o‘rganish” kabi yo‘nalishlar mavjud\n\n"
            f"<b>6 • Sifatli ovqatlanish</b>\n"
            f"Maktab oshxonasi tajribali oshpazlar tomonidan boshqariladi, bu esa o‘quvchilarning kun davomida to‘yimli, muvozanatli ovqatlanishini ta’minlaydi. "
            f"o‘quvchilar uchun kuniga 4 mahal ovqatlanishni o‘z ichiga olgan ovqatlanish dasturimiz sog‘lom ovqatlanish odatlari va yuqori sifatli ingredientlarga urg‘u beradi\n\n"
            f"<b>7 • Jamiyat ishtiroki</b>\n"
            f"O'quvchilarimizning rivojlanishini qo'llab-quvvatlash uchun ota-onalar va mahalliy tashkilotlar bilan faol hamkorlik qilamiz. "
            f"Doimiy tadbirlar, seminarlar va ochiq forumlar maktab va uning jamoasi o'rtasidagi aloqani mustahkamlashga yordam beradi\n\n"
            f"<b>8 • Texnologik taraqqiyot</b>\n"
            f"Texnologiya bizning ta'lim yondashuvimizga chuqur integratsiyalashgan. "
            f"O‘quv xonalari eng so‘nggi raqamli uskunalar bilan jihozlangan bo‘lib, talabalar zamonaviy axborot texnologiyalari xonasidan foydalanishlari mumkin. "
            f"Biz raqamli savodxonlikni birinchi o'ringa qo'yamiz va o'quvchilarning kelajak texnologik talablariga yaxshi tayyorlanishini ta'minlaymiz\n\n"
            f"<b>9 • Xavfsiz muhit</b>\n"
            f"O'quvchilarimiz xavfsizligi birinchi o'rinda turadi. "
            f"Maktab keng qamrovli xavfsizlik choralari, jumladan, kuzatuv tizimlari va boshqariladigan kirish nuqtalari bilan jihozlangan. "
            f"Bizning xodimlarimiz barcha o'quvchilar uchun xavfsiz va qo'llab-quvvatlovchi muhitni saqlashga o'rgatilgan\n\n"
            f"<b>10 • Shaxsiy rivojlanish va uni qo'llab-quvvatlash</b>\n"
            f"Biz o‘quvchilarning shaxsiy o‘sishini ta’minlashga, ularga ishonch, chidamlilik va muhim hayotiy ko‘nikmalarni shakllantirishga yordam berishga e’tibor qaratamiz. "
            f"Muntazam fikr-mulohazalar va moslashtirilgan yordam har bir o'quvchining akademik va shaxsiy rivojlanishi uchun zarur bo'lgan dalda va resurslarni olishini ta'minlaydi</blockquote>\n\n"
            f"📌 <b>Batafsil ma’lumot uchun:</b>\n"
            f"☎️ {SCHOOL_PHONE} | <a href='{SCHOOL_LOCATION_URL}'>📍 Manzil</a>\n\n"
            f"🔗 <b>Ijtimoiy tarmoqdagi sahifalarimiz</b>\n👉 <a href='{SCHOOL_YOUTUBE_URL}'>Youtube</a> | <a href='{SCHOOL_INSTAGRAM_URL}'>Instagram</a> | <a href='{SCHOOL_TELEGRAM_URL}'>Telegram</a>")
    await message.answer(text)

@dp.message(F.text.in_(["📞 Связаться с нами", "📞 Biz bilan bog'lanish", "/contact"]))
async def contact_start(message: types.Message, state: FSMContext):
    await reset_state_keep_lang(state)
    lang = await get_lang(state)
    if lang == 'ru':
        await message.answer("<b>Введите свое имя, чтобы связаться с нами !</b>")
    else:
        await message.answer("<b>Biz bilan bog'lanish uchun ismingizni kiriting !</b>")
    await state.set_state(Contact.name)

@dp.message(F.text.in_(["💼 Работа", "💼 Ish bo'yicha", "/work"]))
async def work_start(message: types.Message, state: FSMContext):
    await reset_state_keep_lang(state)
    lang = await get_lang(state)
    if lang == 'ru':
        await message.answer("<b>Для подачи заявки на вакансию введите полное имя и фамилию !</b>")
    else:
        await message.answer("<b>Ish bo'yicha hujjat topshirish uchun ism familya to'liq kiriting !</b>")
    await state.set_state(Work.full_name)

@dp.message(F.text.in_(["📚 Прием в школу", "📚 Maktabga qabul"]))
async def admission_start(message: types.Message, state: FSMContext):
    await reset_state_keep_lang(state)
    lang = await get_lang(state)
    builder = InlineKeyboardBuilder()
    if lang == 'ru':
        regions = REGIONS_RU
        text = "В каком районе вы проживаете ?"
    else:
        regions = REGIONS_UZ
        text = "Qaysi tumanda istiqomat qilasiz ?"
    for r in regions:
        builder.button(text=r, callback_data=r)
    builder.adjust(1)
    await message.answer(text, reply_markup=builder.as_markup())
    await state.set_state(Admission.region)

@dp.message(Contact.name)
async def contact_name(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    if message.content_type == types.ContentType.TEXT:
        await state.update_data(name=message.text)
        if lang == 'ru':
            await message.answer("<b>Отправьте свой номер телефона, нажав на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Telefon raqamingizni quyidagi tugma orqali yuboring !</b>", reply_markup=get_contact_keyboard(lang))
        await state.set_state(Contact.phone)
    elif message.content_type == types.ContentType.PHOTO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте фото !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Rasm yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.LOCATION:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте локацию !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Lokatsiya yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.VIDEO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте видео !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Video yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.AUDIO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте аудио !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Audio yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.DOCUMENT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте документ !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Hujjat yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.CONTACT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте контакт !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Raqam yubormang !</b>", reply_markup=get_main_keyboard(lang))

@dp.message(Contact.phone)
async def contact_phone(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    if message.content_type == types.ContentType.CONTACT:
        phone_number = message.contact.phone_number
        await state.update_data(phone=phone_number)
        if lang == 'ru':
            await message.answer("<b>Введите ваше сообщение и наши сотрудники свяжутся с вами !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Xabaringizni kiriting, xodimlarimiz siz bilan bog'lanishadi !</b>", reply_markup=get_main_keyboard(lang))
        await state.set_state(Contact.message)
    elif message.content_type == types.ContentType.TEXT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте текст, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Matn yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))
    elif message.content_type == types.ContentType.PHOTO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте фото, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Rasm yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))
    elif message.content_type == types.ContentType.LOCATION:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте локацию, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Lokatsiya yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))
    elif message.content_type == types.ContentType.VIDEO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте видео, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Video yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))
    elif message.content_type == types.ContentType.AUDIO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте аудио, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Audio yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))
    elif message.content_type == types.ContentType.DOCUMENT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте документ, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Hujjat yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))

@dp.message(Contact.message)
async def contact_message_send(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    if message.content_type == types.ContentType.TEXT:
        data = await state.get_data()
        username = message.from_user.username
        tz = ZoneInfo("Asia/Tashkent")
        now = datetime.now(tz)
        current_date = now.strftime("%d.%m.%Y")
        current_time = now.strftime("%H:%M")
        if lang == "ru":
            send_contact = f"<b>Имя:</b> {data.get('name')}\n"
            if username:
                send_contact += f"<b>Профиль:</b> @{username}\n"
            send_contact += f"<b>Телефон:</b> {data.get('phone')}\n<b>Время:</b> {current_time}\n<b>Дата:</b> {current_date}"
            await bot.send_message(GROUP_CHAT_ID, f"{send_contact}\n{message.text}")
            await message.answer("<b>Ваше сообщение успешно отправлено, спасибо !</b>", reply_markup=get_main_keyboard(lang))
        else:
            send_contact = f"<b>Ismi:</b> {data.get('name')}\n"
            if username:
                send_contact += f"<b>Akkount:</b> @{username}\n"
            send_contact += f"<b>Telefon:</b> {data.get('phone')}\n<b>Vaqt:</b> {current_time}\n<b>Sana:</b> {current_date}"
            await bot.send_message(GROUP_CHAT_ID, f"{send_contact}\n{message.text}")
            await message.answer("<b>Xabaringiz muvaffaqiyatli yuborildi, rahmat !</b>", reply_markup=get_main_keyboard(lang))
        await reset_state_keep_lang(state)
    elif message.content_type == types.ContentType.PHOTO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте фото !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Rasm yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.LOCATION:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте локацию !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Lokatsiya yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.VIDEO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте видео !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Video yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.AUDIO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте аудио !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Audio yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.DOCUMENT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте документ !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Hujjat yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.CONTACT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте контакт !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Raqam yubormang !</b>", reply_markup=get_main_keyboard(lang))

@dp.message(Work.full_name)
async def work_full_name(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    if message.content_type == types.ContentType.TEXT:
        await state.update_data(full_name=message.text)
        if lang == 'ru':
            await message.answer("<b>Отправьте свой номер телефона, нажав на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Telefon raqamingizni quyidagi tugma orqali yuboring !</b>", reply_markup=get_contact_keyboard(lang))
        await state.set_state(Work.phone)
    elif message.content_type == types.ContentType.PHOTO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте фото !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Rasm yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.LOCATION:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте локацию !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Lokatsiya yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.VIDEO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте видео !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Video yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.AUDIO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте аудио !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Audio yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.DOCUMENT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте документ !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Hujjat yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.CONTACT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте контакт !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Raqam yubormang !</b>", reply_markup=get_main_keyboard(lang))

@dp.message(Work.phone)
async def work_phone(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    if message.content_type == types.ContentType.CONTACT:
        phone_number = message.contact.phone_number
        await state.update_data(phone=phone_number)
        if lang == 'ru':
            await message.answer("<b>Загрузите свое резюме !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Rezyumeni yuklang !</b>", reply_markup=get_main_keyboard(lang))
        await state.set_state(Work.cv)
    elif message.content_type == types.ContentType.TEXT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте текст, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Matn yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))
    elif message.content_type == types.ContentType.PHOTO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте фото, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Rasm yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))
    elif message.content_type == types.ContentType.LOCATION:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте локацию, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Lokatsiya yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))
    elif message.content_type == types.ContentType.VIDEO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте видео, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Video yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))
    elif message.content_type == types.ContentType.AUDIO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте аудио, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Audio yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))
    elif message.content_type == types.ContentType.DOCUMENT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте документ, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Hujjat yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))

@dp.message(Work.cv)
async def work_cv_document(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    if message.content_type == types.ContentType.DOCUMENT:
        mime_type = message.document.mime_type.lower() if message.document.mime_type else ""
        if mime_type not in ALLOWED_MIME_TYPES:
            if lang == 'ru':
                await message.answer("<b>Файл в этом формате не принимаются ❌ \n\nПринимаются файл в формате pdf, doc, docx, jpg, jpeg, png ✅</b>")
            else:
                await message.answer("<b>Bunday formatdagi fayllar qabul qilinmaydi ❌ \n\npdf, doc, docx, jpg, jpeg, png formatdagi fayllar qabul qilinadi ✅</b>")
            return
        data = await state.get_data()
        username = message.from_user.username
        tz = ZoneInfo("Asia/Tashkent")
        now = datetime.now(tz)
        current_date = now.strftime("%d.%m.%Y")
        current_time = now.strftime("%H:%M")
        if lang == "ru":
            send_contact = f"<b>Податель документа:</b> {data.get('full_name')}\n"
            if username:
                send_contact += f"<b>Профиль:</b> @{username}\n"
            send_contact += f"<b>Телефон:</b> {data.get('phone')}\n<b>Время отправки документа:</b> {current_time}\n<b>Дата отправки документа:</b> {current_date}"
            await bot.send_document(GROUP_CHAT_ID, document=message.document.file_id, caption=f"<b>{send_contact}</b>")
            await message.answer("<b>Документ успешно отправлен, спасибо !</b>", reply_markup=get_main_keyboard(lang))
        else:
            send_contact = f"<b>Hujjat topshiruvchi:</b> {data.get('full_name')}\n"
            if username:
                send_contact += f"<b>Akkount:</b> @{username}\n"
            send_contact += f"<b>Telefon:</b> {data.get('phone')}\n<b>Hujjat yuborilgan vaqt:</b> {current_time}\n<b>Hujjat yuborilgan sana:</b> {current_date}"
            await bot.send_document(GROUP_CHAT_ID, document=message.document.file_id, caption=f"<b>{send_contact}</b>")
            await message.answer("<b>Hujjat muvaffaqiyatli yuborildi, rahmat !</b>", reply_markup=get_main_keyboard(lang))
        await reset_state_keep_lang(state)
    elif message.content_type == types.ContentType.PHOTO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте фото !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Rasm yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.LOCATION:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте локацию !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Lokatsiya yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.VIDEO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте видео !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Video yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.AUDIO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте аудио !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Audio yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.CONTACT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте контакт !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Raqam yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.TEXT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте текст !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Matn yubormang !</b>", reply_markup=get_contact_keyboard(lang))

@dp.callback_query(Admission.region)
async def admission_region_cb(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(region=callback.data)
    lang = await get_lang(state)
    builder = InlineKeyboardBuilder()
    if lang == 'ru':
        builder.button(text="Начальный класс", callback_data="Начальный класс")
        builder.button(text="Старшие классы", callback_data="Старшие классы")
        text = "В какой класс переходит ваш ребенок?"
    else:
        builder.button(text="Boshlang’ich sinf", callback_data="Boshlang’ich sinf")
        builder.button(text="Yuqori sinf", callback_data="Yuqori sinf")
        text = "Farzandingiz qaysi sinfga oʻtkazmoqchisz ?"
    builder.adjust(1)
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await state.set_state(Admission.classes)

@dp.callback_query(Admission.classes)
async def admission_classes_cb(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(classes=callback.data)
    lang = await get_lang(state)
    if lang == 'ru':
        await callback.message.answer("<b>Для приема введите полное имя и фамилию !</b>")
    else:
        await callback.message.answer("<b>Qabul uchun ism familya to'liq kiriting !</b>")
    await state.set_state(Admission.full_name)

@dp.message(Admission.full_name)
async def admission_full_name(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    if message.content_type == types.ContentType.TEXT:
        await state.update_data(full_name=message.text)
        if lang == 'ru':
            await message.answer("<b>Отправьте свой номер телефона, нажав на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Telefon raqamingizni quyidagi tugma orqali yuboring !</b>", reply_markup=get_contact_keyboard(lang))
        await state.set_state(Admission.phone)
    elif message.content_type == types.ContentType.PHOTO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте фото !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Rasm yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.LOCATION:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте локацию !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Lokatsiya yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.VIDEO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте видео !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Video yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.AUDIO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте аудио !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Audio yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.DOCUMENT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте документ !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Hujjat yubormang !</b>", reply_markup=get_main_keyboard(lang))
    elif message.content_type == types.ContentType.CONTACT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте контакт !</b>", reply_markup=get_main_keyboard(lang))
        else:
            await message.answer("<b>Raqam yubormang !</b>", reply_markup=get_main_keyboard(lang))

@dp.message(Admission.phone)
async def admission_phone(message: types.Message, state: FSMContext):
    lang = await get_lang(state)
    if message.content_type == types.ContentType.CONTACT:
        tz = ZoneInfo("Asia/Tashkent")
        now = datetime.now(tz)
        current_date = now.strftime("%d.%m.%Y")
        current_time = now.strftime("%H:%M")
        phone_number = message.contact.phone_number
        await state.update_data(phone=phone_number)
        data = await state.get_data()
        username = message.from_user.username
        if lang == 'ru':
            send_text = f"<b>Заявитель:</b> {data['full_name']}\n"
            if username:
                send_text += f"<b>Профиль:</b> @{username}\n"
            send_text += f"<b>Телефон:</b> {data['phone']}\n<b>Регион:</b> {data['region']}\n<b>Выбранный класс:</b> {data['classes']}\n<b>Время заявки:</b> {current_time}\n<b>Дата оставления заявки:</b> {current_date}"
            await bot.send_message(GROUP_CHAT_ID, f"<b>{send_text}</b>")
            await message.answer("<b>Ваша заявка успешно отправлена, спасибо !</b>", reply_markup=get_main_keyboard(lang))
        else:
            send_text = f"<b>Arizachi:</b> {data['full_name']}\n"
            if username:
                send_text += f"<b>Akkount:</b> @{username}\n"
            send_text += f"<b>Telefon:</b>{data['phone']}\n<b>Tanlagan hudud:</b> {data['region']}\n<b>Tanlagan sinf:</b> {data['classes']}\n<b>Ariza vaqti:</b> {current_time}\n<b>Ariza qoldirilgan sana:</b> {current_date}"
            await bot.send_message(GROUP_CHAT_ID, f"<b>{send_text}</b>")
            await message.answer("<b>Qabul uchun arizangiz muvaffaqiyatli yuborildi, rahmat !</b>", reply_markup=get_main_keyboard(lang))
        await reset_state_keep_lang(state)
    elif message.content_type == types.ContentType.TEXT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте текст, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Matn yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))
    elif message.content_type == types.ContentType.PHOTO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте фото, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Rasm yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))
    elif message.content_type == types.ContentType.LOCATION:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте локацию, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Lokatsiya yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))
    elif message.content_type == types.ContentType.VIDEO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте видео, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Video yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))
    elif message.content_type == types.ContentType.AUDIO:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте аудио, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Audio yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))
    elif message.content_type == types.ContentType.DOCUMENT:
        if lang == 'ru':
            await message.answer("<b>Не отправляйте документ, нажмите на кнопку ниже !</b>", reply_markup=get_contact_keyboard(lang))
        else:
            await message.answer("<b>Hujjat yubormang, quyidagi tugmani bosing !</b>", reply_markup=get_contact_keyboard(lang))

async def main():
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())