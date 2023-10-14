import os
from django.http import FileResponse, Http404
from django.conf import settings


def download_file(request, file_name):
    safe_folder = os.path.join(settings.BASE_DIR, "classifier/safe_folder")

    if os.path.isabs(file_name) or file_name != os.path.basename(file_name):
        raise Http404("Invalid file name")

    file_path = os.path.join(safe_folder, file_name)

    if not os.path.commonprefix([file_path, safe_folder]) == safe_folder:
        raise Http404("File not found")

    if not os.path.exists(file_path):
        raise Http404("File not found")

    file = open(file_path, "rb")
    response = FileResponse(file, as_attachment=True, filename=file_name)
    return response
