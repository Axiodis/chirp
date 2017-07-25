from django.contrib import admin

# Register your models here.
from message.models import Message, Follow

admin.site.register(Message)
admin.site.register(Follow)