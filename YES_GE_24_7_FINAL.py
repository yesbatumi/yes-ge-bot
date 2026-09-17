"""
Yes GE 24/7 - ФИНАЛЬНАЯ ВЕРСИЯ
Работает 100%, без скачивания картинок с интернета
Постит 3 раза в день сам: 10:30 / 14:00 / 18:30 по Тбилиси

1-й пост сразу при запуске = Trump Tower
"""

import requests, os, time, random
from datetime import datetime
import pytz

TOKEN = "8908028465:AAG4x3T3eMumyxW9sK6QVYao9VM5FjnyoAc"
CHANNEL_ID = "@yes_ge"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# 3 поста которые будут ротироваться каждый день
POSTS = [
# ПОСТ 1 - Trump Tower главное
"""<b>🇬🇪 TRUMP TOWER TBILISI — 6 башен в парке Сабуртало</b>

Официальный сайт trump-tower-tbilisi.com: 6 небоскребов, центральная 70 этажей — самое высокое здание Грузии. 600,000 м², 1600 квартир от студий до 4-комнатных с панорамными террасами.

📅 Сдача — июнь 2029
📍 Saburtalo Park, до Downtown 600 метров

4 блока: A-отель, B-апарт-отель, C-инвест-квартиры, D-коммерция. Премиум-отделка и полностью меблированные, уровень Four Seasons.

Инфраструктура: infinity-бассейн на крыше, indoor-бассейн, rooftop-рестораны, SPA, фитнес, кинотеатр, коворкинг, шопинг, паркинг.

Archi Group + Biograpi Living, Gensler, Sapir Organization ($7 млрд). Pre-sale открыт.

#TrumpTowerTbilisi #Тбилиси

━━━━━━━━━━━
Нужна помощь с подбором недвижимости? → @Marialvestate""",

# ПОСТ 2 - Что внутри
"""<b>🏗️ Что внутри Trump Tower Tbilisi — разбор</b>

Застройщики Archi (18% рынка, 55 проектов) + Biograpi Living. Архитектор — Gensler, крупнейшее бюро мира. Партнер — Sapir Organization, портфель $7 млрд в Нью-Йорке.

<b>Что внутри вертикального города:</b>
🏊 Infinity на крыше + indoor-бассейн
🍽️ Rooftop-рестораны с панорамой
🧘 Premium SPA и фитнес с видом
🎬 Кинотеатр, конференц, коворкинг
🛍️ Шопинг-центр, детский клуб, паркинг
👔 Управляющая компания

1600 квартир, отделка Four Seasons / Ritz-Carlton, меблированные. Сдача июнь 2029.

Сабуртало — престижный район, граничит с заповедником, в стороне от шума центра.

#Archi #НедвижимостьГрузии

━━━━━━━━━━━
Нужна помощь с подбором недвижимости? → @Marialvestate""",

# ПОСТ 3 - Инвестиции
"""<b>💰 TRUMP TOWER — $2 млрд, самый дорогой проект Грузии</b>

Вчера прошла международная презентация. Премьер Кобахидзе: «исторический день».

💵 $2 млрд инвестиций
📏 280м, 70 этажей — самое высокое в Грузии
🏢 600,000 м² в центре
👔 Eric Trump: «лучшее здание в Европе и Азии»

Первый брендированный проект Trump в регионе. Входит в глобальную сеть Trump Organization. Тысячи рабочих мест и контракты для стройки на годы.

Сдача башни 2031, всего Downtown Tbilisi — 2033. Инвесторы уже в pre-sale.

#TrumpTower #ИнвестицииГрузия #Тбилиси

━━━━━━━━━━━
Нужна помощь с подбором недвижимости? → @Marialvestate"""
]

def send_text(text):
    url = f"{BASE_URL}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "HTML"}, timeout=20)
        print(f"[{datetime.now()}] TEXT {r.status_code} -> {r.text[:200]}")
        return r.json().get("ok", False)
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return False

def send_with_local_photo(text):
    # Ищем любую картинку в папке
    for f in os.listdir("."):
        if f.lower().endswith((".webp",".jpg",".jpeg",".png")):
            try:
                print(f"Отправляю с фото {f}...")
                with open(f, 'rb') as photo:
                    r = requests.post(f"{BASE_URL}/sendPhoto", files={'photo': photo}, data={"chat_id": CHANNEL_ID, "caption": text, "parse_mode": "HTML"}, timeout=30)
                    print(f"PHOTO {r.status_code}")
                    if r.json().get("ok"):
                        return True
            except Exception as e:
                print(f"Фото ошибка {e}")
    # Если фото нет или не получилось - текстом
    return send_text(text)

def post_one():
    post = random.choice(POSTS)
    return send_with_local_photo(post)

def run():
    tz = pytz.timezone("Asia/Tbilisi")
    posted = set()
    print("🤖 Yes GE бот запущен 24/7")
    print("Расписание: 10:30, 14:00, 18:30 по Тбилиси")
    print("Сразу постю Trump Tower...")
    post_one()

    while True:
        now = datetime.now(tz)
        cur = now.strftime("%H:%M")
        today = now.strftime("%Y-%m-%d")
        key = f"{today}_{cur}"

        if cur in ["10:30", "14:00", "18:30"] and key not in posted:
            print(f"\n⏰ Время {cur} - постю...")
            post_one()
            posted.add(key)
            # чистим старые
            posted = {k for k in posted if k.startswith(today)}
        
        time.sleep(50)

if __name__ == "__main__":
    run()
