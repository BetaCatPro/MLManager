from django.contrib import admin
from .models import AlgModels, AlgExperiments, AlgExperimentsList, AlgMetrics, AlgParameters

# Register your models here.

admin.site.register(AlgModels)
admin.site.register(AlgExperiments)
admin.site.register(AlgMetrics)
admin.site.register(AlgParameters)
admin.site.register(AlgExperimentsList)
