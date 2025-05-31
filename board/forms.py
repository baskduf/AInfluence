from django import forms



class WriteForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), required=True)


    def save(self):
        pass
