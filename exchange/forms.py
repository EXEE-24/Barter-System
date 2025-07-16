from django import forms
from .models import ExchangeProposal
from ads.models import Ad

class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'comment']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['ad_sender'].queryset = Ad.objects.filter(
                user=user,
                is_active=True
            )
            self.fields['ad_sender'].label = "Ваше объявление для обмена"
            self.fields['comment'].label = "Ваше сообщение"
            self.fields['comment'].widget = forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Напишите сообщение для владельца товара...'
            })