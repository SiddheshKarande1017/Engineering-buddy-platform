from django.contrib import admin
from django.contrib import admin
from .models import Problem
from .models import Sources

class ProblemAdmin(admin.ModelAdmin):
    list1=('ProblemID','Topic','ProblemName','ProblemLink')
class SourceAdmin(admin.ModelAdmin):
    list2=('SourceID','SourceTopic','SourceLink')

admin.site.register(Problem,ProblemAdmin)
admin.site.register(Sources,SourceAdmin)