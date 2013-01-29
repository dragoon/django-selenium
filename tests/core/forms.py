from django import forms


class SampleSearchForm(forms.Form):
    """Search form for test purposes"""
    query = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-xlarge search-query',
                                                          'autocomplete': 'off'}))
