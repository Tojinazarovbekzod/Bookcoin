from django.db import models


class Tag(models.Model):
    name = models.CharField(verbose_name="Tag name",max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return str(self.name)  

class Book(models.Model):
    GENRE_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Mathematics',      'Mathematics'),
        ('Physics',          'Physics'),
        ('Economics',        'Economics'),
        ('Biology',          'Biology'),
        ('Law',              'Law'),
        ('Psychology',       'Psychology'),
        ('History',          'History'),
        ('Philosophy',       'Philosophy'),
        ('Engineering',      'Engineering'),
        ('Chemistry',        'Chemistry'),
        ('Medicine',         'Medicine'),
        ('General',          'General'),
    ]

    title       = models.CharField(verbose_name="Book name", max_length=550)
    body        = models.TextField(verbose_name="Description", blank=True)
    author      = models.CharField(verbose_name="Author", default="Admin", max_length=100)
    genre       = models.CharField(verbose_name="Genre", max_length=100, choices=GENRE_CHOICES, default='General')
    price       = models.PositiveIntegerField(verbose_name="Price (BKC)", default=0)
    rating      = models.DecimalField(verbose_name="Rating", max_digits=3, decimal_places=1, default=0.0)
    cover_image = models.URLField(verbose_name="Cover Image URL", blank=True, default='')
    tag         = models.ManyToManyField(Tag, blank=True)
    views       = models.PositiveIntegerField(default=0)
    publish_date= models.DateTimeField(verbose_name="Published date", auto_now_add=True)
    published   = models.BooleanField(default=True)
    on_top      = models.BooleanField(default=False)
    content     = models.TextField(blank=True)

    def __str__(self):
        return str(self.title)

class Comment(models.Model):
    author = models.CharField(verbose_name="Comment author", max_length=100, blank=False)
    text = models.TextField(verbose_name="Comment")
    post = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.author} - {self.text[:30]}"

class Rating(models.Model):
    post = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="ratings")
    value = models.PositiveSmallIntegerField(verbose_name="Comment", default=0 )
    
    def __str__(self):
        return str(self.value)
    
    

class Notification(models.Model):
    ICON_CHOICES = [
        ('warning', 'Warning'),
        ('stars',   'Stars'),
        ('mail',    'Mail'),
        ('info',    'Info'),
    ]
    COLOR_CHOICES = [
        ('error',     'Red'),
        ('secondary', 'Yellow'),
        ('primary',   'Purple'),
    ]
    title      = models.CharField(max_length=255)
    message    = models.TextField()
    icon       = models.CharField(max_length=50, choices=ICON_CHOICES, default='mail')
    color      = models.CharField(max_length=50, choices=COLOR_CHOICES, default='primary')
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class PurchaseHistory(models.Model):
    user        = models.ForeignKey('User', on_delete=models.CASCADE, related_name='purchases')
    book_title  = models.CharField(max_length=550)
    book_author = models.CharField(max_length=200, blank=True)
    book_genre  = models.CharField(max_length=100, blank=True)
    price       = models.PositiveIntegerField(default=0)
    book_img    = models.URLField(blank=True, default='')
    purchased_at= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-purchased_at']

    def __str__(self):
        return f"{self.user} — {self.book_title}"


class User(models.Model):
    username = models.CharField(max_length=150) 
    surname = models.CharField(max_length=150)  
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'surname'],
                name='unique_username_and_surname_together'
            )
        ]

    def __str__(self):
        return f"{self.username} {self.surname}"