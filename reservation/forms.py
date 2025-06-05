from django import forms

from .models import VehicleRating


class VehicleRatingForm(forms.ModelForm):
    class Meta:
        model = VehicleRating
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.RadioSelect(),
            "comment": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Conte sua experiência com este veículo...",
                    "class": "form-control shadow-sm comment-box",
                }
            ),
        }
