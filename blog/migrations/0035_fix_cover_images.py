from django.db import migrations

P = "https://placehold.co/300x450"

COVER_IMAGES = {
    "O'tkan Kunlar":     f"{P}/2e0052/ffffff?text=O%27tkan%0AKunlar",
    "Mehrobdan Chayon":  f"{P}/2e0052/ffffff?text=Mehrobdan%0AChayon",
    "Sarob":             f"{P}/1a1a2e/ffffff?text=Sarob",
    "Shum Bola":         f"{P}/0f3460/ffffff?text=Shum%0ABola",
    "Yulduzli Tunlar":   f"{P}/2e0052/ffffff?text=Yulduzli%0ATunlar",
    "Ulug'bek Xazinasi": f"{P}/1b1b2f/ffffff?text=Ulug%27bek%0AXazinasi",
    "Qutlug' Qon":       f"{P}/3a0000/ffffff?text=Qutlug%27%0AQon",
    "Ikki Eshik Orasi":  f"{P}/0d3b1f/ffffff?text=Ikki+Eshik%0AOrasi",
    "Alpomish":          f"{P}/2e0052/ffffff?text=Alpomish",
    "Padarkush":         f"{P}/1a1a2e/ffffff?text=Padarkush",
    "Diyonat":           f"{P}/1a2e00/ffffff?text=Diyonat",
    "Boburnoma":         f"{P}/2e1a00/ffffff?text=Boburnoma",
}


def fix_cover_images(apps, schema_editor):
    Book = apps.get_model('blog', 'Book')
    for title, url in COVER_IMAGES.items():
        Book.objects.filter(title=title).update(cover_image=url)


def revert_fix(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0034_update_book_cover_images'),
    ]

    operations = [
        migrations.RunPython(fix_cover_images, revert_fix),
    ]
