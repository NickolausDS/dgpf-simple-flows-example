from django.urls import include, path
from dgpf_flows_example import views

urlpatterns = [
    # Our custom views
    path("", views.index, name="index"),
    path("hello-flow/", views.hello_flow, name="hello-flow"),
    # Used for login/logout
    path("", include("globus_portal_framework.urls")),
    path("", include("social_django.urls", namespace="social")),
]
