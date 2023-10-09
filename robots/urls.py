from django.urls import path

from .views.weekly_prod_report import get_exel_weekly_prod_report


urlpatterns = [
    # Endpoint for generating a weekly production report in Excel format
    path('weekly_prod_report/', get_exel_weekly_prod_report, name='weekly_prod_report'),
]
