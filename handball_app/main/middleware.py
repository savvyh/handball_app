from django.shortcuts import redirect

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.profile_completed and request.path != '/profiles/create/':
            return redirect('create_profile')
        response = self.get_response(request)
        return response
