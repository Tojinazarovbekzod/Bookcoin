from django.db import migrations

WP = "https://upload.wikimedia.org/wikipedia"
SF = "https://commons.wikimedia.org/wiki/Special:FilePath"

UZBEK_BOOKS = [
    {
        'title': "O'tkan Kunlar",
        'author': 'Abdulla Qodiriy',
        'genre': 'History',
        'body': (
            "O'zbek adabiyotining birinchi klassik romani (1925). "
            "XIX asrning ikkinchi yarmida Toshkentda yashagan Otabek va Kumushning "
            "fojiaviy muhabbati orqali o'sha davr o'zbek jamiyati, urf-odatlari va "
            "siyosiy hayoti tasvirlanadi. Asar o'zbek prozasining asosi hisoblanadi."
        ),
        'price': 60,
        'rating': 5.0,
        'cover_image': f"{SF}/Stamps_of_Uzbekistan,_2004-07.jpg?width=300",
        'on_top': True,
    },
    {
        'title': "Mehrobdan Chayon",
        'author': 'Abdulla Qodiriy',
        'genre': 'History',
        'body': (
            "Abdulla Qodiriyning ikkinchi romani (1929). "
            "Asarda feodal zulm va jaholat ostida ezilgan Ro'zi va Anvarning fojiaviy "
            "taqdiri tasvirlanadi. Roman o'zbek xalqining o'tmish hayotini, "
            "eski urf-odatlar va ijtimoiy muammolarni yorqin ko'rsatib beradi."
        ),
        'price': 55,
        'rating': 4.9,
        'cover_image': f"{SF}/Stamps_of_Uzbekistan,_2004-07.jpg?width=300",
        'on_top': False,
    },
    {
        'title': "Sarob",
        'author': 'Abdulla Qahhor',
        'genre': 'Psychology',
        'body': (
            "Abdulla Qahhorning mashhur romani (1943). "
            "Asarda ikki yuz yildan ortiq Toshkentda yashab kelgan "
            "Sobirov oilasining taqdiri, urush yillarida insoniy his-tuyg'ular "
            "va ruhiy izlanishlar poetik mahorat bilan tasvirlanadi."
        ),
        'price': 50,
        'rating': 4.8,
        'cover_image': f"{SF}/Stamps_of_Uzbekistan,_2007-05.jpg?width=300",
        'on_top': False,
    },
    {
        'title': "Shum Bola",
        'author': "G'afur G'ulom",
        'genre': 'General',
        'body': (
            "G'afur G'ulomning o'z bolaligi haqidagi avtobiografik qissasi (1936). "
            "XX asr boshlarida Toshkentdagi oddiy mahallada o'sadigan Shakar "
            "nomli bolaning sarguzashtlari, o'sha davr hayoti va o'zbek xalqining "
            "turmush tarzi jonli va hazil-mutoyiba bilan tasvirlanadi."
        ),
        'price': 40,
        'rating': 4.7,
        'cover_image': (
            f"{WP}/commons/3/30/"
            "%D0%93%D0%B0%D1%84%D1%83%D1%80_%D0%93%D1%83%D0%BB%D1%8F%D0%BC"
            "_%28%D0%BF%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82%29.jpg"
        ),
        'on_top': False,
    },
    {
        'title': "Yulduzli Tunlar",
        'author': 'Pirimqul Qodirov',
        'genre': 'History',
        'body': (
            "Pirimqul Qodirovning tarixiy romani (1978). "
            "Ulug' astronom va shoir Zahiriddin Muhammad Bobur hayoti tasvirlanadi: "
            "uning taxtni qo'lga kiritish uchun olib borgan kurashi, Hindistonga "
            "safarlari, so'yish va zafarlari, hamda she'riy ijodi."
        ),
        'price': 65,
        'rating': 4.9,
        'cover_image': (
            f"{WP}/commons/7/7a/"
            "Humayun_and_Babur_%28Late_Shah_Jahan_Album%29_Babur_detail.jpg"
        ),
        'on_top': True,
    },
    {
        'title': "Ulug'bek Xazinasi",
        'author': 'Odil Yoqubov',
        'genre': 'History',
        'body': (
            "Odil Yoqubovning tarixiy romani (1973). "
            "Ulug' astronom va olim Mirzo Ulug'bekning hayoti, ilmiy kashfiyotlari, "
            "Samarqanddagi rasadxonasini qurishi va fojiali o'limi tasvirlanadi. "
            "Asar ilm-fan va jaholat o'rtasidagi abadiy kurashni aks ettiradi."
        ),
        'price': 60,
        'rating': 4.8,
        'cover_image': (
            f"{WP}/commons/thumb/1/19/Mirza_Ulugh_Beg_150.jpg"
            "/250px-Mirza_Ulugh_Beg_150.jpg"
        ),
        'on_top': False,
    },
    {
        'title': "Qutlug' Qon",
        'author': 'Oybek',
        'genre': 'History',
        'body': (
            "Oybek (Muso Toshmuhammad o'g'li)ning tarixiy romani (1940). "
            "Amir Temur va Toxtamishxon o'rtasidagi ziddiyatlar, "
            "XV asr O'rta Osiyo siyosiy hayoti, xalq qahramonligi va "
            "vatanparvarlik mavzularini qamrab olgan yirik epik asar."
        ),
        'price': 55,
        'rating': 4.7,
        'cover_image': (
            f"{WP}/commons/thumb/0/0c/Oybek_%28Guliston_Magazine%29.jpg"
            "/250px-Oybek_%28Guliston_Magazine%29.jpg"
        ),
        'on_top': False,
    },
    {
        'title': "Ikki Eshik Orasi",
        'author': 'Said Ahmad',
        'genre': 'General',
        'body': (
            "Said Ahmadning (Xudoyberdiyev) mashhur romani (1971). "
            "Asar urushdan keyingi O'zbekistonda kolxoz hayotini, oddiy dehqon "
            "va ishchilarning turmushini, sevgi va sadoqat mavzularini "
            "o'tkir kuzatuvchanlik va yumor bilan tasvirlaydi."
        ),
        'price': 45,
        'rating': 4.6,
        'cover_image': (
            f"{WP}/uz/thumb/5/50/Said_Ahmad.jpg/250px-Said_Ahmad.jpg"
        ),
        'on_top': False,
    },
    {
        'title': "Alpomish",
        'author': "O'zbek Xalq Eposi",
        'genre': 'General',
        'body': (
            "O'zbek xalqining eng qadimiy va mashhur qahramonlik dostoni. "
            "Bahodur Alpomish Boysinning yetti yillik asirlikdan qaytib, "
            "yurtini va sevgilisi Barchinoyni ozod qilish uchun olib borgan "
            "mardlik kurashi tasvirlanadi. Doston o'zbek xalqining ruhini ifodalaydi."
        ),
        'price': 35,
        'rating': 5.0,
        'cover_image': (
            f"{SF}/The_Soviet_Union_1988_CPA_5990_stamp_"
            "(Alpamysh,_Uzbek_epic_poem._R._Khalilov).jpg?width=300"
        ),
        'on_top': False,
    },
    {
        'title': "Padarkush",
        'author': 'Hamza Hakimzoda Niyoziy',
        'genre': 'General',
        'body': (
            "Hamza Hakimzoda Niyoziyning mashhur dramma asari (1915). "
            "Ota-ona va farzand munosabatlari, eski va yangi hayot o'rtasidagi "
            "ziddiyat, ma'naviy qiymat va axloqiy mas'uliyat mavzularini "
            "o'tkir dramaturgi mahorat bilan tasvirlagan birinchi o'zbek dramasida."
        ),
        'price': 40,
        'rating': 4.5,
        'cover_image': f"{WP}/commons/d/da/Hamza_Niyazi.jpg",
        'on_top': False,
    },
    {
        'title': "Diyonat",
        'author': 'Odil Yoqubov',
        'genre': 'Psychology',
        'body': (
            "Odil Yoqubovning zamonaviy romani (1958). "
            "Jamiyatda vijdon, diyonat va insoniy qadr-qimmat mavzularini ko'taradi. "
            "Asarda turli xil odamlarning hayoti va ularning axloqiy tanlovlari, "
            "yaxshilik va yomonlik o'rtasidagi kurash tasvirlanadi."
        ),
        'price': 50,
        'rating': 4.6,
        'cover_image': (
            f"{WP}/uz/thumb/6/61/Odil_Yoqubov.jpg/250px-Odil_Yoqubov.jpg"
        ),
        'on_top': False,
    },
    {
        'title': "Boburnoma",
        'author': 'Zahiriddin Muhammad Bobur',
        'genre': 'History',
        'body': (
            "Zahiriddin Muhammad Boburning o'z qo'li bilan yozgan avtobiografik asari "
            "(XVI asr). Bobur o'z hayotini, harbiy yurishlarini, tabiat va "
            "odamlarga bo'lgan kuzatishlarini o'tkir idrok va she'riy til bilan "
            "bayon etadi. Dunyo adabiyotining noyob yodgorliklaridan biri."
        ),
        'price': 70,
        'rating': 5.0,
        'cover_image': (
            f"{WP}/commons/7/7a/"
            "Humayun_and_Babur_%28Late_Shah_Jahan_Album%29_Babur_detail.jpg"
        ),
        'on_top': True,
    },
]


def recreate_books(apps, schema_editor):
    Book = apps.get_model('blog', 'Book')
    Book.objects.all().delete()
    for data in UZBEK_BOOKS:
        Book.objects.create(
            title=data['title'],
            author=data['author'],
            genre=data['genre'],
            body=data['body'],
            price=data['price'],
            rating=data.get('rating', 0),
            cover_image=data['cover_image'],
            on_top=data.get('on_top', False),
            published=True,
        )


def delete_books(apps, schema_editor):
    Book = apps.get_model('blog', 'Book')
    Book.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0036_real_cover_images'),
    ]

    operations = [
        migrations.RunPython(recreate_books, delete_books),
    ]
