# Generated by Django 4.2.7 on 2023-12-24 06:17

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_comment_created_alter_comment_updated_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(upload_to='post_images/')),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='عنوان')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='blog.post', verbose_name='پست')),
            ],
            options={
                'verbose_name': 'تصویر',
                'verbose_name_plural': 'تصویرها',
                'ordering': ['created'],
                'indexes': [models.Index(fields=['created'], name='blog_image_created_1ba45b_idx')],
            },
        ),
    ]
