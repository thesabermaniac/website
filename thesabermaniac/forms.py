from django import forms


class TradeForm(forms.Form):
    name = forms.CharField()
    fangraphs_id = forms.CharField(widget=forms.HiddenInput(), required=False)
