# forms.py

from django import forms

class ExampleForm(forms.Form):
    """
    A basic form definition demonstrating common field types.
    """
    # Text Input
    name = forms.CharField(
        label='Your Name',
        max_length=100,
        help_text='Enter your full name.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Email Input with Validation
    email = forms.EmailField(
        label='Email Address',
        required=True,
        help_text='We will send a confirmation email here.'
    )

    # Number Input
    age = forms.IntegerField(
        label='Your Age',
        min_value=18,
        max_value=99,
        required=False  # Optional field
    )

    # Selection Field (Dropdown)
    favorite_color = forms.ChoiceField(
        label='Favorite Color',
        choices=[
            ('blue', 'Blue'),
            ('green', 'Green'),
            ('red', 'Red'),
            ('other', 'Other')
        ],
        initial='blue'
    )

    # Text Area
    comment = forms.CharField(
        label='Comments',
        required=False,
        widget=forms.Textarea
    )

    # Boolean/Checkbox
    agree_to_terms = forms.BooleanField(
        label='I agree to the terms and conditions.',
        required=True
    )