from django.views.generic import TemplateView


class EvaluationLandingView(TemplateView):
    template_name = "evaluation_form.html"
