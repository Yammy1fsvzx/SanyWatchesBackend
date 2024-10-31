from django.db import models

class CategoryManager(models.Manager):
    def create_category(self, name, description='', image=None):
        category = self.create(name=name, description=description, image=image)
        return category


class BrandManager(models.Manager):
    def create_brand(self, name, logo, header, description=''):
        brand = self.create(name=name, logo=logo, header=header, description=description)
        return brand


class ProductManager(models.Manager):
    def create_product(self, category, type, brand, name, reference_number, price, slug):
        product = self.create(category=category, type=type, brand=brand, name=name, reference_number=reference_number, price=price, slug=slug)
        return product

    def update_product(self, product_id, **kwargs):
        product = self.get(id=product_id)
        for key, value in kwargs.items():
            setattr(product, key, value)
        product.save()
        return product


# Подключаем менеджеры к моделям
class Category(models.Model):
    # ... (поля)
    objects = CategoryManager()


class Brand(models.Model):
    # ... (поля)
    objects = BrandManager()


class Product(models.Model):
    # ... (поля)
    objects = ProductManager()