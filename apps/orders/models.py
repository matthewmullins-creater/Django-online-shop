from django.db import models
from apps.accounts.models import Customer
from apps.products.models import Product
from django.utils import timezone
import uuid
import utils
#______________________________________________________________________________________________________________________________
class PaymentType(models.Model):
    payment_title = models.CharField(max_length=32, verbose_name='Payment Method Type')
    def __str__(self):
        return self.payment_title
    class Meta:
        verbose_name='Payment Method Type'
        verbose_name_plural='Payment Method Types'

#______________________________________________________________________________________________________________________________

class Order(models.Model):
    Customer=models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='orders', verbose_name='Customer')
    register_date=models.DateField(default=timezone.now,verbose_name='Order Registration Date')
    update_date=models.DateField(auto_now=True, verbose_name='Order Update Date')
    is_finaly=models.BooleanField(default=True, verbose_name='Payment Status')
    oder_code=models.CharField(max_length=36,default=uuid.uuid4,unique=True,editable=False,verbose_name='Order Generation Code')
    discount=models.IntegerField(blank=True,null=True,default=0,verbose_name='Invoice Discount')
    description=models.TextField(blank=True,null=True,verbose_name='Description')
    payment = models.ForeignKey(PaymentType, on_delete=models.CASCADE, null=True,blank=True,related_name='pyman_types', verbose_name='Payment Method Type')
    def get_order_total_price(self):
        sum_=0
        for item in self.order_details1.all():
            sum_+=item.product.get_price_by_discount()*item.quantity
        order_final_price,delivery,tax=utils.price_by_delivery_tax(sum_,self.discount)
        return int((order_final_price)*10)

    def __str__(self):
        return f'{self.Customer}\t{self.id}\t{self.is_finaly}'
    class Meta:
        verbose_name='Order'
        verbose_name_plural='Orders'
#______________________________________________________________________________________________________________________________

class OrderDetails(models.Model):
    Order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details1', verbose_name='Order')
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_details2', verbose_name='Product')
    quantity=models.PositiveIntegerField(default=1,verbose_name='Product Quantity')
    price=models.IntegerField(verbose_name='Product Price')
    def __str__(self):
        return f'{self.Product}\t{self.price}\t{self.quantity}'
    class Meta:
        verbose_name='Order Details'
        verbose_name_plural='Order Details'