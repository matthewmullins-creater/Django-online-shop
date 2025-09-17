from django.db import models
from utils import FileUpload
from django.utils import timezone
from django.utils.html import mark_safe
# Multiple texts might be placed on the slider, so I placed 3 slider titles for this purpose
# slider_link : slider can be clicked
class Slider(models.Model):
    slider_title1 = models.CharField(max_length=500,null=True,blank=True,verbose_name="First Text")
    slider_title2 = models.CharField(max_length=500,null=True,blank=True,verbose_name="Second Text")
    slider_title3 = models.CharField(max_length=500,null=True,blank=True,verbose_name="Third Text")
    
    file_upload = FileUpload('images','slides')
    image_name = models.ImageField(upload_to=file_upload.upload_to,verbose_name="Slider Image")
    
    slider_link = models.URLField(max_length=200,null=True,blank=True,verbose_name="Link")
    
    is_active = models.BooleanField(default=True,blank=True,verbose_name="Active/Inactive Status")
    
    register_date = models.DateTimeField(auto_now_add=True,verbose_name="Registration Date")
    publish_date = models.DateTimeField(default=timezone.now,verbose_name="Publication Date")
    update_date = models.DateTimeField(auto_now=True,verbose_name="Last Update Date")
    
    def __str__(self):
        return f"{self.slider_title1}"
    
    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"
        
    # Writing code to display image in admin panel
    # mark_safe : receives an HTML code as a string and executes it
    def image_slide(self):
        return mark_safe(f'<img src="/media/{self.image_name}" style="width:80px; height:80px"/>')
    
    image_slide.short_description = "Slide Image"
    
    
    # I want the slider link to be clickable from the admin panel as well
    def link(self):
        return mark_safe(f'<a href="{self.slider_link} target="_blank">link</a>')
    
    link.short_description = 'Links'