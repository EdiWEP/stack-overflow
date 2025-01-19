from django.urls import path
from .views import CodeRunView

urlpatterns = [
    path("run/<str:language>/", CodeRunView.as_view(), name="run_code")
]