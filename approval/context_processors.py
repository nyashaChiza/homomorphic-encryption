from .models import Approval

def get_notifications(request):
    notifications = None
    if request.user.is_authenticated:
        notifications = Approval.objects.filter(viewed=False).all()
        
    return {'notifications': notifications}
        
        