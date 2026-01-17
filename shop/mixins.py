from datetime import datetime

from django.shortcuts import redirect


class IsAuthenticatedMixin:
    login_url = "login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_time"] = datetime.now()
        context["is_authenticated"] = self.request.user.is_authenticated
        return context
