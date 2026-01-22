import nepali_datetime

def to_nepali_date(ad_date):
    """Converts AD date to BS date string"""
    if not ad_date:
        return ""
    bs_date = nepali_datetime.date.from_datetime_date(ad_date)
    return bs_date.strftime('%K-%n-%D') # YYYY-MM-DD format in BS


def current_nepali_date():
    return nepali_datetime.date.today()

def get_submission_url(request, office_id):
    from django.urls import reverse
    relative_url = reverse('grievance_submit')
    return request.build_absolute_uri(f"{relative_url}?office_id={office_id}")
