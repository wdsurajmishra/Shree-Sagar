from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as OriginalFlatPageAdmin
from .forms import FlatPageForm  # Import your custom form
from django.contrib.flatpages.models import FlatPage
from .models import Slider, Home, VideoCallBooking, Faq

admin.site.unregister(FlatPage)

@admin.register(FlatPage)
class FlatPageAdmin(OriginalFlatPageAdmin):
    form = FlatPageForm

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'image')    

@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')    


    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
@admin.register(VideoCallBooking)
class VideoCallAdmin(admin.ModelAdmin):
    list_display= ['name', 'phone', 'date', 'slot', 'created_at']

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display= ['question', 'position', 'created_at']