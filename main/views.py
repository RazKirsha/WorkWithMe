from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator

from .forms import *
from .models import *
from offers.forms import SkillsForm
from offers.models import Offers
from pros.models import AcceptOffer
from pros.forms import AcceptOfferForm

from django.contrib import messages


# from pros.models import Notify


# def get_notification(user):

# notification = Notify.objects.filter(seen=False)


# Create your views here.
def signup(request):
    form = CustomCreationForm()
    skills_form = SkillsForm()

    if request.method == "POST":
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            form.save()

        latest_profile = Profile.objects.latest('created')
        skills_form = SkillsForm(request.POST, request.FILES, instance=latest_profile)
        if skills_form.is_valid():
            skills_form.save()

        if skills_form.is_valid() and form.is_valid():
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            messages.success(request, 'Account created successfully, Your are now logged in!')
            return redirect('homepage')
        else:
            messages.error(request, 'there was a problem with your signup data, please try again')

    return render(request, 'registration/signup.html',
                  {'form': form, 'skills_form': skills_form})


def homepage(request):
    if request.user.is_authenticated:
        me = request.user.profile
        my_offers = Offers.objects.filter(offer_maker=me)
        users_meetings = AcceptOffer.objects.filter(offer__in=my_offers, seen=False, updated=False, deleted=False,
                                                    meeting_time__gte=datetime.now())
        if users_meetings:
            for notification in users_meetings:
                messages.info(request,
                              f'{notification.offer} has been recieved. Meeting is at {notification.meeting_time}')
                notification.seen = True
                notification.save()

        pro_meetings = AcceptOffer.objects.filter(pro=me, seen=False, updated=True, deleted=False)

        if pro_meetings:
            for notification in pro_meetings:
                messages.warning(request,
                                 f'{notification.offer} has been updated. Meeting is now at {notification.meeting_time}')
                notification.seen = True
                notification.save()

        pro_meetings = AcceptOffer.objects.filter(pro=me, seen=False, deleted=True)

        if pro_meetings:
            for notification in pro_meetings:
                messages.warning(request, f'{notification.offer} has been Deleted.')
                notification.seen = True
                notification.save()

    return render(request, 'homepage.html')


def sendEmail(request):
    if request.method == 'POST':
        template = render_to_string('email_template.html', {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'message': request.POST['message'],
        })

        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['razlala1421@gmail.com']
        )

        email.fail_silently = False
        email.send()

        return redirect('homepage')


@login_required
def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    me = request.user.profile

    my_offers = Offers.objects.filter(offer_maker=me)
    meetings_as_pro = AcceptOffer.objects.filter(pro=me, deleted=False)
    meetings_as_user = AcceptOffer.objects.filter(offer__in=my_offers).filter(deleted=False)

    if profile == me:
        pending_offers = Offers.objects.filter(offer_maker=profile, date_deadline__gte=datetime.now(), accepted=False)

        page_num = request.GET.get('page')
        offers_paginator = Paginator(pending_offers, 3)
        page = offers_paginator.get_page(page_num)

        context = {
            'profile': profile,
            'count': offers_paginator.count,
            'page': page,
            'meetings_as_pro': meetings_as_pro,
            'meetings_as_user': meetings_as_user,
        }

        return render(request, 'profile.html', context)
    return render(request, 'profile.html',
                  {'profile': profile, 'meetings_as_pro': meetings_as_pro, 'meetings_as_user': meetings_as_user})


@login_required
def edit_meeting(request, pk):
    meeting = AcceptOffer.objects.get(id=pk)

    if request.method == 'GET':
        print('\n')
        print('----------------')
        print(meeting.reformat_time)
        print('----------------')
        print('\n')
        form = AcceptOfferForm(instance=meeting)
        return render(request, 'accept_offer.html', {'form': form})

    elif request.method == 'POST':
        data = request.POST
        form = AcceptOfferForm(data, instance=meeting)
        if form.is_valid():
            edited_meeting = form.save(commit=False)
            edited_meeting.updated = True
            edited_meeting.seen = False
            edited_meeting.save()
        return redirect('homepage')


@login_required
def delete_meeting(request, pk):
    meeting = AcceptOffer.objects.get(id=pk)

    if request.method == 'GET':
        return render(request, 'delete_meeting_confirm.html')

    elif request.method == 'POST':
        meeting.deleted = True
        meeting.seen = False
        meeting.save()
        return redirect('homepage')
