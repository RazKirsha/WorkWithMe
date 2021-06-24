from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from offers.models import *

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import *
from main.models import Profile

from datetime import datetime


# Create your views here.
@login_required
def pro_profile(request):
    skills = request.user.profile.skills.all()
    offers = Offers.objects.filter(field__in=skills, accepted=False,
                                   date_deadline__gt=datetime.now()).distinct().order_by('date_deadline')

    page_num = request.GET.get('page')
    offers_paginator = Paginator(offers, 3)
    page = offers_paginator.get_page(page_num)

    context = {
        'count': offers_paginator.count,
        'offers': page,
    }

    return render(request, 'pro_profile.html', context)


@login_required
def accept_offer(request, pk):
    form = AcceptOfferForm()
    me = request.user.profile
    offer = Offers.objects.get(id=pk)

    if request.method == 'POST':
        data = request.POST
        form = AcceptOfferForm(data)
        if form.is_valid():
            offer.accepted = True
            schedule = form.save(commit=False)
            schedule.offer = offer
            schedule.pro = me
            offer.save()
            schedule.save()
            messages.success(request, f'Your meeting has been schedule!')
            return redirect('homepage')

    return render(request, 'accept_offer.html', {'form': form})


# @login_required
# def my_meetings(request):
#     me = request.user.profile
#     my_offers = Offers.objects.filter(offer_maker=me)
#     pro_meetings = AcceptOffer.objects.filter(pro=me)
#     users_meetings = AcceptOffer.objects.filter(offer__in=my_offers,
#                                                 meeting_time__lte=datetime.now())
#
#     return render(request, 'my_meetings.html', {'pro_meetings': pro_meetings, 'users_meetings': users_meetings})


@login_required
def video_chat(request, pk):
    meeting = AcceptOffer.objects.get(id=pk)
    me = request.user.profile
    if me == meeting.pro or me == meeting.offer.offer_maker:
        return render(request, 'video_chat.html', {'meeting': meeting})

    messages.success(request, 'This meeting is not for you darling!')
    return redirect('homepage')


@login_required
def create_feedback(request, pk):
    pro = Profile.objects.get(id=pk)

    if request.method == 'GET':
        rating_form = CreateFeedbackForm(instance=pro)
        return render(request, 'create_feedback.html', {'form': rating_form})

    elif request.method == 'POST':
        data = request.POST
        pro_rating = int(pro.rating)
        rating_form = CreateFeedbackForm(data, instance=pro)
        if rating_form.is_valid():
            current_rating = int(data['rating'])
            edited_pro = rating_form.save(commit=False)
            num_reviews = edited_pro.reviews_num
            edited_pro.rating = round((pro_rating * num_reviews + current_rating) / (num_reviews + 1))
            edited_pro.reviews_num += 1
            edited_pro.save()
            messages.success(request, 'Thanks for your review!')
        return redirect('homepage')
