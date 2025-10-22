from django.contrib import admin
from django.utils.html import format_html
from .models import DashboardEntry

@admin.register(DashboardEntry)
class DashboardEntryAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'dashboard_title', 'link_to_dashboard', 'link_to_json')

    def link_to_dashboard(self, obj):
        url = obj.dashboard_url()
        return format_html('<a href="{}" target="_blank">{}</a>', url, obj.uuid)
    link_to_dashboard.short_description = 'Дашборд'

    def link_to_json(self, obj):
        url = obj.json_url()
        return format_html('<a href="{}" target="_blank">JSON</a>', url)
    link_to_json.short_description = 'JSON файл'
