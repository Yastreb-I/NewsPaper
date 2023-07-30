from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from django.core.mail import send_mail, EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from django.conf import settings
from django.utils import timezone

from datetime import datetime, timedelta
from news.models import Author, Category, Post
import logging

logger = logging.getLogger("django")


@login_required
def upgrade_me(request):
    user = request.user
    Author.objects.create(userAuthor=user)
    # Удалить автора
    # auth = Author.objects.get(userAuthor=user)
    # auth.delete()

    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news')


class UserAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'user_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        groups_authors = user.groups.filter(name='authors').exists()

        if groups_authors:
            day = datetime.today().strftime("%Y-%m-%d")
            author = Author.objects.get(userAuthor__id=self.request.user.id)
            post_to_day = Post.objects.filter(author=author, dateCreation__date=day).count()
            context['post_to_day'] = post_to_day
            context['posts'] = Post.objects.filter(author=author)

        categories = Category.objects.all()
        subscribers_user = []
        for cat in categories:
            user_cat = cat.subscribers.filter(email=user.email)
            if user_cat.exists():
                subscribers_user.append(cat.id)

        context['is_not_authors'] = not groups_authors
        context['categories'] = categories
        context['subscribers'] = subscribers_user

        return context


# Сообщение о подписке пользователя на категорию
@login_required
def subscribe_to_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if not category.subscribers.filter(id=user.id).exists():
        email = user.email
        category.subscribers.add(user)
        context = {'category': category,
                   'user': user,
                   }
        email_html = render_to_string('subscribers/email_subscription_messages.html', context)
        mesg = EmailMultiAlternatives(
            subject=f'Подтверждение подписки на категорию - {category}!',
            body=f'',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email, ],
        )
        mesg.attach_alternative(email_html, "text/html")
        try:
            mesg.send()  # отсылаем
        except Exception as e:
            logger.exception(e)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


# Сообщение об отписке категории пользователю
@login_required
def unsubscribe_to_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    email = user.email

    if category.subscribers.filter(id=user.id).exists():

        try:
            send_mail(
                subject=f'Отписка от темы',
                message=f'Здравствуй, {user}! \nВы отписались от категории - {category}! \n'
                        f'Надеемся Вы найдете для себя другие темы на нашем сайте.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email, ],
            )
            category.subscribers.remove(user)
        except Exception as e:
            print(e)
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))
