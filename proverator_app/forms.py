from urllib.parse import urlparse
from django import forms
from loguru import logger
import tldextract
import idna
import re

DOMAIN_RE = re.compile(r"^[a-z0-9.-]+\.[a-z0-9-]{2,}$", re.IGNORECASE)


class DomainForm(forms.Form):
    domain = forms.CharField(max_length=255)

    def clean_domain(self):
        raw = self.cleaned_data["domain"].strip()
        logger.debug(f"Raw input: {raw}")

        # Если URL — достаём hostname
        if raw.startswith(("http://", "https://")):
            parsed = urlparse(raw)
            host = parsed.hostname
        else:
            host = raw

        if not host:
            raise forms.ValidationError("Не удалось определить домен.")

        host = host.lower().strip()

        # Конвертировать в punycode
        try:
            host_ascii = idna.encode(host).decode("ascii")
            logger.debug(f"Punycode: {host_ascii}")
        except idna.IDNAError:
            raise forms.ValidationError("Некорректный IDN-домен (проверьте символы).")

        # Проверить базовую структуру
        if not DOMAIN_RE.match(host_ascii):
            raise forms.ValidationError("Введите корректное доменное имя (пример: example.com).")

        # Проверить существование TLD
        ext = tldextract.extract(host_ascii)
        if not ext.suffix:
            raise forms.ValidationError("Некорректная доменная зона.")

        return host_ascii

      
    
