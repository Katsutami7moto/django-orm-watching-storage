from datetime import datetime, timezone, timedelta

from django.shortcuts import render
from django.utils.timezone import localtime

from datacenter.models import Visit


def get_duration(later: datetime, earlier: datetime):
    if later and earlier:
        return later - earlier


def format_duration(delta: timedelta) -> str:
    delta_total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(delta_total_seconds, 60 * 60)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


def storage_information_view(request):
    unfinished_visits = Visit.objects.filter(leaved_at=None)
    serialized_visits = []
    for visit in unfinished_visits:
        visiter_name = visit.passcard.owner_name
        visit_entered_at = visit.entered_at
        duration = format_duration(get_duration(later=datetime.now(timezone.utc), earlier=localtime(visit_entered_at)))
        visit_info = {
            'who_entered': visiter_name,
            'entered_at': visit_entered_at,
            'duration': duration,
        }
        serialized_visits.append(visit_info)

    context = {
        'non_closed_visits': serialized_visits,
    }
    return render(request, 'storage_information.html', context)
