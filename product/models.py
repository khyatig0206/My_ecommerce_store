from django.db import models
from base.models import BaseModel
# Create your models here.
from django.utils.text import slugify

class Category(BaseModel):
    category_name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True,null=True,blank=True)
    category_image=models.ImageField(upload_to="categories")

    def save(self,*args,**kwargs):
        self.slug=slugify(self.category_name)
        super(Category,self).save(*args,**kwargs)

    def __str__(self) -> str:
        return self.category_name

class ColorVariant(BaseModel):
    color=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.color

class SizeVariant(BaseModel):
    size=models.CharField(max_length=100)
    price=models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.size


class Product(BaseModel):
    product_name= models.CharField(max_length=100)
    slug=models.SlugField(unique=True,null=True,blank=True)
    category= models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    price= models.IntegerField()
    product_desc= models.TextField()
    color_variant=models.ManyToManyField(ColorVariant,blank=True)
    size_variant=models.ManyToManyField(SizeVariant,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
            original_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name

    def get_product_price_by_size(self, size):
        size_variant = self.size_variant.get(size=size)  # Fetch the size variant related to this product
        return self.price + size_variant.price

class ProductImage(BaseModel):
    product= models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_images")
    image= models.ImageField(upload_to="product")
    color = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name="product_images")
    
    def __str__(self) -> str:
        return f"{self.product.product_name} - {self.color.color if self.color else 'No Color'}"
    