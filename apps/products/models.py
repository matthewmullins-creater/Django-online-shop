from django.db import models
from utils import FileUpload
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from middlewares.middlewares import RequestMiddleware
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum,Avg
#_______________________________________________________________

class Brand(models.Model):
    brand_title = models.CharField(max_length=100,verbose_name="Brand Name")
    file_upload = FileUpload('images','brand')
    image_name = models.ImageField(upload_to=file_upload.upload_to,verbose_name="Product Brand Image")
    slug=models.SlugField(max_length=200,null=True)

    def __str__(self):
        return self.brand_title
    
    class Meta:
        verbose_name="Brand"
        verbose_name_plural="Brands"

#_______________________________________________________________

class PoductGroup(models.Model):
    group_title = models.CharField(max_length=100,verbose_name="Product Group Title")
    file_upload = FileUpload(dir='images',prefix='product_group')
    image_name = models.ImageField(upload_to=file_upload.upload_to,verbose_name="عکس گروه کالا")
    description = models.TextField(verbose_name="توضیحات گروه کالا",blank=True,null=True)
    is_active = models.BooleanField(default=True,blank=True,verbose_name="Active / Inactive Status")
    group_parent = models.ForeignKey('PoductGroup',on_delete=models.CASCADE,blank=True,null=True,verbose_name="والدگروه کالا",related_name="groups")
    slug=models.SlugField(max_length=200,null=True)
    register_data=models.DateTimeField(auto_now=True,verbose_name="Registration Date")
    published_date=models.DateTimeField(default=timezone.now,verbose_name="Publication Date")
    update_date=models.DateTimeField(auto_now=True,verbose_name="Last Update Date")
    
    def __str__(self):
        return self.group_title
    
    class Meta:
        verbose_name="Product Group"
        verbose_name_plural="Product Groups"

#_______________________________________________________________

class Feature(models.Model):
    feature_name = models.CharField(max_length=100,verbose_name="Feature Name")
    product_group = models.ManyToManyField(PoductGroup,verbose_name="Product Group",related_name="features_of_group")
    
    def __str__(self):
        return self.feature_name
    
    class Meta:
        verbose_name = "Feature"
        verbose_name_plural = "Features"


#_______________________________________________________________

class Product(models.Model):
    produce_name = models.CharField(max_length=500,verbose_name="Product Name")
    summery_description = models.TextField(default="",null=True,blank=True)
    description = RichTextUploadingField(default="",config_name='special',blank=True)
    file_upload = FileUpload('images','product')
    image_name = models.ImageField(upload_to=file_upload.upload_to,verbose_name="Product Image")
    price=models.PositiveIntegerField(default=0,verbose_name="Product Price")
    product_group = models.ManyToManyField(PoductGroup,verbose_name="Product Group",related_name="products_of_group")
    features=models.ManyToManyField(Feature,through="ProductFeature")
    brand = models.ForeignKey(Brand,verbose_name="Product Brand",on_delete=models.CASCADE,null=True,related_name="product_of_brands")
    is_active = models.BooleanField(default=True,blank=True,verbose_name="Active / Inactive Status")
    slug=models.SlugField(max_length=200,null=True)
    register_data=models.DateTimeField(auto_now=True,verbose_name="Registration Date")
    published_date=models.DateTimeField(default=timezone.now,verbose_name="Publication Date")
    update_date=models.DateTimeField(auto_now=True,verbose_name="Last Update Date")
    
    def __str__(self):
        return f'{self.produce_name}'
    
    def get_absolute_url(self):
        return reverse("products:product_details", kwargs={"slug": self.slug})
    
    # قیمت با تخفیف کاالا
    def get_price_by_discount(self):
        list1=[]
        for dbd in self.discount_basket_details_product.all():
            if (dbd.discount_basket.is_active == True and 
                dbd.discount_basket.start_date <= timezone.now() and
                timezone.now() <= dbd.discount_basket.end_data):
                list1.append(dbd.discount_basket.discount)
                
        discount=max(list1) if (len(list1)>0) else 0
        Price_after_discount = self.price-(self.price*discount/100)
        return Price_after_discount
    
    # خودش چون توی پروداکت نوشته شده محصول جاری رو حساب میکنه
    def get_number_in_warehouse(self):
        # محاسبه ی تمام ورودی ها
        sum1 = self.warehouse_products.filter(warehouse_type_id=1).aggregate(Sum('qty'))
        # محاسبه ی تمام خروجی ها
        sum2 = self.warehouse_products.filter(warehouse_type_id=2).aggregate(Sum('qty'))
        
        input = 0
        if sum1['qty__sum']!=None:
            input=sum1['qty__sum']
        output = 0
        if sum2['qty__sum']!=None:
            output=sum2['qty__sum']
            
        return input - output
    
    def getMainProductGroups(self):
        return self.product_group.all()[0].id
    
    # میزان امتیازی که کاربر جاری به این کالا داده
    def get_user_score(self):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        score = 0
        # یعنی امتیاز رو فقط واسه این کاربر برسی و فیلتر میکنه
        user_score = self.scoring_product.filter(scoring_user=request.user)
        if user_score.count() > 0:
            score = user_score[0].score
        return score

    # میانگین امتیازی که این کالا کسب کرده
    def get_average_score(self):
        avgScore = self.scoring_product.all().aggregate(Avg('score'))['score__avg']
        if avgScore == None:
            avgScore = 0
        return avgScore
    
    # ایا این کالا مورد علاقه کاربر جاری بوده یا خیر
    def get_user_favorite(self):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        flag=self.favorite_product.filter(favorite_user=request.user).exists()
        return flag
     
    # تابع برای برگرداندن گروه اصلی کالا
    def getMinProducGroups(self):
        return self.product_group.all()[0].id
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = "Products"

#_______________________________________________________________
class FeatureValue(models.Model):
    value_title = models.CharField(max_length=100,verbose_name='Value Title')
    feature = models.ForeignKey(Feature,on_delete=models.CASCADE,blank=True,null=True,verbose_name="Feature",related_name="feature_values")
    
    def __str__(self):
        return f'{self.id} {self.value_title}'
    
    class Meta:
        verbose_name = 'Feature Value'
        verbose_name_plural = 'Feature Values'

#_______________________________________________________________
class ProductFeature(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Product",related_name='product_features')
    feature = models.ForeignKey(Feature,on_delete=models.CASCADE,verbose_name="Feature")
    value = models.CharField(max_length=100,verbose_name="Product Feature Value")
    filter_value = models.ForeignKey(FeatureValue,null=True,blank=True,on_delete=models.CASCADE,verbose_name="Feature Value for Filter")
    
    def __str__(self):
        return f"{self.product} - {self.feature} : {self.value}"
    
    class Meta:
        verbose_name = 'Product Feature'
        verbose_name_plural = "Product Features"
#_______________________________________________________________
class ProductGallery(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Product",related_name="gallery_images")
    file_upload = FileUpload('images','product_gallery')
    image_name = models.ImageField(upload_to=file_upload.upload_to,verbose_name="Product Image")
    