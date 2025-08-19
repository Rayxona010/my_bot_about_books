import logging
import random
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from config import TOKEN


BOOKS_DB = {
    "falsafiy": [
        {
            "title": "Yashamoq",
            "author": "Kazuo Ishiguro",
            "description": "Inson hayoti va sevgi haqida chuqur hikoya.",
        },
        {
            "title": "Yo'lda",
            "author": "Jack Kerouac",
            "description": "Erkinlik va sayohat ruhidagi roman.",
        },
        {
            "title": "Sofist",
            "author": "Platon",
            "description": "Falsafiy munozaralar kitobi.",
        },
        {
            "title": "Zamonaviy Falsafa",
            "author": "Bertrand Russell",
            "description": "Falsafa tarixi haqida.",
        },
        {
            "title": "O'zlik",
            "author": "Soren Kierkegaard",
            "description": "Ekzistensializm haqida chuqur asar.",
        },
        {
            "title": "Meditatsiyalar",
            "author": "Marcus Aurelius",
            "description": "Stoik falsafa asari.",
        },
        {
            "title": "Bunday dedi Zardusht",
            "author": "Nietzsche",
            "description": "Falsafiy roman.",
        },
        {
            "title": "Dunyo sifatida tasavvur",
            "author": "Schopenhauer",
            "description": "Metafizika haqida.",
        },
        {
            "title": "Falsafiy tadqiqotlar",
            "author": "Wittgenstein",
            "description": "Til falsafasi haqida.",
        },
        {
            "title": "Inson va tabiat",
            "author": "Kant",
            "description": "Axloqiy falsafa asari.",
        },
    ],
    "fantaziya": [
        {
            "title": "Uzuklar Egasi",
            "author": "J.R.R. Tolkien",
            "description": "Epik fantastik sarguzasht.",
        },
        {
            "title": "Harry Potter va Falsafiy Tosh",
            "author": "J.K. Rowling",
            "description": "Sehrli dunyodagi sarguzasht.",
        },
        {
            "title": "Narniya Xronikalari",
            "author": "C.S. Lewis",
            "description": "Fantastik olam hikoyasi.",
        },
        {
            "title": "Qorong'u Minorasi",
            "author": "Stephen King",
            "description": "Fantastik va sirli hikoya.",
        },
        {
            "title": "Yer Dengizi",
            "author": "Ursula K. Le Guin",
            "description": "Sehrli orollar haqida.",
        },
        {
            "title": "Muz va Olov Qo'shig'i",
            "author": "George R.R. Martin",
            "description": "Epik fantaziya.",
        },
        {
            "title": "Tumanlarda Tug'ilgan",
            "author": "Brandon Sanderson",
            "description": "Sehr va sarguzasht.",
        },
        {
            "title": "Hobbit",
            "author": "J.R.R. Tolkien",
            "description": "Hobbitning sayohati.",
        },
        {
            "title": "Bo'ronnoma",
            "author": "Brandon Sanderson",
            "description": "Epik fantastik hikoya.",
        },
        {
            "title": "Vaqt G'ildiragi",
            "author": "Robert Jordan",
            "description": "Fantastik dunyo.",
        },
    ],
    "ilmiy_fantastika": [
        {
            "title": "Dune",
            "author": "Frank Herbert",
            "description": "Cho'l sayyorasidagi epik hikoya.",
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "description": "Totalitar jamiyat tasviri.",
        },
        {
            "title": "Fahrenheit 451",
            "author": "Ray Bradbury",
            "description": "Kitoblar yoqilgan dunyo.",
        },
        {
            "title": "Neyromanser",
            "author": "William Gibson",
            "description": "Kiberpank hikoyasi.",
        },
        {
            "title": "Marslik",
            "author": "Andy Weir",
            "description": "Marsdagi omon qolish.",
        },
        {
            "title": "Asos",
            "author": "Isaac Asimov",
            "description": "Galaktik imperiya hikoyasi.",
        },
        {
            "title": "Enderning O'yini",
            "author": "Orson Scott Card",
            "description": "Kosmik urush haqida.",
        },
        {
            "title": "Jasur Yangi Dunyo",
            "author": "Aldous Huxley",
            "description": "Distopik kelajak.",
        },
        {
            "title": "Qor To'foni",
            "author": "Neal Stephenson",
            "description": "Virtual haqiqat hikoyasi.",
        },
        {
            "title": "Hiperion",
            "author": "Dan Simmons",
            "description": "Ilmiy fantastik epos.",
        },
    ],
    "romantika": [
        {
            "title": "G'urur va Xurofot",
            "author": "Jane Austen",
            "description": "Sevgi va ijtimoiy sinflar haqida.",
        },
        {
            "title": "Romeo va Juletta",
            "author": "William Shakespeare",
            "description": "Fojiali sevgi hikoyasi.",
        },
        {
            "title": "Jeyn Eyr",
            "author": "Charlotte Bronte",
            "description": "Romantik va hayotiy hikoya.",
        },
        {
            "title": "Yovvoyi Cho'l",
            "author": "Emily Bronte",
            "description": "Qayg'uli sevgi hikoyasi.",
        },
        {
            "title": "Daftar",
            "author": "Nicholas Sparks",
            "description": "Zamonaviy sevgi hikoyasi.",
        },
        {
            "title": "Sevgi Hikoyasi",
            "author": "Erich Segal",
            "description": "Sevgi va yo'qotish.",
        },
        {
            "title": "Sendan Oldin Men",
            "author": "Jojo Moyes",
            "description": "Fojiali romantika.",
        },
        {
            "title": "P.S. Seni Sevaman",
            "author": "Cecelia Ahern",
            "description": "Sevgi xatlari hikoyasi.",
        },
        {
            "title": "Chet Eldagi",
            "author": "Diana Gabaldon",
            "description": "Tarixiy romantika.",
        },
        {
            "title": "Yulduzlarimizdagi Ayb",
            "author": "John Green",
            "description": "Yosh sevgi hikoyasi.",
        },
    ],
    "detektiv": [
        {
            "title": "Sherlock Holmes Sarguzashtlari",
            "author": "Arthur Conan Doyle",
            "description": "Sirli jinoyatlar.",
        },
        {
            "title": "Sharqdagi Qotillik",
            "author": "Agatha Christie",
            "description": "Detektiv hikoya.",
        },
        {
            "title": "Ajdahodagi Qiz",
            "author": "Stieg Larsson",
            "description": "Zamonaviy detektiv.",
        },
        {
            "title": "Yo'qolgan Qiz",
            "author": "Gillian Flynn",
            "description": "Psixologik triller.",
        },
        {
            "title": "Da Vinchi Kodi",
            "author": "Dan Brown",
            "description": "Sirli sarguzasht.",
        },
        {
            "title": "Katta Uyqu",
            "author": "Raymond Chandler",
            "description": "Qattiq detektiv hikoyasi.",
        },
        {
            "title": "O'rmonda",
            "author": "Tana French",
            "description": "Sirli qotillik.",
        },
        {
            "title": "Kukuning Chaqiriqi",
            "author": "J.K. Rowling",
            "description": "Zamonaviy detektiv.",
        },
        {
            "title": "Malta Lochini",
            "author": "Dashiell Hammett",
            "description": "Klassik detektiv.",
        },
        {
            "title": "Baskervill Iti",
            "author": "Arthur Conan Doyle",
            "description": "Sherlockning sarguzashti.",
        },
    ],
    "tarixiy": [
        {
            "title": "Sapiens",
            "author": "Yuval Noah Harari",
            "description": "Insoniyat tarixi haqida.",
        },
        {
            "title": "Urush va Tinchlik",
            "author": "Leo Tolstoy",
            "description": "Tarixiy epos.",
        },
        {
            "title": "Yer Ustunlari",
            "author": "Ken Follett",
            "description": "O'rta asrlar hikoyasi.",
        },
        {
            "title": "Ikki Shahar Hikoyasi",
            "author": "Charles Dickens",
            "description": "Fransuz inqilobi.",
        },
        {
            "title": "Kitob O'g'risi",
            "author": "Markus Zusak",
            "description": "Ikkinchi jahon urushi.",
        },
        {
            "title": "Ko'rinmaydigan Nur",
            "author": "Anthony Doerr",
            "description": "Urush davri hikoyasi.",
        },
        {
            "title": "Geysha Xotiralari",
            "author": "Arthur Golden",
            "description": "Yaponiya tarixi.",
        },
        {
            "title": "Men, Klavdiy",
            "author": "Robert Graves",
            "description": "Rim imperiyasi.",
        },
        {
            "title": "Atirgul Nomi",
            "author": "Umberto Eco",
            "description": "O'rta asr sirlari.",
        },
        {
            "title": "Shogun",
            "author": "James Clavell",
            "description": "Yaponiya feodalizmi.",
        },
    ],
    "sarguzasht": [
        {
            "title": "Alkimyogar",
            "author": "Paulo Coelho",
            "description": "Orzu izlash hikoyasi.",
        },
        {
            "title": "Xazina Orol",
            "author": "Robert Louis Stevenson",
            "description": "Xazina ovchilari.",
        },
        {
            "title": "Monte-Kristo Grafi",
            "author": "Alexandre Dumas",
            "description": "Qasos hikoyasi.",
        },
        {
            "title": "Yer Markaziga Sayohat",
            "author": "Jules Verne",
            "description": "Ilmiy sarguzasht.",
        },
        {"title": "Odisseya", "author": "Homer", "description": "Qadimiy sarguzasht."},
        {
            "title": "Mobi-Dik",
            "author": "Herman Melville",
            "description": "Dengiz sarguzashti.",
        },
        {
            "title": "Saksonda Dunyo Bo'ylab",
            "author": "Jules Verne",
            "description": "Sayohat hikoyasi.",
        },
        {
            "title": "Uch Mushketyor",
            "author": "Alexandre Dumas",
            "description": "Do'stlik va jang.",
        },
        {
            "title": "Pi Hayoti",
            "author": "Yann Martel",
            "description": "Omon qolish hikoyasi.",
        },
        {
            "title": "Yovvoyi Chaqiriq",
            "author": "Jack London",
            "description": "Tabiatdagi hayot.",
        },
    ],
    "qorqinchli": [
        {
            "title": "Drakula",
            "author": "Bram Stoker",
            "description": "Vampir hikoyasi.",
        },
        {
            "title": "Yorqinlik",
            "author": "Stephen King",
            "description": "Qo'rqinchli mehmonxona.",
        },
        {
            "title": "Frankenshteyn",
            "author": "Mary Shelley",
            "description": "Yirtik hayvon hikoyasi.",
        },
        {
            "title": "Bu",
            "author": "Stephen King",
            "description": "Qo'rqinchli masxaraboz.",
        },
        {
            "title": "Jin Oyini",
            "author": "William Peter Blatty",
            "description": "Jin urgan qiz.",
        },
        {
            "title": "Hayvon Qabristoni",
            "author": "Stephen King",
            "description": "Qabriston sirlari.",
        },
        {
            "title": "Rozmarining Chaqalog'i",
            "author": "Ira Levin",
            "description": "Shaytoniy bolalik.",
        },
        {
            "title": "Salemning Qismi",
            "author": "Stephen King",
            "description": "Vampirlar shahri.",
        },
        {
            "title": "Tepalik Uyi Arvohlari",
            "author": "Shirley Jackson",
            "description": "Arvohlar uyi.",
        },
        {
            "title": "Doktor Jekyll va Mister Hyde",
            "author": "Robert Louis Stevenson",
            "description": "Ikki shaxsiyat.",
        },
    ],
    "ozini_ozi_rivojlantirish": [
        {
            "title": "Hozirning Kuchi",
            "author": "Eckhart Tolle",
            "description": "Hozirda yashash haqida.",
        },
        {
            "title": "Atomik Odatlar",
            "author": "James Clear",
            "description": "Odatlar shakllantirish.",
        },
        {
            "title": "7 Odat",
            "author": "Stephen Covey",
            "description": "Muvaffaqiyat odatlari.",
        },
        {
            "title": "Tez va Sekin Fikrlash",
            "author": "Daniel Kahneman",
            "description": "Fikrlash turlari.",
        },
        {
            "title": "Hayot Ma'nosini Izlash",
            "author": "Viktor Frankl",
            "description": "Hayot ma'nosi.",
        },
        {
            "title": "Odatlarning Kuchi",
            "author": "Charles Duhigg",
            "description": "Odatlar kuchi.",
        },
        {
            "title": "Katta Jasorat",
            "author": "Brené Brown",
            "description": "Jasorat va zaiflik.",
        },
        {
            "title": "Fikrlash Tarzi",
            "author": "Carol Dweck",
            "description": "Fikrlash tarzi haqida.",
        },
        {
            "title": "To'rt Kelishuv",
            "author": "Don Miguel Ruiz",
            "description": "Hayot qoidalari.",
        },
        {
            "title": "Qat'iyat",
            "author": "Angela Duckworth",
            "description": "Qat'iyat kuchi.",
        },
    ],
    "klassik": [
        {
            "title": "Jinoyat va Jazo",
            "author": "Fyodor Dostoevsky",
            "description": "Axloqiy dilemma.",
        },
        {
            "title": "G'urur va Xurofot",
            "author": "Jane Austen",
            "description": "Ijtimoiy sevgi.",
        },
        {
            "title": "Buyuk Getsbi",
            "author": "F. Scott Fitzgerald",
            "description": "Amerika orzusi.",
        },
        {
            "title": "Mobi-Dik",
            "author": "Herman Melville",
            "description": "Dengiz sarguzashti.",
        },
        {
            "title": "Urush va Tinchlik",
            "author": "Leo Tolstoy",
            "description": "Tarixiy epos.",
        },
        {
            "title": "Anna Karenina",
            "author": "Leo Tolstoy",
            "description": "Fojiali sevgi.",
        },
        {
            "title": "Karamazov Birodarlar",
            "author": "Fyodor Dostoevsky",
            "description": "Falsafiy roman.",
        },
        {
            "title": "Bechora Odamlar",
            "author": "Victor Hugo",
            "description": "Adolat uchun kurash.",
        },
        {
            "title": "Qushni O'ldirmang",
            "author": "Harper Lee",
            "description": "Adolat va tenglik.",
        },
        {
            "title": "Jeyn Eyr",
            "author": "Charlotte Bronte",
            "description": "Romantik hikoya.",
        },
    ],
}


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    buttons = [
        [KeyboardButton(text="Falsafiy"), KeyboardButton(text="Fantaziya")],
        [KeyboardButton(text="Ilmiy Fantastika"), KeyboardButton(text="Romantika")],
        [KeyboardButton(text="Detektiv"), KeyboardButton(text="Tarixiy")],
        [KeyboardButton(text="Sarguzasht"), KeyboardButton(text="Qo'rqinchli")],
        [
            KeyboardButton(text="O'zini-o'zi rivojlantirish"),
            KeyboardButton(text="Klassik"),
        ],
    ]
    klaviatura = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer(
        "Assalomu alaykum! Hurmatli foydalanuvchi botimizga xush kelibsiz🤗.   O'zingizga kerakli tugmalarni bosing va foydali ma'lumot oling. Buning uchun  janrni tanlang:",
        reply_markup=klaviatura,
    )


