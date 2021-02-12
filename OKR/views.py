from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import EntryCreationForm, ObjectiveCreationForm, KRCreationForm
from .models import Entry, Objective
from .filters import ObjectiveKRFilter
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def view_data(request):
    if request.method == 'POST' and 'objective-btn' in request.POST:
        form = ObjectiveCreationForm(request.POST)
        if form.is_valid():
            objective = form.save(commit=False)
            objective.user = get_object_or_404(User, id=request.user.id)
            objective.save()
            messages.success(request, 'Objective Created successfully')
            return redirect('okr-view-data')
    if request.method == 'POST' and 'entry-btn' in request.POST:
        form = EntryCreationForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = get_object_or_404(User, id=request.user.id)
            entry.save()
            messages.success(request, 'Entry Created successfully')
            return redirect('okr-view-data')
    if request.method == 'POST' and 'kr-btn' in request.POST:
        form = KRCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Key Result Created successfully')
            return redirect('okr-view-data')

    form_objective = ObjectiveCreationForm()
    form_kr = KRCreationForm()
    form_entry = EntryCreationForm()
    data = Entry.objects.filter(user=request.user)
    form = ObjectiveKRFilter(request.GET, queryset=data)
    data = form.qs

    paginator = Paginator(data, 10)

    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    context = {
        'data': response,
        'form_kr':form_kr,
        'form_objective':form_objective,
        'form_entry':form_entry,
        'filter_form': form
    }
    return render(request, 'OKR/show_entry.html', context=context)


@login_required
def load_okr(request):
    context = {

    }
    return render(request, 'webpages/index.html', context=context)