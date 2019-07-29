from django import forms
from .models import *

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = ""
        self.fields['content'].widget = forms.TextInput()
        self.fields['content'].widget.attrs = {'class': "form-control", 'placeholder': "평가를 남겨주세요."}
