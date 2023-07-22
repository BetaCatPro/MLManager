from django.contrib import admin
from django.urls import path

from api.views import ExperimentsView, ExperimentsListView, ExpMetricsView, ExpModelsView, ExpParametersView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('experiments/', ExperimentsView.as_view()),
    path('experiment_list/', ExperimentsListView.as_view()),
    path('exp_parameters/', ExpParametersView.as_view()),
    path('exp_metrics/', ExpMetricsView.as_view()),
    path('exp_models/', ExpModelsView.as_view()),
]
