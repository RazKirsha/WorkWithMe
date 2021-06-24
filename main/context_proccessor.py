from pros.models import AcceptOffer
from offers.models import Offers
from datetime import datetime


def active_offers(request):
    if not request.user.is_authenticated:
        return []

    else:
        me = request.user.profile
        my_offers = Offers.objects.filter(offer_maker=me)
        pro_meetings = AcceptOffer.objects.filter(pro=me,
                                                  meeting_time__gte=datetime.now(), deleted=False).order_by(
            'meeting_time')
        users_meetings = AcceptOffer.objects.filter(offer__in=my_offers).filter(
            meeting_time__gte=datetime.now(), deleted=False).order_by('meeting_time')

        return {'pro_meetings': pro_meetings, 'users_meetings': users_meetings}
