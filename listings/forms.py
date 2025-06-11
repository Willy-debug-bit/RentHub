from django import forms
from .models import Listing, Inquiry, Booking


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title',  
            'description', 
            'rent', 
            'location',
            'image', 
            'property_type', 
            'image', 
            'is_published'
            ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter listing title',
                'title': 'Listing Title',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe the property...',
                'title': 'Property Description',
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Enter price in KES',
                'title': 'Price',
                'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'e.g, Asego, Prisons, Shauri Yako...',
                'title': 'Location of Property',
                'class': 'form-control'
            }),
            'image': forms.ClearableFileInput(attrs={
                'title': 'Upload an image',
                'class': 'form-control'
            }),

            'is_published': forms.CheckboxInput(),
        }


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'message']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            
        }