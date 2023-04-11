from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy


class ItemGender(models.Model):
    # example: For her/For him/Unisex/Kids
    gender = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.gender

    def get_absolute_url(self):
        return reverse('gender', kwargs={'slug': self.slug})


class ItemType(models.Model):
    # example: For her -> Clothes/Shoes/Accessories
    type = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse('type', kwargs={'slug': self.slug})


class ItemCategory(models.Model):
    # example: For her -> Clothes -> T-shirts
    category = models.CharField(max_length=30, unique=True)
    is_returnable = models.BooleanField(default=True)
    slug = models.SlugField(null=True)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class ItemSize(models.Model):
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE, default=None)
    size = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.size


class ItemBrandSegment(models.Model):
    brand_segment = models.CharField(max_length=25, unique=True, null=True)

    def __str__(self):
        return self.brand_segment


class ItemBrand(models.Model):
    brand = models.CharField(max_length=50, unique=True, null=True)
    segment = models.ManyToManyField(ItemBrandSegment)
    logo = models.ImageField(default=None)
    description = models.TextField(null=True, default=None)

    def __str__(self):
        return self.brand


class ItemMaterial(models.Model):
    material = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.material


class ItemColor(models.Model):
    color = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.color


class ItemSeason(models.Model):
    season = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.season


class ItemPicture(models.Model):
    name = models.CharField(null=True, max_length=255)
    picture = models.ImageField(upload_to='shop/static/shop/images/')

    def __str__(self):
        return str(f"{self.name} id={self.pk}")

    def get_url(self):
        return self.picture.url


def not_negative(value):
    if value < 0:
        raise ValidationError(
            gettext_lazy("Item price can't be lesser than 0"),
            params={"value": value},
        )


class Item(models.Model):
    # example: For her -> Clothes -> T-shirts -> T-shirt
    item_gender = models.ForeignKey(ItemGender, on_delete=models.CASCADE)
    item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    item_type = models.ForeignKey(ItemType, to_field='type',
                                  related_name='item_type', on_delete=models.CASCADE)
    item_brand = models.ForeignKey(ItemBrand, on_delete=models.CASCADE)
    item_material = models.ForeignKey(ItemMaterial, on_delete=models.CASCADE)
    item_color = models.ManyToManyField(ItemColor)
    item_season = models.ManyToManyField(ItemSeason)
    is_eco = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField(validators=(not_negative, ))
    on_sale = models.BooleanField(default=False)
    discount = models.IntegerField(default=0, validators=(not_negative, ))
    final_price = models.IntegerField(default=0, validators=(not_negative, ))
    quantity = models.IntegerField(validators=(not_negative, ), default=1)
    details = models.TextField(null=True, blank=True)
    pictures = models.ManyToManyField(ItemPicture, default=None)
    slug = models.SlugField(null=True)

    def clean(self):
        if not self.on_sale and self.discount > 0:
            raise ValidationError(gettext_lazy('Discount should be 0 when item is not on sale.'))
        if self.on_sale and self.discount < 1:
            raise ValidationError(gettext_lazy('Discount should be >0 when item is on sale.'))
        elif self.on_sale and self.discount > 1:
            self.final_price = self.get_final_price()

    def __str__(self):
        return self.name

    def get_price(self):
        return int(int(self.price) / 100)

    def get_absolute_url(self):
        return reverse('gender', kwargs={'slug': self.slug})

    def get_final_price(self):
        if self.on_sale:
            self.discount, self.price, self.final_price = int(self.discount), int(self.price), int(self.final_price)
            self.discount /= 100
            self.final_price = (self.price - (self.price * self.discount)) // 100
        return self.final_price

    def save(self, *args, **kwargs):
        if self.item_category:
            self.item_type = self.item_category.type
        super().save(*args, **kwargs)


class ItemStock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.ForeignKey(ItemSize, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=(not_negative, ))

    def last_n_items_in_stock(self):
        if int(self.quantity) < 4:
            return f"Last {self.quantity} items in this size!"

    def out_of_stock(self):
        if int(self.quantity) == 0:
            return f"This item is currently out of stock"


