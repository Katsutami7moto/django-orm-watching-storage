from django.shortcuts import render

from datacenter.models import Visit, is_visit_longer_than


def storage_information_view(request):
    unfinished_visits = Visit.objects.filter(leaved_at=None)
    serialized_visits = []
    for visit in unfinished_visits:
        visiter_name = visit.passcard.owner_name
        visit_entered_at = visit.entered_at
        duration, is_strange = is_visit_longer_than(visit=visit, minutes=60)
        serialized_visit = {
            'who_entered': visiter_name,
            'entered_at': visit_entered_at,
            'duration': duration,
            'is_strange': is_strange,
        }
        serialized_visits.append(serialized_visit)

    context = {
        'non_closed_visits': serialized_visits,
    }
    return render(request, 'storage_information.html', context)
