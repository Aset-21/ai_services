import sys, subprocess, socket
from pathlib import Path
from django.http import JsonResponse, HttpResponseNotFound
from django.conf import settings


running_dashboards = {}   # uuid → port

def show_dashboard(request, uuid):
    json_path = Path(settings.DASHBOARD_DIR) / f"{uuid}.json"
    if not json_path.exists():
        return HttpResponseNotFound("Dashboard not found")


    if uuid in running_dashboards:
        port = running_dashboards[uuid]
    else:

        s = socket.socket()
        s.bind(("", 0))
        port = s.getsockname()[1]
        s.close()


        subprocess.Popen([
            sys.executable, "-c",
                    f"""
import json, pandas as pd
from vizro import Vizro
from vizro.managers import data_manager
from vizro.models import Dashboard

with open(r"{json_path}", "r", encoding="utf-8") as f:
    cfg = json.load(f)
df = pd.DataFrame(cfg["data"])
for c in df.columns:
    try:
        df[c] = pd.to_datetime(df[c], format="%Y-%m-%d")
    except Exception:
        pass
data_manager["data"] = df
Vizro().build(Dashboard(**cfg["config"])).run(port={port})
        """
        ])

        running_dashboards[uuid] = port

    return JsonResponse({
        "message": "Dashboard is running",
        "url": f"http://127.0.0.1:{port}"
    })


