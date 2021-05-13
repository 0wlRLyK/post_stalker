from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.utils import timezone


class OnlineUserActivity(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_activity = models.DateTimeField()

    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activity'

    @staticmethod
    def update_user_activity(user):
        """Updates the timestamp a user has for their last action. Uses UTC time."""
        OnlineUserActivity.objects.update_or_create(user=user, defaults={'last_activity': timezone.now()})

    @staticmethod
    def get_user_activities(time_delta=timedelta(minutes=15)):
        """
        Gathers OnlineUserActivity objects from the database representing active users.

        :param time_delta: The amount of time in the past to classify a user as "active". Default is 15 minutes.
        :return: QuerySet of active users within the time_delta
        """
        starting_time = timezone.now() - time_delta
        return OnlineUserActivity.objects.filter(last_activity__gte=starting_time).order_by('-last_activity')

    @staticmethod
    def check_user_online(user=AnonymousUser, time_delta=15):
        """
        Get information about one user activity

        :param user: Searched user last activity
       :param time_delta: The amount of time in the past to classify a user as "active". Default is 15 minutes.
       :return: QuerySet of active users within the time_delta
       """
        activity = OnlineUserActivity.objects.get(user=user)

        active_time = (timezone.now() - activity.last_activity)
        active_minutes = (active_time.seconds // 60) % 60
        if active_minutes > time_delta or active_time.days > 0:
            return False
        return True
