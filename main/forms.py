from django import forms
from .models import ContactProfile


class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactProfile
        fields = ("name", "email", "message")

    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Full name...",
            }
        ),
    )

    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email...",
            }
        ),
    )

    message = forms.CharField(
        max_length=1000,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Message...", "rows": 6}),
    )
