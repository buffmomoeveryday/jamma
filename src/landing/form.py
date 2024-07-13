from django import forms


class NewUrlForm(forms.Form):
    name = forms.CharField(max_length=255)
    url = forms.URLField(max_length=255)

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url")
        url = url.replace("http://", "")
        return cleaned_data
