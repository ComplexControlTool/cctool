from django.contrib import admin

from .models.models import Graph, NodePlus, EdgePlus

admin.site.register(Graph)
admin.site.register(NodePlus)
admin.site.register(EdgePlus)