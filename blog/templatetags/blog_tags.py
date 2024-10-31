from django import template
from ..models import *
from django.db.models import Count
from markdown import markdown
from django.utils.safestring import mark_safe
from random import randrange

register = template.Library()


@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.simple_tag
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.simple_tag
def last_post_date():
    return Post.published.last().publish


@register.inclusion_tag('partials/latest_posts.html')
def latest_post(count):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {'l_posts': l_posts}
    return context


@register.simple_tag()
def most_popular_posts(count=5):
    return Post.published.annotate(comment_count=Count('comments')).order_by('-comment_count')[:count]


@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))


@register.simple_tag(name="mart")
def max_reading_time():
    posts = Post.published.all()
    all_times = []
    for post in posts:
        read_time = post.reading_time
        all_times.append(read_time)
    m = max(all_times)
    return m


@register.simple_tag(name="mirt")
def max_reading_time():
    posts = Post.published.all()
    all_times = []
    for post in posts:
        read_time = post.reading_time
        all_times.append(read_time)
    m = min(all_times)
    return m


@register.filter()
def censor(text):
    bad_words = ['بیشعور', 'گاو', 'خر', 'عوضی']
    for word in bad_words:
        if word in text:
            text = text.replace(word, "*" * len(word))
    return mark_safe(text)


@register.simple_tag(name='mau')
def most_active_user():
    users = User.objects.all()
    mx = 0
    u = None
    for user in users:
        if user.user_posts.filter(status=Post.Status.PUBLISHED).count() > mx:
            mx = user.user_posts.count()
            u = user
    return u


@register.simple_tag
def random_post():
    num = Post.published.count()
    post_num = randrange(1, num )
    return Post.published.get(id=post_num).get_absolute_url()
