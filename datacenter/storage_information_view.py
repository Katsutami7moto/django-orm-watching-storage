from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datetime import datetime, timezone, timedelta
from django.utils.timezone import localtime
from django.db import models


def get_duration(visit_local_time: datetime) -> timedelta:
    return datetime.now(timezone.utc) - visit_local_time


def format_duration(delta: timedelta) -> str:
    delta_total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(delta_total_seconds, 60 * 60)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


def storage_information_view(request):
    non_closed_visits = []
    visits_not_leaved = Visit.objects.filter(leaved_at=None)
    for visit in visits_not_leaved:
        visiter_name = visit.passcard.owner_name
        visit_local_time = visit.entered_at
        duration = format_duration(get_duration(localtime(visit_local_time)))
        visit_info = {
            'who_entered': visiter_name,
            'entered_at': visit_local_time,
            'duration': duration,
        }
        non_closed_visits.append(visit_info)

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
