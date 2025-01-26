import datetime
import platform
import re

from ollama import chat
from ollama import ChatResponse
import dateparser


def find_datetime(string):
    parsed_datetime = dateparser.parse(string)

    if parsed_datetime:
        return parsed_datetime

    match = re.search(r"([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]", string)
    if match:
        time_str = match.group(0)
        hour, minute = map(int, time_str.split(":"))

        return datetime.datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
    return None


if platform.system() == 'Linux':
    STRAPI_BASE_URL = 'http://localhost:1338/api'
else:
    STRAPI_BASE_URL = 'https://opendata.bounceme.net:444/api'

print(STRAPI_BASE_URL)


def model_ask(prompt):
    response: ChatResponse = chat(model='llama3.2', messages=[
        {
            'role': 'system',
            'content': 'Classify a message from social network if it is an event and export data from there (ONLY date, time, location, organization name and price (if available)). Message may be in russian or english.',
        },
        {
            'role': 'user',
            'content': '''Узнайте, что нового в AWS — приходите на встречу 30 января!
  Когда и где?
  30 января в 19:00 ждем вас в Алматы, на ул. Ходжанова 2/2, в MOST IT Hub (8 этаж). Вход бесплатный
  Что будет?
  Обсудим главные новинки и тренды в IT с крупнейшей мировой конференции AWS re:Invent 2024. Даже если вы не слышали про AWS, это отличный шанс разобраться, куда движется мир технологий.
  Мы поговорим про:
  ️Искусственный интеллект и машинное обучение (AI/ML), включая перспективы Generative AI.
  ️Новые подходы к работе с данными.
  ️Современные инструменты для разработчиков и автоматизации (DevOps) и многое другое,
  а главное НЕТВОРКИНГ
  ️познакомитесь с профессионалами IT-сообщества и получите инсайты из первых рук от ведущих экспертов.
  Кто выступит?
  Антон Коваленко — эксперт с 20-летним опытом в IT, архитектор масштабных инфраструктур и приложений. Senior Solutions Architect в Amazon Web Services.
  Александр Бернадский — специалист по облачным технологиям с 15-летним стажем, помогает компаниям Казахстана внедрять эффективные IT-решения. Solutions Architect, Amazon Web Services (AWS)
  Приветственное слово:
  Алмас Молдаканов,
  региональный менеджер AWS в Казахстане и СНГ.
  Нурбек Садыков,
  AWS Community Leader, CEO qCloudy
  Регистрация по ссылке (<URL>). Кол-во мест ограничено️
  @cloudnativekz ''',
        },
        {
            'role': 'assistant',
            'content': '''Date and Time: 30 января 2025, 19:00
Location: MOST IT HUB Almaty
Format: offline
Summary: Встреча на тему: "Что такое AWS" в MOST IT Hub Almaty'''},
        {
            'role': 'user',
            'content': '''UEnter и ЕБРР проведут круглый стол по обсуждению стартап экосистемы.
  В рамках мероприятия предусматривается обсуждение текущего состояния и перспектив развития стартап-экосистемы в Узбекистане, а также программ ЕБРР по техническому содействию стартап проектов.
  Круглый стол предназначен для представителей стартап-сообщества, венчурных инвесторов, а также для организаций, занятых в области развития стартап экосистемы в Узбекистане.
  Ознакомиться (<URL>) с программой.
  Заинтересованные принять участие в качестве слушателей могут зарегистрироваться на мероприятие по ссылке (<URL>).
  Дата: 15 января 2025г.
  Время: 09:00-12:30
  Язык: английский
  Локация: UEnter (<URL>)
  @uenteruz
  Telegram (<URL>) | Instagram (<URL>) | Facebook (<URL>) | (<URL>) Website (<URL>) '''},

        {'role': 'assistant',
         'content': '''Date and Time: 15 января 2025, 09:00
Location: UEnter
Format: offline
Summary: Круглый стол по обсуждению стартап экосистемы в UEnter'''},
        {'role': 'user',
         'content': prompt}
    ])
    return response.message.content
