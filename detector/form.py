from django import forms

class HoaxTextForm(forms.Form):
    hoax_text = forms.CharField(label='Teks Hoaks', widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}), disabled=True)
