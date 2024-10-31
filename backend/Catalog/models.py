from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"), blank=True)
    image = models.ImageField(upload_to='categories/', verbose_name=_("Image"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"), blank=True)

    def __str__(self):
        """
        Возвращает строковое представление объекта Category.

        Returns:
            str: Название категории.
        """
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Product Type"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        """
        Возвращает строковое представление объекта ProductType.

        Returns:
            str: Название типа продукта.
        """
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Brand Name"))
    logo = models.ImageField(upload_to='brands/', verbose_name=_("Logo"), blank=True)
    header = models.ImageField(upload_to='brands/headers/', verbose_name=_("Header"), blank=True)
    description = models.TextField(verbose_name=_("Description"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        """
        Возвращает строковое представление объекта Brand.

        Returns:
            str: Название бренда.
        """
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Currency Name"))
    symbol = models.CharField(max_length=10, verbose_name=_("Currency Symbol"))
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=_("Exchange Rate"),  default=1.0000)

    def __str__(self):
        """
        Возвращает строковое представление объекта Currency.

        Returns:
            str: Название валюты.
        """
        return self.name


class Parameter(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='parameters')
    name = models.CharField(max_length=255, verbose_name=_("Parameter Name"))

    def __str__(self):
        """
        Возвращает строковое представление объекта Parameter.

        Returns:
            str: Название параметра.
        """
        return self.name


class ProductParameter(models.Model):
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name=_("Value"))

    def __str__(self):
        """
        Возвращает строковое представление объекта ProductParameter.

        Returns:
            str: Строка формата "<название параметра>: <значение>".
        """
        return f"{self.parameter.name}: {self.value}"


class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', verbose_name=_("Image"), blank=True)
    order = models.IntegerField(default=0, verbose_name=_("Display Order"))

    def __str__(self):
        """
        Возвращает строковое представление объекта ProductImage.

        Returns:
            str: Описание изображения для товара.
        """
        return f"Image for {self.product.name}"


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Tag Name"))

    def __str__(self):
        """
        Возвращает строковое представление объекта Tag.

        Returns:
            str: Название тега.
        """
        return self.name


class ProductTag(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        """
        Возвращает строковое представление объекта ProductTag.

        Returns:
            str: Описание связи товара и тега.
        """
        return f"{self.product.name} - {self.tag.name}"


class Report(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    date = models.DateField(verbose_name=_("Date"))
    sales_count = models.IntegerField(verbose_name=_("Sales Count"), default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Revenue"), default=0)

    def __str__(self):
        """
        Возвращает строковое представление объекта Report.

        Returns:
            str: Описание отчета для товара на указанную дату.
        """
        return f"Report for {self.product.name} on {self.date}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    reference_number = models.CharField(max_length=100, unique=True, verbose_name=_("Reference Number"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    parameters = models.ManyToManyField(ProductParameter, related_name='products')

    def convert_price(self, currency):
        """
        Конвертирует цену товара в указанную валюту.

        Args:
            currency (Currency): Объект валюты для конверсии.

        Returns:
            Decimal: Конвертированная цена в указанной валюте.
        """
        return self.price * currency.exchange_rate

    def __str__(self):
        return self.name