import json
from django.db import models

class DashboardEntry(models.Model):
    uuid = models.CharField(max_length=64, unique=True)
    json_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def dashboard_title(self):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # предполагается, что title находится в корне JSON
            return data.get('title', 'Без названия')
        except Exception:
            return 'Ошибка чтения'
    dashboard_title.short_description = 'Наименование дашборда'

    def dashboard_url(self):
        return f'/dashboard/{self.uuid}'
    dashboard_url.short_description = 'URL дашборда'
    dashboard_url.allow_tags = True

    def json_url(self):
        # ссылка для скачивания/просмотра JSON файла, например:
        return f'/media/dashboards/{self.uuid}.json'
    json_url.short_description = 'JSON файл'
    json_url.allow_tags = True
