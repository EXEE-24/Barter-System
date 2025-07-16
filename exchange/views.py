from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ads.models import Ad  # Импортируем модель Ad из приложения ads
from .models import ExchangeProposal
from .forms import ExchangeProposalForm
from django.contrib import messages


@login_required
def proposal_list(request):
    received_proposals = ExchangeProposal.objects.filter(
        ad_receiver__user=request.user
    ).select_related('ad_sender', 'ad_receiver')

    sent_proposals = ExchangeProposal.objects.filter(
        ad_sender__user=request.user
    ).select_related('ad_sender', 'ad_receiver')

    return render(request, 'exchange/proposal_list.html', {
        'received_proposals': received_proposals,
        'sent_proposals': sent_proposals
    })


@login_required
def update_proposal(request, pk):
    proposal = get_object_or_404(
        ExchangeProposal,
        pk=pk,
        ad_receiver__user=request.user
    )

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['accepted', 'rejected']:
            proposal.status = new_status
            proposal.save()
            messages.success(request, 'Статус предложения обновлен')
            if new_status == 'accepted':
                ExchangeProposal.objects.filter(
                    ad_receiver=proposal.ad_receiver,
                    status='pending'
                ).exclude(pk=proposal.pk).update(status='rejected')

    return redirect('exchange:proposal_list')


@login_required
def create_proposal(request, ad_id):
    ad_receiver = get_object_or_404(Ad, id=ad_id)

    if ad_receiver.user == request.user:
        messages.error(request, 'Вы не можете предложить обмен для своего товара')
        return redirect('ads:ad_detail', pk=ad_id)

    existing = ExchangeProposal.objects.filter(
        ad_sender__user=request.user,
        ad_receiver=ad_receiver
    ).exists()

    if existing:
        messages.error(request, 'Вы уже отправляли предложение для этого товара')
        return redirect('ads:ad_detail', pk=ad_id)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST, user=request.user)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_receiver = ad_receiver
            proposal.save()
            messages.success(request, 'Предложение успешно отправлено')
            return redirect('exchange:proposal_list')
    else:
        form = ExchangeProposalForm(user=request.user)

    return render(request, 'exchange/proposal_form.html', {
        'form': form,
        'ad_receiver': ad_receiver
    })