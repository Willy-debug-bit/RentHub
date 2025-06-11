from django.shortcuts import render, redirect, get_object_or_404
from .forms import ListingForm, InquiryForm, BookingForm
from django.contrib.auth.decorators import login_required
from .models import Listing, Booking
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect('listings')  # Make sure your URL name matches
    else:
        form = ListingForm()
    return render(request, 'listings/create_listing.html', {'form': form})

def listings_page(request):
    query = request.GET.get('query', '')
    location = request.GET.get('location', '')
    price_range = request.GET.get('price_range', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    listings = Listing.objects.filter(is_published=True)

    if query:
        listings = listings.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

    if location: 
        listings = listings.filter(location=location)

    if min_price:
        listings = listings.filter(price_gte=min_price)

    if max_price :
        listings = listings.filter(price_lte=max_price)

    # Price range filter
    if price_range == '0-5000':
        listings = listings.filter(price_lte=5000)
    elif price_range == '5000-10000':
        listings = listings.filter(price_gte=5000, price_lte=10000)
    elif price_range == '10000+':
        listings = listings.filter(price_gte=10000)

    locations = Listing.objects.values_list('location', flat=True).distinct()

    

    paginator = Paginator(listings, 10)  # 10 listings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print("Rendering listings_page.html template")
    


    return render(request, 'listings/listings_page.html', {
        'page_obj': page_obj,
        'query': query,
        'location': location,
        'min_price': min_price,
        'max_price': max_price,
        'price_range': price_range,
        'locations': locations,
    })


def listing_detail(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    return render(request, 'listings/listing_detail.html', {'listing': listing})

@login_required
def edit_listing(request, slug):
    listing = get_object_or_404(Listing, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/edit_listing.html', {'form': form})

@login_required
def delete_listing(request, slug):
    listing = get_object_or_404(Listing, slug=slug, owner=request.user)
    if request.method == 'POST':
        listing.delete()
        return redirect('dashboard')
    return render(request, 'listings/delete_listing.html', {'listing': listing})


def inquiry_view(request, slug):
    listing = get_object_or_404(Listing, slug=slug)

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.listing = listing
            inquiry.save()
            return redirect('listing_detail', slug=slug)
    else:
        form = InquiryForm()

    return render(request, 'listings/inquiry_form.html', {'form': form, 'listing': listing})


@login_required
def booking_view(request, slug):
    print("Inside book_listing view")
    listing = get_object_or_404(Listing, slug=slug)
    if request.method == 'POST':
        print("Inside book_listing view")
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.listing = listing
            booking.user = request.user
            booking.status = 'Pending'
            booking.save()
            return redirect('listings:listing_detail', slug=slug)
    else:
        form = BookingForm()
    return render(request, 'listings/booking_form.html', {'form': form, 'listing': listing})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
        else:
            form = UserCreationForm()
        return render(request, 'auth/register.html', {'form': form})
    