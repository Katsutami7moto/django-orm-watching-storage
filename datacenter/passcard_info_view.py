from django.shortcuts import render

from datacenter.models import Visit, Passcard, is_visit_longer_than


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
            'is_strange': is_strange,
        }
        serialized_visits.append(serialized_visit)

    context = {
        'passcard': passcard,
        'this_passcard_visits': serialized_visits,
    }
    return render(request, 'passcard_info.html', context)
