# Trong tệp context_processors.py của ứng dụng Django của bạn
from django.contrib.messages import get_messages

def messages(request):
    return {
        'messages': get_messages(request),
    }
