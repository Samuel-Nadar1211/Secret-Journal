from django.shortcuts import render, redirect
from .models import Entries
from .forms import EntryForm
from account.models import User
from event.models import Events


def login_required(func):       # decorator
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.COOKIES or 'password' not in request.COOKIES:
            return redirect('account:index')
        
        try:
            user = User.objects.get(user_id = int(request.COOKIES['user_id']))
            if user.password != request.COOKIES['password']:
                return redirect('account:logout')
        except (User.DoesNotExist, KeyError):
            return redirect('account:logout')

        if 'entry_id' in kwargs:
            entry_id = kwargs['entry_id']
            try:
                entry = Entries.objects.get(entry_id = entry_id)
                if entry.user_id != int(request.COOKIES['user_id']):
                    return home(request)
            except Entries.DoesNotExist:
                return home(request)

        if 'event_id' in kwargs:
            event_id = kwargs['event_id']
            from event.views import manage_event

            try:
                event = Events.objects.get(event_id = event_id)
                if event.user_id != int(request.COOKIES['user_id']):
                    return manage_event(request)
            except Events.DoesNotExist:
                return manage_event(request)
            
        return func(request, *args, **kwargs)
    return wrapper


@login_required
def home (request):
    user = User.objects.get(user_id = int(request.COOKIES['user_id']))
    entries = Entries.objects.filter(user_id = int(request.COOKIES['user_id']))
    
    if request.method == "POST":
        if 'title' in request.POST:
            title = request.POST.get('title').strip()
            entries = entries.filter(title__icontains = title)

        elif 'start_date' in request.POST:
            from django.utils.dateparse import parse_date
            from datetime import timedelta
            
            start_date = parse_date(request.POST.get('start_date'))
            end_date = parse_date(request.POST.get('end_date'))
            entries = entries.filter(date_created__gte = start_date, date_created__lt = end_date + timedelta(days=1))

    context = {
        'user_name' : user.name,
        'entries' : entries.order_by('-date_updated')
    }

    return render(request, 'home.html', context)


@login_required
def create_entry(request):              # Create
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user_id = int(request.COOKIES['user_id'])
            instance.save()
            return redirect('entry:home')
    else:
        form = EntryForm()
    return render(request, 'entry_form.html', {'form': form})


@login_required
def read_entry(request, entry_id):      # Read
    entry = Entries.objects.get(entry_id = entry_id)
    return render(request, 'entry.html', {'entry': entry})


@login_required
def edit_entry(request, entry_id):      # Update
    instance = Entries.objects.get(entry_id = entry_id)
    
    if request.method == 'POST':
        form = EntryForm(request.POST, instance = instance)
        if form.is_valid():
            form.save()
            return redirect('entry:read', entry_id = entry_id)
    else:
        form = EntryForm(instance = instance)
    return render(request, 'entry_form.html', {'form': form})


@login_required
def remove_entry(request, entry_id):    # Delete
    entry = Entries.objects.get(entry_id = entry_id)
    if request.method == 'POST':
        entry.delete()
        return redirect('entry:home')
    return render(request, 'confirm_delete.html', {'entry': entry})
