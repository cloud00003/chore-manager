from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

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


@require_POST
def chore_complete(request, pk):
    chore = get_object_or_404(Chore, pk=pk)
    chore.is_completed = True
    chore.save(update_fields=["is_completed"])
    return redirect("chores:chore_list")


@require_http_methods(["GET", "POST"])
def chore_edit(request, pk):
    chore = get_object_or_404(Chore, pk=pk)
    form = ChoreForm(
        request.POST if request.method == "POST" else None, instance=chore
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("chores:chore_list")
    return render(request, "chores/chore_form.html", {"form": form, "chore": chore})


@require_http_methods(["GET", "POST"])
def chore_delete(request, pk):
    chore = get_object_or_404(Chore, pk=pk)
    if request.method == "POST":
        chore.delete()
        return redirect("chores:chore_list")
    return render(request, "chores/chore_confirm_delete.html", {"chore": chore})
