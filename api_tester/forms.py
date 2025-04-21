from django import forms
from .models import APIRequest

class APIRequestForm(forms.Form):
    url = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://api.example.com/endpoint'}),
        required=True
    )
    method = forms.ChoiceField(
        choices=APIRequest.METHOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    headers = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Content-Type: application/json\nAuthorization: Bearer token',
            'rows': 3
        }),
        required=False,
        help_text='Enter headers as key-value pairs, one per line'
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': '{\n  "key": "value"\n}',
            'rows': 5
        }),
        required=False,
        help_text='Enter JSON request body'
    )
    
    def clean_headers(self):
        headers_text = self.cleaned_data.get('headers', '')
        if not headers_text:
            return {}
        
        headers_dict = {}
        for line in headers_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if ':' in line:
                key, value = line.split(':', 1)
                headers_dict[key.strip()] = value.strip()
        
        return headers_dict
    
    def clean_body(self):
        body = self.cleaned_data.get('body', '')
        if not body:
            return None
        return body
