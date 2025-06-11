from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from listings.models import Listing, Inquiry, Booking


# Create your views here.
@login_required                                                                                                                                                                                                                                                                                                                                                                                                                                                             
def dashboard(request):
    user_listings = Listing.objects.filter(owner=request.user)
    user_inquiries = Inquiry.objects.filter(listing__owner=request.user)
    user_bookings = Booking.objects.filter(user=request.user)

    context = {
        'user_listings': user_listings,
        'user_inquiries': user_inquiries,
        'user_bookings': user_bookings,
    }
    return render(request, 'users/dashboard.html', context, {'user_listings': user_listings})

@login_required
def rentee_dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    inquiries = Inquiry.objects.filter(listing__owner=request.user)

    return render(request, 'users/rentee_dashboard.html', {
        'bookings': bookings,
        'inquiries': inquiries,
    })