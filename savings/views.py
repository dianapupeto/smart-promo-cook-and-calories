from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from .models import SavingsRecord


@login_required
def dashboard(request):
    """Лична статистика: спестено на седмица + агрегирано по месец."""
    records = SavingsRecord.objects.filter(user=request.user).order_by("-week_start")

    monthly = (
        records
        .annotate(month=TruncMonth("week_start"))
        .values("month")
        .annotate(
            spent=Sum("total_spent"),
            regular=Sum("total_regular_price"),
        )
        .order_by("-month")
    )
    monthly_summary = [
        {"month": row["month"], "saved": (row["regular"] or 0) - (row["spent"] or 0)}
        for row in monthly
    ]

    total_saved = sum(m["saved"] for m in monthly_summary) if monthly_summary else 0

    context = {
        "records": records,
        "monthly_summary": monthly_summary,
        "total_saved": total_saved,
    }
    return render(request, "savings/dashboard.html", context)
