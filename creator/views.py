from django.shortcuts import render
from .service import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

def index(request):
    csv_data = get_csv_data("creator_info.csv")
    labels = get_four_previous_weeks_date()
    print("labels:", labels)
    chart_label = "Weekly subscribers"
    print("chart_label:", chart_label)
    chart_data = get_subs_for_last_four_weeks()
    print("chart_data:", chart_data)
    context = {
        "name": csv_data["Name"][0],
        "username": csv_data["username"][0],
        "total_likes": csv_data["Total likes"][0],
        "total_share": csv_data["Total share"][0],
        "total_comments": csv_data["Total comments"][0],
        "labels": labels,
        "chart_label": chart_label,
        "chart_data": chart_data
    }
    return render(request, "index.html", context)