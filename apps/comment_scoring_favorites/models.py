from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser
from django.core.validators import MinValueValidator,MaxValueValidator

# ---------------------------------------------------------------------------------------------

# approving_user : comments are not active by default and must be approved
# comment_parent : includes comments that are given to someone else's comment

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='comments_product',verbose_name='Product')
    commenting_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='comments_user1',verbose_name='Commenting User')
    approving_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='comments_user2',verbose_name='Comment Approving User',null=True,blank=True)
    comment_text = models.TextField(verbose_name='Comment Text')
    registerdate = models.DateTimeField(auto_now_add=True,verbose_name='Comment Registration Date')
    is_active = models.BooleanField(default=False,verbose_name='Comment Status')
    comment_parent = models.ForeignKey('Comment',on_delete=models.CASCADE,null=True,blank=True,verbose_name='Comment Parent',related_name='comment_child')
    
    def __str__(self):
        return f"{self.product} - {self.commenting_user}"
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

# ---------------------------------------------------------------------------------------------

# scoring

class Scoring(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='scoring_product',verbose_name='Product')
    scoring_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='scoring_user',verbose_name='Scoring User')
    registerdate = models.DateTimeField(auto_now_add=True,verbose_name='Registration Date')
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)],verbose_name='Score')
    
    def __str__(self):
        return f"{self.product} - {self.scoring_user}"
    
    class Meta:
        verbose_name = 'Score'
        verbose_name_plural = 'Scores'

# ---------------------------------------------------------------------------------------------

class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='favorite_product',verbose_name='Product')
    favorite_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='favorite_user',verbose_name='Favorite User')
    registerdate = models.DateTimeField(auto_now_add=True,verbose_name='Registration Date')
    
    def __str__(self):
        return f"{self.product} - {self.favorite_user}"
    
    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'