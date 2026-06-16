# tours/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import TourPackage, CustomerInquiry

def home(request):
    # Fetch only 3 active packages to feature on the home page
    featured_packages = TourPackage.objects.filter(is_active=True).select_related('category')[:3]
    return render(request, 'home.html', {'packages': featured_packages})

def packages_list(request):
    # Start with all active packages
    packages = TourPackage.objects.filter(is_active=True).select_related('category')
    
    # 1. Search by Destination / Title
    destination = request.GET.get('destination', '')
    if destination:
        packages = packages.filter(title__icontains=destination)
        
    # 2. Filter by Duration
    duration = request.GET.get('duration', '')
    if duration == 'short':
        packages = packages.filter(duration_days__lte=7)
    elif duration == 'medium':
        packages = packages.filter(duration_days__gt=7, duration_days__lte=14)
    elif duration == 'long':
        packages = packages.filter(duration_days__gt=14)
        
    # 3. Filter by Max Price
    max_price = request.GET.get('max_price', '')
    if max_price and max_price.isdigit():
        packages = packages.filter(price__lte=max_price)

    # 4. Sort Results
    sort = request.GET.get('sort', 'featured')
    if sort == 'price_low':
        packages = packages.order_by('price')
    elif sort == 'price_high':
        packages = packages.order_by('-price')
    elif sort == 'duration_short':
        packages = packages.order_by('duration_days')
    elif sort == 'duration_long':
        packages = packages.order_by('-duration_days')
    else:
        packages = packages.order_by('-id') # Default Featured (Newest)

    # Pass the current filters back to the template to keep the form populated
    context = {
        'packages': packages,
        'current_destination': destination,
        'current_duration': duration,
        'current_max_price': max_price,
        'current_sort': sort,
    }
    return render(request, 'packages.html', context)

def package_detail(request, pk):
    # Fetch a specific package by its ID (Primary Key)
    package = get_object_or_404(TourPackage, pk=pk, is_active=True)
    return render(request, 'package_detail.html', {'package': package})

def submit_inquiry(request, pk):
    # Handle the form submission from the package details page
    package = get_object_or_404(TourPackage, pk=pk)
    
    if request.method == 'POST':
        # Grab the data from the Tailwind form
        customer_name = request.POST.get('customer_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        # Save it to the database
        CustomerInquiry.objects.create(
            package=package,
            customer_name=customer_name,
            phone_number=phone_number,
            email=email,
            message=message
        )
        
        # Redirect back to the home page after successful submission
        # (In a real app, you might want to redirect to a 'Thank You' page)
        return redirect('tours:home')
        
    return redirect('tours:package_detail', pk=pk)

def tailor_made(request):
    if request.method == 'POST':
        # Here you will eventually save the form data to a new BespokeInquiry model
        # For now, we capture it and show a success message
        name = request.POST.get('name')
        # Simulate saving the high-value lead
        messages.success(request, f"Thank you, {name}. Our VIP Concierge will contact you within 2 hours.")
        return redirect('tours:tailor_made')
        
    return render(request, 'tailor_made.html')