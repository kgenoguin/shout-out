from __future__ import unicode_literals
from django.db import models
from django.conf import settings


class Profile(models.Model):

    def upload_user_image(instance, filename):
        return u'images/users/%s/%s' % (str(instance.user), str(filename))

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank = True, null = True)
    photo = models.ImageField(upload_to=upload_user_image, blank = True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