@dp.message(Command("genres"))
async def cmd_genres(message: Message):
    buttons = [
        [KeyboardButton(text="Falsafiy"), KeyboardButton(text="Fantaziya")],
        [KeyboardButton(text="Ilmiy Fantastika"), KeyboardButton(text="Romantika")],
        [KeyboardButton(text="Detektiv"), KeyboardButton(text="Tarixiy")],
        [KeyboardButton(text="Sarguzasht"), KeyboardButton(text="Qo'rqinchli")],
        [
            KeyboardButton(text="O'zini-o'zi rivojlantirish"),
            KeyboardButton(text="Klassik"),
        ],
    ]
    klaviatura = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("Janrni tanlang:", reply_markup=klaviatura)


@dp.message(Command("books"))
async def cmd_books(message: Message):
    buttons = [
        [InlineKeyboardButton(text="Yashamoq", callback_data="book_yashamoq")],
        [
            InlineKeyboardButton(
                text="Uzuklar Egasi", callback_data="book_uzuklar_egasi"
            )
        ],
        [
            InlineKeyboardButton(
                text="Harry Potter va Falsafiy Tosh", callback_data="book_harry_potter"
            )
        ],
        [InlineKeyboardButton(text="Dune", callback_data="book_dune")],
        [InlineKeyboardButton(text="1984", callback_data="book_1984")],
        [
            InlineKeyboardButton(
                text="G'urur va Xurofot", callback_data="book_gurur_va_xurofot"
            )
        ],
        [
            InlineKeyboardButton(
                text="Sherlock Holmes Sarguzashtlari",
                callback_data="book_sherlock_holmes",
            )
        ],
        [InlineKeyboardButton(text="Sapiens", callback_data="book_sapiens")],
        [InlineKeyboardButton(text="Alkimyogar", callback_data="book_alkimyogar")],
        [InlineKeyboardButton(text="Drakula", callback_data="book_drakula")],
    ]
    klaviatura = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Kitob tanlang:", reply_markup=klaviatura)


