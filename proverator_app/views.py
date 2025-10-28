from django.shortcuts import redirect, render
import idna
from loguru import logger

from proverator_app.models import Domain, Request
from proverator_app.services.db import add_domain, get_domain
from proverator_app.services.util import chunk_history
from .forms import DomainForm, DomainSelectForm
from django.contrib import messages


def domain_view(request):
    """Добавить домен в БД для мониторинга"""
    
    errors = []
    value = ""
    result = None

    if request.method == "POST":
        value = request.POST.get("domain", "")
        form = DomainForm({"domain": value})
        if form.is_valid():
            domain = form.cleaned_data["domain"]
            url_prefix = form.cleaned_data["url_prefix"]

            logger.debug(url_prefix)

            # Вернёт читабельный вид, если домен - рф
            try:
                my_domain = idna.decode(domain)
            except idna.IDNAError:
                my_domain = domain


            result:dict[str,str]= add_domain(f"{url_prefix}{my_domain}")

            if result["results"]:
                messages.success(request, result.get("message"))
            else:
                messages.error(request, result.get("message"))

            logger.debug(result)
        else:
            errors = form.errors.get("domain", [])
            result = "❌ Ошибка: проверьте введённое значение."
            for error in errors:
                messages.error(request, f"❌ {error}")
            logger.debug(result)
    return redirect("/")



def monitor(request):
    """Отображант по-умолчанию данные проверки по первому добавленному домену"""
    if request.method == "POST":
        context = get_domain(request.POST.get("domain"))
    else:
        context = get_domain()

    context["form"] = DomainSelectForm()

    # logger.debug(context)
    return render(request, "monitor.html", context)
