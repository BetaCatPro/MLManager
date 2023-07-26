from django.contrib import admin
from django.urls import path

from api.views import insertToMySQL, ExperimentsView, ExperimentsListView, ExpMetricsView, ExpParametersView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ins2mysql/', insertToMySQL.as_view()),
    path('experiments/', ExperimentsView.as_view()),
    path('experiment_list/', ExperimentsListView.as_view()),
    path('exp_parameters/', ExpParametersView.as_view()),
    path('exp_metrics/', ExpMetricsView.as_view()),
]