@dp.message(Command("authors"))
async def cmd_authors(message: Message):
    buttons = [
        [InlineKeyboardButton(text="Kazuo Ishiguro", callback_data="author_ishiguro")],
        [InlineKeyboardButton(text="J.R.R. Tolkien", callback_data="author_tolkien")],
        [InlineKeyboardButton(text="J.K. Rowling", callback_data="author_rowling")],
        [InlineKeyboardButton(text="Frank Herbert", callback_data="author_herbert")],
        [InlineKeyboardButton(text="George Orwell", callback_data="author_orwell")],
        [InlineKeyboardButton(text="Jane Austen", callback_data="author_austen")],
        [InlineKeyboardButton(text="Arthur Conan Doyle", callback_data="author_doyle")],
        [InlineKeyboardButton(text="Yuval Noah Harari", callback_data="author_harari")],
        [InlineKeyboardButton(text="Paulo Coelho", callback_data="author_coelho")],
        [InlineKeyboardButton(text="Bram Stoker", callback_data="author_stoker")],
    ]
    klaviatura = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Muallif tanlang:", reply_markup=klaviatura)


@dp.message(Command("recommend"))
async def cmd_recommend(message: Message):
    buttons = [
        [InlineKeyboardButton(text="Falsafiy", callback_data="genre_falsafiy")],
        [InlineKeyboardButton(text="Fantaziya", callback_data="genre_fantaziya")],
        [
            InlineKeyboardButton(
                text="Ilmiy Fantastika", callback_data="genre_ilmiy_fantastika"
            )
        ],
        [InlineKeyboardButton(text="Romantika", callback_data="genre_romantika")],
        [InlineKeyboardButton(text="Detektiv", callback_data="genre_detektiv")],
        [InlineKeyboardButton(text="Tarixiy", callback_data="genre_tarixiy")],
        [InlineKeyboardButton(text="Sarguzasht", callback_data="genre_sarguzasht")],
        [InlineKeyboardButton(text="Qo'rqinchli", callback_data="genre_qorqinchli")],
        [
            InlineKeyboardButton(
                text="O'zini-o'zi rivojlantirish",
                callback_data="genre_ozini_ozi_rivojlantirish",
            )
        ],
        [InlineKeyboardButton(text="Klassik", callback_data="genre_klassik")],
    ]
    klaviatura = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Janrdan kitob tavsiya qilaymi?", reply_markup=klaviatura)


