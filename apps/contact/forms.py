from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Honeypot field for anti-spam bots
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'tabindex': '-1', 'autocomplete': 'off'})
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Name',
                'required': True,
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'name@example.com',
                'required': True,
                'autocomplete': 'email',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Tell me about your project, idea, or opportunity...',
                'rows': 5,
                'required': True,
            }),
        }

    def clean_website(self):
        # If honeypot is filled, it's likely a bot
        val = self.cleaned_data.get('website')
        if val:
            raise forms.ValidationError('Bot detected.')
        return val

    def clean_message(self):
        msg = self.cleaned_data.get('message', '').strip()
        if len(msg) < 10:
            raise forms.ValidationError('Please provide a message with at least 10 characters.')
        return msg

