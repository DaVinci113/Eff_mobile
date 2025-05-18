from django.contrib import admin
from .models import Ad, ExchangeProposal, Category

# Register your models here.
admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(ExchangeProposal)

