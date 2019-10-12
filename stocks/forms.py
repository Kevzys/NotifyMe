from django import forms

class CreateNewStockList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)

class CreateNewStock(forms.Form):
    symbol = forms.CharField(max_length=10)
