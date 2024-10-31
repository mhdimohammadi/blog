from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse
from django_resized import ResizedImageField
from django.template.defaultfilters import slugify


class PublishedManager(models.Manager):
    def get_queryset(self, query):
        return super().get_queryset(query).filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts', verbose_name='نویسنده')
    title = models.CharField(max_length=250, verbose_name='عنوان')
    description = models.TextField(verbose_name="توضیحات")
    slug = models.SlugField(max_length=250, verbose_name='اسلاگ')
    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    created = jmodels.jDateTimeField(auto_now_add=True)
    update = jmodels.jDateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name='وضعیت')
    reading_time = models.PositiveIntegerField(verbose_name='زمان مطالعه', default=0)

    def __str__(self):
        return self.title

    objects = jmodels.jManager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.id])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for img in self.images.all():
            storage, path = img.image_file.storage, img.image_file.path
            storage.delete(path)
        super().delete(*args, **kwargs)


class Ticket(models.Model):
    message = models.TextField(verbose_name='پیام')
    name = models.CharField(verbose_name="نام", max_length=250)
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=11, verbose_name='شماره تماس')
    subject = models.CharField(max_length=250, verbose_name='موضوع')

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def __str__(self):
        return self.subject


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="پست")
    name = models.CharField(max_length=250, verbose_name="نام")
    body = models.TextField(verbose_name="متن کامنت")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    active = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]
        verbose_name = "کامنت"
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return f"{self.name}:{self.post}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name='پست')
    image_file = ResizedImageField(upload_to='post_images/', size=[500, 500], quality=100, crop=['middle', 'center'])
    title = models.CharField(max_length=250, verbose_name='عنوان', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    created = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصویرها'

    def __str__(self):
        return self.title if self.title else self.image_file.name

    def delete(self, *args, **kwargs):
        storage, path = self.image_file.storage, self.image_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)


class Account(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    date_of_birth = jmodels.jDateField(verbose_name="تاریخ تولد", blank=True, null=True)
    bio = models.TextField(verbose_name='بیو', blank=True, null=True)
    photo = ResizedImageField(verbose_name='تصویر پروفایل', upload_to='account/images', size=[500, 500], quality=60,
                              crop=['middle', "center"])
    job = models.CharField(max_length=250, verbose_name='شغل', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'اکانت'
        verbose_name_plural = 'اکانت ها'
