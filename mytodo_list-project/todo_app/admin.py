from django.contrib import admin
# importing Todo model
from .models import Todo

# to read the createdAt datetime of the Todos model:
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('createdAt',)

# Registering Todo model, passing the class to read
admin.site.register(Todo, TodoAdmin)

