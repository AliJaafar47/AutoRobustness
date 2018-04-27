from django.contrib import admin

from . models import Project , Class , Step , Test, Metric, Test_Result, Step_Result, Project_result


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name','classe')
    fields = ('name', 'classe')
    #filter_horizontal = ('classe',)
    
class StepAdmin(admin.ModelAdmin):
    list_display = ('step_number','name','description','test_list')
    fields = ('step_number','name', 'description','tests')
    filter_horizontal = ('tests',)
    ordering = ('step_number',)
    
    def test_list(self, obj):
        return ", ".join([p.name for p in obj.tests.all()])

class TestAdmin(admin.ModelAdmin):
    list_display = ('name','description','metrics_list')
    fields = ('name', 'description','metrics')
    filter_horizontal = ('metrics',)
    def metrics_list(self, obj):
        return ", ".join([p.name for p in obj.metrics.all()])
    
admin.site.register(Test, TestAdmin)   
admin.site.register(Project, ProjectAdmin)
admin.site.register(Class)
admin.site.register(Step, StepAdmin)
admin.site.register(Metric)
admin.site.register(Test_Result)
admin.site.register(Step_Result)
admin.site.register(Project_result)
#admin.site.register(Class)


