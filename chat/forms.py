from django import forms
from .models import ChatRoom


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(CreateRoomForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'placeholder': 'Room name',
             'class': 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'placeholder': 'Room description',
             'class': 'form-control'})
