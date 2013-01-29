from django.views.generic import FormView
from core.forms import SampleSearchForm


class SampleSearchView(FormView):
    template_name = "home.html"
    form_class = SampleSearchForm

    def form_valid(self, form):
        """Show the results that will be used in tests"""
        return self.render_to_response(self.get_context_data(form=form, success='SUCCESS'))