@dp.message(
    F.text.in_(
        [
            "Falsafiy",
            "Fantaziya",
            "Ilmiy Fantastika",
            "Romantika",
            "Detektiv",
            "Tarixiy",
            "Sarguzasht",
            "Qo'rqinchli",
            "O'zini-o'zi rivojlantirish",
            "Klassik",
        ]
    )
)
@dp.message(Command("all_genres"))
async def all_genres(message: Message):
    buttons = []
    janrlar = [
        "Falsafiy",
        "Fantaziya",
        "Ilmiy Fantastika",
        "Romantika",
        "Detektiv",
        "Tarixiy",
        "Sarguzasht",
        "Qo'rqinchli",
        "O'zini-ozi rivojlantirish",
        "Klassik",
    ]
    for janr in janrlar:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=janr, callback_data=f"genre_{janr.lower().replace(' ', '_')}"
                )
            ]
        )
    klaviatura = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Janr tanlang:", reply_markup=klaviatura)


@dp.message(Command("all_authors"))
async def all_authors(message: Message):
    buttons = []
    authors = [
        "Kazuo Ishiguro",
        "J.R.R. Tolkien",
        "J.K. Rowling",
        "Frank Herbert",
        "George Orwell",
        "Jane Austen",
        "Arthur Conan Doyle",
        "Yuval Noah Harari",
        "Paulo Coelho",
        "Bram Stoker",
    ]
    for author in authors:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=author,
                    callback_data=f"author_{author.lower().replace(' ', '_')}",
                )
            ]
        )
    klaviatura = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Muallif tanlang:", reply_markup=klaviatura)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
