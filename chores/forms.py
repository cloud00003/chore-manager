from django import forms

from .models import Chore


class ChoreForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ["title", "responsible_person", "deadline"]
        widgets = {
            "deadline": forms.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }
