from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy
from smart_selects.db_fields import ChainedForeignKey

from acc.models import CustomUser


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
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.size

    def get_absolute_url(self):
        return reverse('gender', kwargs={'slug': self.slug})



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
    quantity = models.PositiveSmallIntegerField(default=0)
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
            discount = self.discount / 100
            self.final_price = (self.price - (self.price * discount)) // 100
            return int(self.final_price)
        return self.get_price()

    def save(self, *args, **kwargs):
        if self.item_category:
            self.item_type = self.item_category.type
        super().save(*args, **kwargs)


class ItemStock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE, null=True)
    size = ChainedForeignKey(ItemSize, chained_field='item_type',
                             chained_model_field='item_type',
                             show_all=False, auto_choose=True,
                             sort=True)
    quantity = models.IntegerField(validators=(not_negative, ))

    class Meta:
        unique_together = ('item', 'size',)

    def __str__(self):
        self.out_of_stock()
        return f"{self.item} {self.size}"

    def last_n_items_in_stock(self):
        if int(self.quantity) < 4:
            return f"Last {self.quantity} items in this size!"

    def out_of_stock(self):
        if int(self.quantity) == 0:
            return f"{self.item} {self.size} is currently out of stock"

    def save(self, *args, **kwargs):
        if self.quantity:
            self.item.quantity += self.quantity
            self.item.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.item.quantity -= self.quantity
        self.item.save()
        super(ItemStock, self).delete(*args, **kwargs)


class Cart(models.Model):
    session = models.CharField(unique=True, max_length=255, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    items = models.ManyToManyField(ItemStock, default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    have_been_bought = models.BooleanField(default=False)

    def __str__(self):
        if self.user:
            return f"{self.pk} {self.user}"
        return f"{self.pk} {self.session}"


class ItemInCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(ItemStock, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(null=True, default=0)

    def __str__(self):
        return f"{self.cart} {self.item} {self.quantity}"

    def get_total(self):
        total = int(self.quantity) * self.item.item.get_final_price()
        return total