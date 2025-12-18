from django.db import models

class Tag(models.Model):
    name = models.CharField(verbose_name="Tag name",max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return str(self.name)  

class Post(models.Model):
    title = models.CharField(verbose_name="Post title", max_length=550)
    body = models.TextField(verbose_name="Post body")
    author = models.CharField(verbose_name="Post author", default="Admin", max_length=100)
    tag = models.ManyToManyField(Tag)
    views = models.PositiveIntegerField(default=0)
    publish_date = models.DateTimeField(verbose_name="Published date", auto_now_add=True)
    published = models.BooleanField(default=True)
    on_top = models.BooleanField(default=False)
    content = models.TextField()

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    author = models.CharField(verbose_name="Comment author", max_length=100, blank=False)
    text = models.TextField(verbose_name="Comment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.author} - {self.text[:30]}"

class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="ratings")
    value = models.PositiveSmallIntegerField(verbose_name="Comment", default=0 )
    
    def __str__(self):
        return str(self.value)
    
    

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