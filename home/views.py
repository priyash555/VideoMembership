
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Membership, UserMembership, Subscription
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

import stripe

# Create your views here.
def starting(request):
    return render(request,'home/starting.html',{})

def about(request):
    return render(request,'home/about.html')

@login_required
def member(request):
    object = Membership.objects.all()
    context = { 'object_list':object,
                'current_membership':get_user_membership(request).membership
    }
    print(context)
    return render(request,'home/membership.html',context)

def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None

@login_required
def membersh(request,key):
    object = Membership.objects.filter(membership_type=key)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    user_membership = get_user_membership(request)
    context = { 'selected_membership':object,
                'publishKey': publishKey }
    return render(request,'home/membershipindi.html',context)


def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None


@login_required
def updateTransactionRecords(request, subscription_id, selected_membership):
    user_membership = get_user_membership(request)
    user_membership.membership = selected_membership
    user_membership.save()

    sub, created = Subscription.objects.get_or_create(
        user_membership=user_membership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()

    try:
        del request.session['selected_membership_type']
    except:
        pass

    messages.info(request, 'Successfully created {} membership'.format(
        selected_membership))
    return redirect(reverse('home-memberships'))

@login_required
def cancelSubscription(request):
    user_sub = get_user_subscription(request)

    if user_sub.active is False:
        messages.info(request, "You dont have an active membership")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
    sub.delete()

    user_sub.active = False
    user_sub.save()

    free_membership = Membership.objects.get(membership_type='Free')
    user_membership = get_user_membership(request)
    user_membership.membership = free_membership
    user_membership.save()


    return redirect(reverse('profileview'))

@login_required
def callfun(request,key):
    if request.method == "POST":
        object = Membership.objects.filter(membership_type=key)
        publishKey = settings.STRIPE_PUBLISHABLE_KEY
        user_membership = get_user_membership(request)
        selected_membership = Membership.objects.get(membership_type=key)
        token = request.POST['stripeToken']

        # UPDATE FOR STRIPE API CHANGE 2018-05-21

        '''
        First we need to add the source for the customer
        '''
        customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
        customer.source = token # 4242424242424242
        customer.save()

        '''
        Now we can create the subscription using only the customer as we don't need to pass their
        credit card source anymore
        '''

        subscription = stripe.Subscription.create(
            customer=user_membership.stripe_customer_id,
            items=[
                { "plan": selected_membership.stripe_plan_id },
            ]
        )
        updateTransactionRecords(request,subscription.id,selected_membership)
        return redirect(reverse('home-memberships'))

@login_required
def profile_view(request):
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request)
    context = {
        'user_membership': user_membership,
        'user_subscription': user_subscription
    }
    return render(request, "users/profile.html", context)
