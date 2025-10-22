from ninja import Router, Schema
from django.conf import settings
from .utils import generate_dashboard
from .models import DashboardEntry
from ninja import Schema
from typing import List, Dict, Any


router = Router(tags=["Dashboard generate"])

from ninja import Schema
from typing import List, Dict, Any

class DashboardSchema(Schema):
    data: List[Dict[str, Any]]
    config: Dict[str, Any]

    class Config:
        schema_extra = {
            "example": {
                "data": [
                    {
                        "product": "Product A",
                        "sales": 1240,
                        "date": "2025-10-01"
                    }
                ],
                "config": {
                    "title": "Product Sales Dashboard",
                    "filters": [
                        {"name": "Date", "type": "date"},
                        {"name": "Product", "type": "dropdown"}
                    ]
                }
            }
        }


# 2️⃣ Эндпоинт с телом запроса
@router.post("/upload/", summary="Генерация дашборда")
def upload_dashboard(request, payload: DashboardSchema):
    data_json = payload.dict()
    dash_id = generate_dashboard(data_json)
    DashboardEntry.objects.create(
        uuid=dash_id,
        json_path=f"{settings.DASHBOARD_DIR}/{dash_id}.json"
    )

    url = f"http://127.0.0.1:8000/dashboard/{dash_id}/"
    return {"uuid": dash_id, "dashboard_url": url}

