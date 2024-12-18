"""Module that holds functionality related to user badge management"""
from django.apps import apps

def check_for_badge_awards(user) -> None:
    """Checks whether user is eligible to receive any of the badges the user does not currently have
    If user is eligible to earn a new badge, it is created"""
    Badge = apps.get_model("sovf", "Badge")
    UserBadge = apps.get_model("sovf", "UserBadge")

    for badge in Badge.objects.all():
        if UserBadge.objects.filter(user=user, badge=badge).exists():
            continue

        if badge.check_eligibility(user):
            UserBadge.objects.create(user=user, badge=badge)
