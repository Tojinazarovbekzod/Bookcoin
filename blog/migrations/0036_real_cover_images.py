from django.db import migrations

WP = "https://upload.wikimedia.org/wikipedia"
SF = "https://commons.wikimedia.org/wiki/Special:FilePath"

COVER_IMAGES = {
    # Abdulla Qodiriy markasi (Commons)
    "O'tkan Kunlar":     f"{SF}/Stamps_of_Uzbekistan,_2004-07.jpg?width=300",
    "Mehrobdan Chayon":  f"{SF}/Stamps_of_Uzbekistan,_2004-07.jpg?width=300",

    # Abdulla Qahhor markasi (Commons)
    "Sarob":             f"{SF}/Stamps_of_Uzbekistan,_2007-05.jpg?width=300",

    # G'afur G'ulom portreti (Commons - tasdiqlangan URL)
    "Shum Bola": (
        f"{WP}/commons/3/30/"
        "%D0%93%D0%B0%D1%84%D1%83%D1%80_%D0%93%D1%83%D0%BB%D1%8F%D0%BC"
        "_%28%D0%BF%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82%29.jpg"
    ),

    # Bobur portreti — Yulduzli Tunlar va Boburnoma uchun
    "Yulduzli Tunlar": (
        f"{WP}/commons/7/7a/"
        "Humayun_and_Babur_%28Late_Shah_Jahan_Album%29_Babur_detail.jpg"
    ),
    "Boburnoma": (
        f"{WP}/commons/7/7a/"
        "Humayun_and_Babur_%28Late_Shah_Jahan_Album%29_Babur_detail.jpg"
    ),

    # Ulug'bek haykali (Commons - tasdiqlangan URL)
    "Ulug'bek Xazinasi": (
        f"{WP}/commons/thumb/1/19/Mirza_Ulugh_Beg_150.jpg/250px-Mirza_Ulugh_Beg_150.jpg"
    ),

    # Oybek portreti — Guliston jurnali (Commons - tasdiqlangan URL)
    "Qutlug' Qon": (
        f"{WP}/commons/thumb/0/0c/Oybek_%28Guliston_Magazine%29.jpg"
        "/250px-Oybek_%28Guliston_Magazine%29.jpg"
    ),

    # Said Ahmad portreti (uz.wikipedia - tasdiqlangan URL)
    "Ikki Eshik Orasi": (
        f"{WP}/uz/thumb/5/50/Said_Ahmad.jpg/250px-Said_Ahmad.jpg"
    ),

    # Alpomish — Sovet markasi (Commons)
    "Alpomish": (
        f"{SF}/The_Soviet_Union_1988_CPA_5990_stamp_"
        "(Alpamysh,_Uzbek_epic_poem._R._Khalilov).jpg?width=300"
    ),

    # Hamza Hakimzoda Niyoziy portreti (Commons - tasdiqlangan URL)
    "Padarkush": (
        f"{WP}/commons/d/da/Hamza_Niyazi.jpg"
    ),

    # Odil Yoqubov portreti (uz.wikipedia - tasdiqlangan URL)
    "Diyonat": (
        f"{WP}/uz/thumb/6/61/Odil_Yoqubov.jpg/250px-Odil_Yoqubov.jpg"
    ),
}


def apply_real_covers(apps, schema_editor):
    Book = apps.get_model('blog', 'Book')
    for title, url in COVER_IMAGES.items():
        Book.objects.filter(title=title).update(cover_image=url)


def revert(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0035_fix_cover_images'),
    ]

    operations = [
        migrations.RunPython(apply_real_covers, revert),
    ]
