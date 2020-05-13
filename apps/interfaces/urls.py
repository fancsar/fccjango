
from django.urls import path
from .views import InterfanceList,InterfacesDetail


urlpatterns = [
    path('interfaces/', InterfanceList.as_view()),
    path('interfaces/<int:pk>/', InterfacesDetail.as_view())
]
