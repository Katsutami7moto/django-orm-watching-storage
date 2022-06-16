from datetime import datetime, timezone, timedelta

from django.db import models
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(visit: Visit) -> timedelta:
    if visit.leaved_at:
        return localtime(visit.leaved_at) - localtime(visit.entered_at)
    else:
        return datetime.now(timezone.utc) - localtime(visit.entered_at)


def format_duration(delta: timedelta) -> str:
    delta_total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(delta_total_seconds, 60 * 60)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


def is_visit_longer_than(visit: Visit, minutes: int):
    duration = get_duration(visit)
    duration_in_seconds = duration.total_seconds() // 60
    minutes_in_seconds = timedelta(minutes=minutes).total_seconds() // 60
    return format_duration(duration), duration_in_seconds > minutes_in_seconds
