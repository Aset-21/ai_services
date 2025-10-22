from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI

# импортируем роутеры
from docx_generate.api import router as docx_router
from vizro_app.api import router as dashboard_router
from vizro_app import views

# один общий NinjaAPI
api = NinjaAPI(title="AI Services API")

# добавляем оба подроутера
api.add_router("/docx/", docx_router)
api.add_router("/dashboard/", dashboard_router)

# маршруты Django
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("dashboard/<uuid>/", views.show_dashboard),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)