from django.urls import include, path

from proverator_app.views import domain_view, monitor

urlpatterns = [
    path("",monitor,name="monitor"),
    path("submit-domain/",domain_view,name="add_domain")
]
