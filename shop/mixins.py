from datetime import datetime

class IsAuthenticatedMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_time"] = datetime.now()
        context["is_authenticated"] = self.request.user.is_authenticated
        return context