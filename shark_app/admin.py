from django.contrib import admin
from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe
from .models import *



class NewsAdminForm(forms.ModelForm):

    body = forms.CharField(widget=CKEditorUploadingWidget(), label='Описание новости')

    class Meta:
        model = News
        fields = '__all__'


class ArchiveAdminForm(forms.ModelForm):

    description = forms.CharField(widget=CKEditorUploadingWidget(), label="Описание архива")

    class Meta:
        model = Archive
        fields = "__all__"

class NewsImageStackedInline(admin.TabularInline):

    model = Images
    extra = 1

class DocumentFileStackedInline(admin.TabularInline):

    model = Dock
    extra = 1


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    list_display = ("id", "date")
    list_display_links = ("id", "date")
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('date',"description")
    list_filter = ('created_at', 'updated_at')
    form = ArchiveAdminForm



@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
    list_display_links = ("id", "name")
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    inlines = [DocumentFileStackedInline,]



@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'category','get_image')
    list_display_links = ('id','name',)
    readonly_fields = ('created_at', 'updated_at', 'get_big_image')
    filter_horizontal = ('tags',)
    search_fields = ('name','tags', 'category')
    list_filter = ('category', 'created_at', 'updated_at')
    inlines = [NewsImageStackedInline,]
    form = NewsAdminForm


    @admin.display(description='Изображение')
    def get_image(self, item):
        if item.images.first():
            return mark_safe(f'<img src="{item.images.first().image.url}" width="100px">')
        return '-'
    
    @admin.display(description='Изображение')
    def get_big_image(self, item):
        if item.images.first():
            return mark_safe(f'<img src="{item.images.first().image.url}" width="100%">')
        return '-'
    
    
admin.site.register(Category)
admin.site.register(AiylKeneshi)
admin.site.register(Postanovlenie)
admin.site.register(Comment)
admin.site.register(Tags)
admin.site.register(Chapter)

# Register your models here.
