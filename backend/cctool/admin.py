from django.contrib import admin
from  cctool.models import Graph


class GraphAdmin(admin.ModelAdmin):
	"""
	Customize the Graph page for the admin page.
	"""
	list_display  = ('title', 'owner', 'dateadded', 'dateupdated')
	list_filter   = ['owner']
	search_fields = ['title']

# Add Graph to admin page.
admin.site.register(Graph, GraphAdmin)
