from django import forms


class TelegramIdForm(forms.Form):
    telegram_id = forms.CharField(label='Telegram ID', max_length=100)