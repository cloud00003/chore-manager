from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ChoreForm
from .models import Chore


def chore_list(request):
    return render(
        request,
        "chores/chore_list.html",
        {
            "incomplete_chores": Chore.objects.filter(is_completed=False).order_by(
                "deadline", "pk"
            ),
            "completed_chores": Chore.objects.filter(is_completed=True).order_by(
                "deadline", "pk"
            ),
        },
    )


@require_http_methods(["GET", "POST"])
def chore_create(request):
    form = ChoreForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("chores:chore_list")
    return render(request, "chores/chore_form.html", {"form": form})
