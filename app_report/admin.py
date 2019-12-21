from django.contrib import admin
from app_report.models import Report
from app_report.models import ReportFile
#admin.AdminSite.site_header =  ""
#admin.AdminSite.site_title = "ecustPrint"
# Register your models here.

class ReportFileInline(admin.TabularInline):
    model = ReportFile
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    inlines = [ReportFileInline,]
    list_display = ("user","username","title","time","files",)
    def username(self,obj):
        user = obj.user
        return user.first_name

    def files(self,obj):
        file_list = ReportFile.objects.filter(report=obj)
        s = ""
        for each in file_list:
            s = s + "%s\n"%(each.file.file)
        return s

@admin.register(ReportFile)
class ReportFileAdmin(admin.ModelAdmin):
    pass

