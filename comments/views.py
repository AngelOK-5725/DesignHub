from django.shortcuts import redirect, render

from payments.models import Purchase

# Create your views here.
# embroidery_designs/comments/views.py
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from payments.models import Purchase
from designs.models import Design
from .models import DesignComment

@login_required
def add_comment(request, design_id):
    design = get_object_or_404(Design, id=design_id, is_active=True)
    
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        
        if not text and not image and not video:
            return redirect('item_info', design_id=design_id)
        
        is_verified = Purchase.objects.filter(
            user=request.user,
            design=design
        ).exists()
        
        DesignComment.objects.create(
            design=design,
            user=request.user,
            text=text,
            image=image,
            video=video,
            is_verified_purchase=is_verified
        )
    
    return redirect('item_info', design_id=design_id)