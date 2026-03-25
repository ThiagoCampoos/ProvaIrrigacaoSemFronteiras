from django.db import models


class BaseModel(models.Model):
    """Modelo base abstrato com campos de auditoria e formatacao padrao de datas."""

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Atualizado em")

    @property
    def formatted_created_at(self):
        """Retorna a data de criacao no formato DD/MM/YYYY para exibicao."""
        return self.created_at.strftime("%d/%m/%Y")

    @property
    def formatted_updated_at(self):
        """Retorna a data de atualizacao no formato DD/MM/YYYY para exibicao."""
        return self.updated_at.strftime("%d/%m/%Y")

    class Meta:
        abstract = True
