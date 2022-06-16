from datetime import timedelta

from django.shortcuts import render
from django.utils.timezone import localtime

from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.storage_information_view import get_duration, format_duration


def is_visit_longer_than(visit: Visit, minutes: int):
    duration = get_duration(visit)
    if duration:
        duration_in_seconds = duration.total_seconds() // 60
        minutes_in_seconds = timedelta(minutes=minutes).total_seconds() // 60
        return format_duration(duration), duration_in_seconds > minutes_in_seconds


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    passcard_visits = Visit.objects.filter(passcard=passcard)
    serialized_visits = []
    for visit in passcard_visits:
        visit_entered_at = visit.entered_at
        duration, is_strange = is_visit_longer_than(visit=visit, minutes=60)
        serialized_visit = {
            'entered_at': visit_entered_at,
            'duration': duration,
            'is_strange': is_strange
        }
        serialized_visits.append(serialized_visit)

    context = {
        'passcard': passcard,
        'this_passcard_visits': serialized_visits
    }
    return render(request, 'passcard_info.html', context)
