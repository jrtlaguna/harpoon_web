from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from authentication.decorators import anonymous_required
from core.models import Document


@anonymous_required
def home_page(request: HttpRequest) -> HttpResponse:
    ctx = {"page": "home"}
    return render(request, "core/home_page.html", ctx)


@anonymous_required
def features_page(request: HttpRequest) -> HttpResponse:
    ctx = {"page": "feature"}
    return render(request, "core/features.html", ctx)


@anonymous_required
def about_page(request: HttpRequest) -> HttpResponse:
    ctx = {"page": "about"}
    return render(request, "core/about.html", ctx)


@anonymous_required
def contact_us_page(request: HttpRequest) -> HttpResponse:
    ctx = {"page": "contact"}
    return render(request, "core/contact_us.html", ctx)


@anonymous_required
def login_page(request: HttpRequest) -> HttpResponse:
    ctx = {"page": "login"}
    return render(request, "core/login.html", ctx)


def download_file(request: HttpRequest, document_id: int) -> HttpResponse:

    document_obj = Document.objects.get(id=document_id)
    filename = document_obj.document.name.split("/")[-1]
    response = HttpResponse(document_obj.document, content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response


def remove_document(request: HttpRequest, document_id: int) -> HttpResponse:
    try:
        Document.objects.get(id=document_id).delete()
        return JsonResponse(
            {"message": f"Successfully deleted document with id {document_id}"}
        )
    except Document.DoesNotExist as err:
        print(err)
        return JsonResponse({"message": "An error occured."})
