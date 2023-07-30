from django.contrib import admin
from django.urls import path

from api.views import insertToMySQL, ExperimentsView, ExperimentsListView, ExpStatisticView, ExpDatasetAndRatioView, ExperimentsDetailView, PerExpStatisticView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ins2mysql/', insertToMySQL.as_view()),
    path('experiments/', ExperimentsView.as_view()),
    path('experiment_list/', ExperimentsListView.as_view()),
    path('experiment_detail/', ExperimentsDetailView.as_view()),
    path('exp_dataset/', ExpDatasetAndRatioView.as_view()),
    path('exp_statistic/', ExpStatisticView.as_view()),
    path('exp_per_statistic/', PerExpStatisticView.as_view()),
]
