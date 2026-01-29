from django import forms
from django.forms import inlineformset_factory
from .models import Poll, Choice

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description', 'category', 'is_public', 'allow_multiple_votes', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

ChoiceFormSet = inlineformset_factory(
    Poll, 
    Choice, 
    fields=('choice_text',), 
    extra=2, 
    can_delete=True,
    min_num=2,
    validate_min=True,
    max_num=10,
    validate_max=True
)
