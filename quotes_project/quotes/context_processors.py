from .views import top_tags

def top_ten_tags(request):
    return top_tags(request)