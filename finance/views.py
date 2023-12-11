from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import resolve
from django.views.generic import View
from .models import Bill
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeekDay, ExtractHour
from utils.charts import months, weekdays, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict, get_day_dict
from datetime import datetime, date, timedelta

# Create your views here.
# def home(request):
#
#     bills = Bill.objects.all()
#
#
#     return render(request, 'finance/home.html', {'bills': bills})
#

class home(TemplateView):
    template_name = 'finance/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_threshold = datetime.strptime("01.11.2023", "%d.%m.%Y")
        bills = Bill.objects.filter(date__gt=date_threshold).order_by('date')
        context["bills"] = bills
        return context


def report(request):
    object_list = Bill.objects.all()
    paginator = Paginator(object_list, 50)
    page = request.GET.get('page')
    try:
        strokes = paginator.page(page)
    except PageNotAnInteger:
        strokes = paginator.page(1)
    except EmptyPage:
        strokes = paginator.page(paginator.num_pages)

    return render(request, 'finance/report.html', {'strokes': strokes, 'page': page})

def get_top_3(request):
    top_positions = Bill.objects.values('position').annotate(total_quantity=Sum('quantity')).order_by(
        '-total_quantity')[:3]
    top_positions_list = [{'position': position_data['position'], 'total_quantity': position_data['total_quantity']} for position_data in top_positions]
    return JsonResponse(top_positions_list, safe=False)

def get_grouped_data(request):
    grouped_data = Bill.objects.values('position').annotate(total_quantity=Sum('quantity'))

    data_as_list = list(grouped_data)  # Преобразуйте QuerySet в список словарей

    return JsonResponse(data_as_list, safe=False)


def finance(request):
    grouped_data = Bill.objects.values('position').annotate(total_quantity=Sum('quantity'))
    return render(request, 'finance/finance.html',)



def plan(request):
    return render(request, 'finance/plan.html')

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'finance/charts.html', {})


def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "cutomers": 10,
    }
    return JsonResponse(data)

def get_filter_options(request):
    grouped_bills = Bill.objects.annotate(year=ExtractYear("date")).values("year").order_by("-year").distinct()
    options = [bill["year"] for bill in grouped_bills ]

    return JsonResponse({
        "options": options,
    })

def get_filter_options_day(request):
    grouped_bills = Bill.objects.all().values("date").order_by("-date").distinct()
    options = [bill["date"] for bill in grouped_bills ]

    return JsonResponse({
        "options": options,
    })



def get_sales_chart(request, year):
    bills = Bill.objects.filter(date__year=year)
    grouped_bills = bills.annotate(month=ExtractMonth("date")) \
        .values("month").annotate(summa=Sum("sum")).values("month", "summa").order_by("month")

    sales_dict = get_year_dict()

    for group in grouped_bills:
        sales_dict[months[group["month"] - 1]] = round(group["summa"], 2)

    return JsonResponse({
        "title": f"Sales in {year}",
        "data": {
            "labels": list(sales_dict.keys()),
            "datasets": [{
                "label": "Сумма",
                "backgroundColor": '#000000',
                "borderColor": colorPrimary,
                "data": list(sales_dict.values()),
            }]
        },
    })

def get_sales_day_chart(request, year):
    bills = Bill.objects.filter(date__year=year)
    grouped_bills = bills.annotate(weekday=ExtractWeekDay("date")) \
        .values("weekday").annotate(summa=Avg("sum")).values("weekday", "summa").order_by("weekday")

    sales_dict = get_day_dict()

    for group in grouped_bills:
        sales_dict[weekdays[group["weekday"] - 1]] = round(group["summa"], 2)

    return JsonResponse({
        "title": f"Sales in {year}",
        "data": {
            "labels": list(sales_dict.keys()),
            "datasets": [{
                "label": "Сумма",
                "backgroundColor": '#000000',
                "borderColor": colorPrimary,
                "data": list(sales_dict.values()),
            }]
        },
    })

def get_card_information(request):
    today = date.today()
    year_start = date(today.year, 1, 1)
    month_start = date(today.year, today.month, 1)

    daily_sales = Bill.objects.filter(date=today).aggregate(Sum('sum'))['sum__sum'] or 0
    monthly_sales = Bill.objects.filter(date__gte=month_start).aggregate(Sum('sum'))['sum__sum'] or 0
    yearly_sales = Bill.objects.filter(date__gte=year_start).aggregate(Sum('sum'))['sum__sum'] or 0



    # Получаем суммы за предыдущий день, месяц и год
    yesterday = today - timedelta(days=1)
    if today.month == 1:
        last_month_start = date(today.year - 1, 12, 1)
    else:
        last_month_start = date(today.year, today.month - 1, 1)
    last_year_start = date(today.year - 1, 1, 1)

    yesterday_sales = Bill.objects.filter(date=yesterday).aggregate(Sum('sum'))['sum__sum'] or 0
    last_month_sales = Bill.objects.filter(date__gte=last_month_start, date__lt=month_start).aggregate(Sum('sum'))['sum__sum'] or 0
    last_year_sales = Bill.objects.filter(date__gte=last_year_start, date__lt=year_start).aggregate(Sum('sum'))['sum__sum'] or 0

    def calculate_percentage(current, previous):
        return round((((current - previous) / previous)* 100),2)  if previous != 0 else current

    daily_change = calculate_percentage(daily_sales, yesterday_sales)
    monthly_change = calculate_percentage(monthly_sales, last_month_sales)
    yearly_change = calculate_percentage(yearly_sales, last_year_sales)

    data = {
        'today': str(today),
        'daily_sales': daily_sales,
        'monthly_sales': monthly_sales,
        'yearly_sales': yearly_sales,
        'daily_change': daily_change,
        'monthly_change': monthly_change,
        'yearly_change': yearly_change,
        'daily_change_color': 'green' if daily_change > 0 else 'red',
        'monthly_change_color': 'green' if monthly_change > 0 else 'red',
        'yearly_change_color': 'green' if yearly_change > 0 else 'red',

    }

    return JsonResponse(data)

def get_sales_hour_chart(request, day):
    day_date = datetime.strptime(day, "%Y-%m-%d")
    bills = Bill.objects.filter(date=day_date)  # Filter bills for the specified day


    # извлекаем часы, но нужно прогруппирровать
    # grouped_bills = bills.annotate(hour=ExtractHour("date")) \
    #     .values("hour").annotate(summa=Sum("sum")).values("hour", "summa").order_by("hour")

    grouped_bills = bills.values("position").annotate(summa=Sum("quantity")).values("position", "summa")


    return JsonResponse({
        "title": f"Sales in {day_date}",
        "data": {
            "labels": list(grouped_bills['position']),
            "datasets": [{
                "label": "Сумма",
                "backgroundColor": '#000000',
                "borderColor": colorPrimary,
                "data": list(grouped_bills.summa),
            }]
        },
    })
