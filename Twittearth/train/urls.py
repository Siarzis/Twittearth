from django.urls import path

from . import views
from train.views import Classifier

urlpatterns = [
    path('', Classifier.as_view(), name='classifier'),
]
