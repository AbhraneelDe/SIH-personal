from .models import Notification

def unread_notifications(request):
    if request.user.is_authenticated:
        qs = Notification.objects.filter(user=request.user)
        unread_count = qs.filter(is_read=False).count()
        latest = qs[:5]
        return {
            'unread_notifications_count': unread_count,
            'latest_notifications': latest
        }
    return {
        'unread_notifications_count': 0,
        'latest_notifications': []
    }
