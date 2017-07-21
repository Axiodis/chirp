from django.contrib import admin

# Register your models here.
from message.models import Message


admin.site.register(Message)