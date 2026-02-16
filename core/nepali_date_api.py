from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
import nepali_datetime

@api_view(['GET'])
@permission_classes([AllowAny])
def get_nepali_date(request):
    """
    API endpoint to get current Nepali date and time
    Returns Bikram Sambat date in Nepali Unicode
    """
    # Use Django local time so weekday/date are calculated in configured timezone.
    now = timezone.localtime()
    
    # Convert to Nepali datetime
    nepali_now = nepali_datetime.date.from_datetime_date(now.date())
    
    # Nepali month names
    nepali_months = {
        1: 'बैशाख', 2: 'जेठ', 3: 'असार', 4: 'साउन',
        5: 'भदौ', 6: 'असोज', 7: 'कार्तिक', 8: 'मंसिर',
        9: 'पुष', 10: 'माघ', 11: 'फागुन', 12: 'चैत्र'
    }
    
    # Nepali weekday names
    nepali_weekdays = {
        0: 'सोमबार', 1: 'मंगलबार', 2: 'बुधबार', 3: 'बिहिबार',
        4: 'शुक्रबार', 5: 'शनिबार', 6: 'आइतबार'
    }
    
    # Convert numbers to Nepali
    def to_nepali_number(num):
        nepali_digits = {'0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
                        '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'}
        return ''.join(nepali_digits.get(d, d) for d in str(num))
    
    # Format the date
    year = to_nepali_number(nepali_now.year)
    month = nepali_months[nepali_now.month]
    day = to_nepali_number(nepali_now.day)
    weekday = nepali_weekdays[now.weekday()]
    
    # Format time
    hour = to_nepali_number(now.strftime('%I'))
    minute = to_nepali_number(now.strftime('%M'))
    am_pm = 'बिहान' if now.hour < 12 else 'बेलुका'
    
    return Response({
        'date': f'{year} {month} {day}, {weekday}',
        'time': f'{hour}:{minute} {am_pm}',
        'timestamp': now.isoformat()
    })
