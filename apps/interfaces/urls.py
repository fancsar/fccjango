from django.urls import path
from .views import InterfanceList
from rest_framework import routers

# urlpatterns = [
#     path('interfaces/', InterfanceList.as_view()),
#     path('interfaces/<int:pk>/', InterfacesDetail.as_view())
# ]
router = routers.SimpleRouter()
router.register(r'interfaces', InterfanceList)
urlpatterns = []
urlpatterns += router.urls
