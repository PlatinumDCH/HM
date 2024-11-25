from django import forms
from .models import Quotes, Author

class QuoteForm(forms.ModelForm):
    new_author = forms.CharField(max_length=200, min_length=3, required=False, label='New Author')

    class Meta:
        model = Quotes
        fields = ['quote', 'tags', 'author', 'new_author']

    def __init__(self, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['author'] = forms.ModelChoiceField(
            queryset=Author.objects.all(),
            required=False,
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'author-select'})
        )
        self.fields['new_author'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'author-input',
            'style': 'display: none;',
            'placeholder': 'Enter a new author name'
        })

