from django.shortcuts import render, redirect
from .models import Events
from .forms import EventForm
from entry.views import login_required
from datetime import date
from django.http import HttpResponse
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from io import BytesIO
import os


@login_required
def home (request):
    events = Events.objects.filter(user_id = int(request.COOKIES['user_id']))
    curr_date = date.today()
    messages = []
    
    for event in events:        # delete past event
        if not event.is_anniversary and curr_date > event.date:
            messages.append(event.title + " has ended")
    Events.objects.filter(user_id = int(request.COOKIES['user_id']), is_anniversary = False, date__lt = curr_date).delete()

    events = Events.objects.filter(user_id = int(request.COOKIES['user_id']))
    for event in events:
        if event.is_anniversary:
            event.date = event.date.replace(year = curr_date.year)
            if curr_date > event.date:
                event.date = event.date.replace(year = curr_date.year + 1)

    events = sorted(events, key = lambda x: x.date)
    for event in events:
        days_remaining = (event.date - curr_date).days
        string = ""
        
        if days_remaining == 0:
            string = f"Today is {event.title} ({event.remark})"
        elif days_remaining == 1:
            string = f"Tomorrow is {event.title} ({event.remark})"
        else:
            string = f"{event.title} is due {days_remaining} days"

        def ordinaltag(n):
            return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= n % 100 < 20 else n % 10, "th")
        
        if event.is_anniversary:
            anniversary_date = Events.objects.get(event_id = event.event_id).date
            year_completed = curr_date.year - anniversary_date.year
            if curr_date.month > anniversary_date.month or (curr_date.month == anniversary_date.month and curr_date.day > anniversary_date.day):
                year_completed += 1
            
            string += f" ({ordinaltag(year_completed)} Anniversary)"
        messages.append(string)

    return render(request, 'event_home.html', {'messages' : messages})

@login_required
def manage_event(request):
    events = Events.objects.filter(user_id = int(request.COOKIES['user_id'])).order_by('-event_id')
    return render(request, 'manage_event.html', {'events' : events})

@login_required
def create_event(request):              # Create
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user_id = int(request.COOKIES['user_id'])
            instance.save()
            return redirect('event:home')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})


@login_required
def edit_event(request, event_id):      # Update
    instance = Events.objects.get(event_id = event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance = instance)
        if form.is_valid():
            form.save()
            return redirect('event:manage')
    else:
        form = EventForm(instance = instance)
    return render(request, 'event_form.html', {'form': form})


@login_required
def remove_event(request, event_id):    # Delete
    event = Events.objects.get(event_id = event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event:manage')
    return render(request, 'confirm_delete_event.html', {'event': event})


@login_required
def generate_wish(request):
    if request.method == "POST":
        background_path = os.path.join(settings.MEDIA_ROOT, 'background.png')

        background = Image.open(background_path)
        X, Y = background.size

        if 'photo' in request.FILES:
            uploaded_photo = request.FILES['photo']
            photo = Image.open(uploaded_photo)
            photo = photo.resize((int(X / 72 * 13.7), int(Y / 36 * 13.7)))
            background.paste(photo, (int(X / 72 * 18), int(Y / 36 * 17.1)))
        
        draw = ImageDraw.Draw(background)
        
        font = ImageFont.truetype('font/The Mumbai Sticker.ttf', Y / 36 * 7)
        title = request.POST.get('title')
        
        bbox = draw.textbbox((0, 0), title, font = font)
        x = bbox[2] - bbox[0]
        draw.text(((X - x) / 2, Y / 6), title, font = font, fill = "#f4bd18")

        font = ImageFont.truetype('font/Girassol.ttf', Y / 6)
        first_name = request.POST.get('first_name')
        draw.text((X / 2, Y / 2), first_name, font = font, fill = "#cf9d2e")
        
        if 'last_name' in request.POST:    
            last_name = request.POST.get('last_name')
            draw.text((X / 2, 2 * Y / 3), last_name, font = font, fill = "#cf9d2e")

        output_path = os.path.join(settings.MEDIA_ROOT, 'generated_wish.png')
        background.save(output_path)

        pdf_path = os.path.join(settings.MEDIA_ROOT, 'wish.pdf')
        buffer = BytesIO()
        c = canvas.Canvas(buffer)
        c.setPageSize((background.width, background.height))
        c.drawImage(output_path, 0, 0)
        c.showPage()
        c.save()

        buffer.seek(0)
        pdf_data = buffer.getvalue()
        buffer.close()

        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="wish.pdf"'
        return response

    return render(request, 'generate_wish.html')