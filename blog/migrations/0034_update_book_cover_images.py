from django.db import migrations


COVER_IMAGES = {
    "O'tkan Kunlar": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Abdulla_Qodiriy.jpg/220px-Abdulla_Qodiriy.jpg"
    ),
    "Mehrobdan Chayon": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Abdulla_Qodiriy.jpg/220px-Abdulla_Qodiriy.jpg"
    ),
    "Sarob": (
        "https://upload.wikimedia.org/wikipedia/uz/thumb/5/5f/Abdulla_Qahhor.jpg/220px-Abdulla_Qahhor.jpg"
    ),
    "Shum Bola": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Gafur_Gulom.jpg/220px-Gafur_Gulom.jpg"
    ),
    "Yulduzli Tunlar": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Babur.jpg/220px-Babur.jpg"
    ),
    "Ulug'bek Xazinasi": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Ulugh_beg.jpg/220px-Ulugh_beg.jpg"
    ),
    "Qutlug' Qon": (
        "https://upload.wikimedia.org/wikipedia/uz/thumb/2/24/Oybek.jpg/220px-Oybek.jpg"
    ),
    "Ikki Eshik Orasi": (
        "https://upload.wikimedia.org/wikipedia/uz/thumb/3/35/Said_Ahmad.jpg/220px-Said_Ahmad.jpg"
    ),
    "Alpomish": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Alpamysh.jpg/220px-Alpamysh.jpg"
    ),
    "Padarkush": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Hamza_Hakimzoda_Niyoziy.jpg/220px-Hamza_Hakimzoda_Niyoziy.jpg"
    ),
    "Diyonat": (
        "https://upload.wikimedia.org/wikipedia/uz/thumb/6/6d/Odil_Yoqubov.jpg/220px-Odil_Yoqubov.jpg"
    ),
    "Boburnoma": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Babur.jpg/220px-Babur.jpg"
    ),
}


def update_cover_images(apps, schema_editor):
    Book = apps.get_model('blog', 'Book')
    for title, url in COVER_IMAGES.items():
        Book.objects.filter(title=title, cover_image='').update(cover_image=url)


def revert_cover_images(apps, schema_editor):
    Book = apps.get_model('blog', 'Book')
    for title, url in COVER_IMAGES.items():
        Book.objects.filter(title=title, cover_image=url).update(cover_image='')


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0033_uzbek_books_data'),
    ]

    operations = [
        migrations.RunPython(update_cover_images, revert_cover_images),
    ]
