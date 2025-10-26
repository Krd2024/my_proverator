from django.db import models

# Create your models here.
class Domain(models.Model):
    domain = models.URLField(verbose_name="Домен", max_length=200,unique=True)

    class Meta:
        verbose_name = "Домен"
        verbose_name_plural = "Домены"


    def __str__(self):
        return self.domain

class Request(models.Model):
    domain = models.ForeignKey(Domain, verbose_name="Домен", on_delete=models.CASCADE)
    status_code=models.IntegerField(verbose_name="Статус код")
    response_time=models.BigIntegerField(verbose_name="Время ответа")
    verified_at  = models.DateTimeField(auto_now_add=True,verbose_name="Дата и время проверки")

    class Meta:
        verbose_name = "Запрос"
        verbose_name_plural = "Запросы"

    def __str__(self):
        return f"{self.domain} - {self.status_code}"
