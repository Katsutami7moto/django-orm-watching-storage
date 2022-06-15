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
    non_closed_visits = []
    visits_not_leaved = Visit.objects.filter(leaved_at=None)
    for visit in visits_not_leaved:
        visiter_name = visit.passcard.owner_name
        visit_entered_at = visit.entered_at
        duration = format_duration(get_duration(later=datetime.now(timezone.utc), earlier=localtime(visit_entered_at)))
        visit_info = {
            'who_entered': visiter_name,
            'entered_at': visit_entered_at,
            'duration': duration,
        }
        non_closed_visits.append(visit_info)

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
