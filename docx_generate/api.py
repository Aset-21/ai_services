from ninja import Router, File
from ninja.files import UploadedFile
from docx_generate.models import DocxTemplate
from django.contrib.auth.models import User
from .utils import generate_document
from ninja import Schema
from django.http import FileResponse, Http404
import os

router = Router(tags=["Docx generation"])

# ✅ Получение списка шаблонов
@router.get("/templates", summary="Получить список всех шаблонов")
def list_templates(request):
    return [
        {
            "uuid": str(t.id),
            "name": t.name,
            "created_at": t.created_at,
            "updated_at": t.updated_at,
            "author": t.author.username if t.author else None
        }
        for t in DocxTemplate.objects.all()
    ]

# ✅ Загрузка шаблона
@router.post("/upload", summary="Загрузить шаблон")
def upload_template(request, name: str, file: UploadedFile = File(...)):
    template = DocxTemplate.objects.create(
        name=name,
        file=file,
        author=request.user if request.user.is_authenticated else None
    )
    return {"uuid": str(template.id), "name": template.name}


class GenerateRequest(Schema):
    uuid: str
    data: dict

@router.post("/generate", summary="Генерация файла по шаблону")
def generate_doc(request, payload: GenerateRequest):
    try:
        template = DocxTemplate.objects.get(id=payload.uuid)
    except DocxTemplate.DoesNotExist:
        raise Http404("Template not found")

    output_path = generate_document(template.file.path, payload.data)
    return FileResponse(open(output_path, "rb"), as_attachment=True, filename=output_path.split("/")[-1])
