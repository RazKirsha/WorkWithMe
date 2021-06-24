from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import *


# Create your views here.
@login_required
def make_offer(request):
    form = OfferForm()

    if request.method == 'POST':
        data = request.POST
        form = OfferForm(data)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.offer_maker = request.user.profile
            offer.save()
            form.save_m2m()
            messages.success(request, 'An offer was made!')
            return redirect('homepage')
    return render(request, 'make_offer.html', {'form': form})


def all_pros(request):
    data = Skills.objects.all()[0:8]
    return render(request, 'all_pros.html', {'data': data})

