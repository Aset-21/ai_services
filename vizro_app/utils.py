import json, uuid
from pathlib import Path
from django.conf import settings

def generate_dashboard(data_json: dict) -> str:
    dash_id = str(uuid.uuid4())
    path = Path(settings.DASHBOARD_DIR)
    path.mkdir(parents=True, exist_ok=True)
    with open(path / f"{dash_id}.json", "w", encoding="utf-8") as f:
        json.dump(data_json, f, ensure_ascii=False, indent=2)
    return dash_id
