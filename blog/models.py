from django.db import models
from django.contrib.auth.models import User
from accounts.models import Customer
from tinymce.models import HTMLField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from django.utils.text import slugify
from django.urls import reverse


class Post(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    ]

    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(unique=True, max_length=100)
    content = HTMLField()
    description = models.TextField(max_length=300, blank=True, help_text="A short summary for the post.")
    thumbnail = ProcessedImageField(
        upload_to='post_thumbnails',
        processors=[ResizeToFit(700, 700)],
        format='WEBP',
        options={'quality': 90}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seo_title = models.CharField(max_length=70, blank=True, help_text="SEO title for the post.")
    seo_description = models.CharField(max_length=160, blank=True, help_text="SEO description for the post.")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    tags = models.CharField(max_length=100, blank=True, help_text="Comma-separated tags for the post.")
    view_count = models.PositiveIntegerField(default=0) 


    class Meta:
        db_table = 'post'
        indexes = [
            models.Index(fields=['slug', 'status']),
        ]
        ordering = ['-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_like_count(self):
        likes = Like.objects.filter(post=self)
        return likes.count()

    def get_comment_count(self):
        comments = Comment.objects.filter(post=self)
        return comments.count()
    


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        db_table = 'comment'
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.get_full_name()} on {self.post}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'like'
        unique_together = ('post', 'user') 


    def __str__(self):
        return f'Like by {self.user.get_full_name()} on {self.post}'