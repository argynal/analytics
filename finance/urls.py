from django.urls import path, re_path
from .views import *
urlpatterns = [
    # path('home/', home),
    path('report/', report),
    path('finance/', finance),
    path('plan/', plan),
    re_path(r'^api/data/$', get_data, name = 'api/data'),
    re_path(r'homeview/^$', HomeView.as_view(), name = 'homeview'),
    path('home/', home.as_view(), name='index'),
    path('get_grouped_data/', get_grouped_data, name='get_grouped_data'),
    path('get_top_3/', get_top_3, name='get_top_3'),
    path("chart/filter-options/", get_filter_options, name="chart-filter-options"),
    path("chart/sales/<int:year>/", get_sales_chart, name="chart-sales"),
    path("chart/sales_days/<int:year>/", get_sales_day_chart, name="chart-sales-days"),
    path("chart/get_card_information/", get_card_information, name="get-card-information"),
    path("chart/filter-options-days/", get_filter_options_day, name="filter-options-days"),
    path("chart/sales_hour/<str:day>/", get_sales_hour_chart, name="chart-sales-hour"),
]