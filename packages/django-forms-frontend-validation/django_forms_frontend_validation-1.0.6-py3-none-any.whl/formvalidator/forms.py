from django import forms


class SampleForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Phone Number', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Address', max_length=100, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 50}))
