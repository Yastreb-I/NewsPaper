from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CommonLoginForm(SignupForm):

    def save(self, request):
        print(request)
        user = super(CommonLoginForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

