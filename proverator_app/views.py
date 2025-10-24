from django.shortcuts import redirect, render
import idna
from loguru import logger
from .forms import DomainForm
from django.contrib import messages


def domain_view(request):
    errors = []
    value = ""
    result = None

    if request.method == "POST":
        value = request.POST.get("domain", "")
        form = DomainForm({"domain": value})
        if form.is_valid():
            domain = form.cleaned_data["domain"]
            # Вернёт читабельный вид, если домен - рф
            try:
                my_domain = idna.decode(domain)
            except idna.IDNAError:
                my_domain = domain  

            result = f"✅ Домен '{my_domain}' выглядит корректно."
            messages.success(request, f"✅ Домен '{my_domain}' успешно добавлен!")

            logger.debug(result)
        else:
            errors = form.errors.get("domain", [])
            result = "❌ Ошибка: проверьте введённое значение."
            for error in errors:
                messages.error(request, f"❌ {error}")
            logger.debug(result)
    return redirect("/" )
    return render(request, "domain_form.html", {"errors": errors, "value": value, "result": result})


def chunk_history(history, parts=12):
    """Разбивает список history на Х примерно равных частей."""
    
    if not history:
        return [[] for _ in range(parts)]

    chunk_size = len(history) // parts or 1
    chunks = [history[i : i + chunk_size] for i in range(0, len(history), chunk_size)]
    return chunks
    return chunks[:parts]


test = ["up", "down"] * 200 + [None]


def monitor(request,domain_id:int=None):
    """Отображант по-умолчанию данные проверки по последнему добавленному домену"""

    context = {
        "domain": "example.com",
        "status_code": 0,
        "response_time": 0,
        "uptime_percent": 0,
        "last_check_time": "00:00:00",
        "url": "https://example.com",
        "is_up": True,
        "history": chunk_history(test),
    }
    return render(request, "monitor.html", context)
