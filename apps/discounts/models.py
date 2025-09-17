from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.products.models import Product
#---------------------------------------------------------------------------------------------------------------------------
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10, unique=True,verbose_name="Coupon Code")
    start_date = models.DateTimeField(verbose_name="Start Date")
    end_data = models.DateTimeField(verbose_name="End Date")
    discount = models.IntegerField(verbose_name="Discount Percentage",validators=[MinValueValidator(0),MaxValueValidator(100)])
    is_active = models.BooleanField(default=False,verbose_name="Active Status")
    
    class Meta:
        verbose_name = "Discount Coupon"
        verbose_name_plural = "Coupons"
    
    def __str__(self):
        return self.coupon_code
#---------------------------------------------------------------------------------------------------------------------------
class DiscountBasket(models.Model):
    discount_title = models.CharField(max_length=100,verbose_name="Discount Basket Title")
    start_date = models.DateTimeField(verbose_name="Start Date")
    end_data = models.DateTimeField(verbose_name="End Date")
    discount = models.IntegerField(verbose_name="Discount Percentage",validators=[MinValueValidator(0),MaxValueValidator(100)])
    is_active = models.BooleanField(default=False,verbose_name="Active Status")
    
    class Meta:
        verbose_name = "Discount Basket"
        verbose_name_plural = "Discount Baskets"
    
    def __str__(self):
        return self.discount_title
#---------------------------------------------------------------------------------------------------------------------------
class DiscountBasketDetails(models.Model):
    discount_basket = models.ForeignKey(DiscountBasket,on_delete=models.CASCADE,verbose_name="Discount Basket",related_name="discount_basket_details")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Product",related_name="discount_basket_details_product")
    class Meta:
        verbose_name = "Discount Basket Details"