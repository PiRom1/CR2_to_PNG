from django.urls import path

from . import views

urlpatterns = [
    path("import", views.import_photos, name="import"),
    path("convert", views.convert, name="convert"),
    path("download", views.download_zip, name="download"),
]