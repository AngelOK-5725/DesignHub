# embroidery_designs/designs/forms.py

from django import forms
from .models import DesignRating

class RatingForm(forms.ModelForm):
    class Meta:
        model = DesignRating
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)])
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'rating-radio'})