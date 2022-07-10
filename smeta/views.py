"""Here views lives"""
import io
from django.shortcuts import render
from django.http import FileResponse
from .forms import FileUploadForm
from .busines_logic.main import count_stage_load


def main_page_view(request):
    """Will render main page"""
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            buffer = io.BytesIO()
            work_book = count_stage_load(request.FILES['base_data'])
            work_book.save(buffer)
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='smeta_calculation.xlsx')
        ctx = {'form': form}
        return render(request, 'smeta/index.html', ctx)
    form = FileUploadForm()
    ctx = {'form': form}
    return render(request, 'smeta/index.html', ctx)
