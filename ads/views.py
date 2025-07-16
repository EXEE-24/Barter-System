# ads/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ad, Category
from exchange.models import ExchangeProposal
from .forms import AdForm
from exchange.forms import ExchangeProposalForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

def ad_list(request):
    ads = Ad.objects.filter(is_active=True).order_by('-created_at')

    search_query = request.GET.get('search')
    if search_query:
        ads = ads.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    category_id = request.GET.get('category')
    if category_id:
        ads = ads.filter(category__id=category_id)

    condition = request.GET.get('condition')
    if condition:
        ads = ads.filter(condition=condition)

    paginator = Paginator(ads, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'ads/ad_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'selected_condition': condition,
        'search_query': search_query or ''
    })

@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ads:ad_detail', pk=ad.pk)
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})



def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, 'ads/ad_detail.html', {'ad': ad})


@login_required
def ad_update(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return redirect('ads:ad_list')

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ads:ad_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)

    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def proposal_create(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    if ad.user == request.user:
        return redirect('ads:ad_detail', pk=ad_id)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.sender = request.user
            proposal.receiver = ad.user
            proposal.ad = ad
            proposal.save()
            return redirect('ads:ad_detail', pk=ad_id)
    else:
        form = ExchangeProposalForm()
    return render(request, 'ads/proposal_form.html', {'form': form, 'ad': ad})


@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    # Проверка, что пользователь - автор объявления
    if ad.user != request.user:
        return redirect('ads:ad_list')

    if request.method == 'POST':
        ad.delete()
        return redirect('ads:ad_list')

    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})


def proposal_detail(request, pk):
    proposal = get_object_or_404(ExchangeProposal, pk=pk)
    return render(request, 'ads/proposal_detail.html', {'proposal': proposal})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



