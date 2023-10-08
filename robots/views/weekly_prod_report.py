from datetime import datetime, timedelta

from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from openpyxl import Workbook

from robots.models import Robot


def weekly_prod_report():
    """
    Retrieves the weekly production report of robots created in the last week.

    Returns:
        list: A list of grouped reports,
        where each group contains the model, version, and count of robots.
    """
    # Calculate the start of the week
    start_of_week = datetime.now() - timedelta(days=7)

    # Initialize an empty list to store the weekly production report
    report = []

    # Initialize a dictionary to group the reports by model
    grouped_reports = {}

    # Query the database for robots created within the last week,
    # and annotate the count of each version
    robot_querysets = Robot.objects.filter(created__gte=start_of_week) \
        .values('model', 'version').annotate(count=Count('version'))

    # Extract the model, version, and count from the queryset
    # to the weekly production report
    for queryset in robot_querysets:
        model = queryset['model']
        version = queryset['version']
        count = queryset['count']
        report.append((model, version, count))

    # Group the reports by model
    for report in report:
        key = report[0]
        if key not in grouped_reports:
            grouped_reports[key] = []
        grouped_reports[key].append(report)

    # Convert the grouped reports into a list
    grouped_lists = list(grouped_reports.values())
    return grouped_lists


def weekly_prod_report_to_excel(report=list):
    """
    Converts the weekly production report to an Excel workbook.

    Args:
        report (list): The weekly production report.

    Returns:
        Workbook: An instance of the Excel workbook.
    """
    # Define the title row for the report
    title_row = ['Модель', 'Версия', 'Количество за неделю']

    # Create a new workbook
    workbook = Workbook()
    workbook.remove_sheet(workbook.active)

    # Generate a worksheet for each group of reports
    for group in report:
        worksheet = workbook.create_sheet(title=group[0][0])
        worksheet.append(title_row)

        # Append the data to the worksheet
        for model, version, count in group:
            worksheet.append([model, version, count])

    return workbook


def get_exel_weekly_prod_report(request):
    """
    Generates and returns an Excel file containing the weekly production report.

    Args:
        request: The HTTP request.

    Returns:
        HttpResponse: The HTTP response with the Excel file.
    """
    if request.method == 'GET':
        # Retrieve the weekly production report
        report = weekly_prod_report()

        # Convert the report to an Excel workbook
        workbook = weekly_prod_report_to_excel(report)

        # Create an HTTP response with the Excel file
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=weekly-prod-report.xlsx'

        # Save the workbook to the response
        workbook.save(response)

        # Return the response
        return response
    else:
        # Return an error response if the request method is not GET
        return JsonResponse({'error': 'Invalid request method'})
