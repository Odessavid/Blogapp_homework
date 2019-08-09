from .models import *

def my_func(request):
    if request.user.is_active:
        count = request.user.user_r.filter(read=False).count()
    else:
        count=0
    return {'count':count}

