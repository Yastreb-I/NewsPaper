from datetime import timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings

from news.models import Post, Category


def email_users_category(categories):
    user_email = []
    for user in categories.subscribers.all():
        user_email.append(user.email)
    return user_email


# Отправляет пост подписчику
def new_post_to_subscribes(instance):
    template = 'mailing/new_post_to_subscribes.html'
    subject = f'{instance.headPost}'

    for category in instance.categoriesPost.all():
        email_subject = subject
        email_users = email_users_category(category)
        context = {
            'category': category,
            'post': instance,
        }
        html = render_to_string(
            template_name=template,
            context=context,
        )

        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=email_users,
        )
        msg.attach_alternative(html, "text/html")
        msg.send()


# Приветственное письмо
def welcome_letter(user):
    template = 'mailing/welcome_letter.html'
    subject = 'Регистрация на сайте NewsPaper'
    email_user = user.email
    context = {'user': user.username, }
    html = render_to_string(
        template_name=template,
        context=context,
    )
    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email_user, ],
    )
    msg.attach_alternative(html, "text/html")
    msg.send()


# Еженедельная рассылка подписчикам
def weekly_newsletter():
    print("Запущена-weekly_newsletter")
    start_day = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date_of_week = start_day
    start_date_of_week = start_day - timedelta(weeks=1)
    posts = Post.objects.filter(dateCreation__gte=start_date_of_week, dateCreation__lt=end_date_of_week)
    subscribers = {}
    for post in posts:
        for category in post.categoriesPost.all():
            for subscriber in category.subscribers.all():

                if subscriber in subscribers.keys() and post not in subscribers[subscriber]:
                    subscribers[subscriber].append(post)
                else:
                    subscribers[subscriber] = [post]

    for subscriber, posts in subscribers.items():
        send_subscriber_posts(subscriber, posts)


def send_subscriber_posts(subscriber, posts):
    template = 'mailing/weekly_newsletter.html'
    subject = 'Подписки за неделю'
    email_user = subscriber.email
    context = {
        'user': subscriber.username,
        'posts': posts,
    }
    html = render_to_string(
        template_name=template,
        context=context,
    )
    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email_user, ],
    )
    msg.attach_alternative(html, "text/html")
    msg.send()
