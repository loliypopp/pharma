from django.db import models
from main.models import CustomUser
from django.utils.text import slugify
from transliterate import detect_language
from transliterate import slugify as tr_slugify
from geopy.geocoders import Nominatim

"""PHARMA"""

class Pharmacy(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название аптеки', unique=True)
    image = models.ImageField(upload_to='pharmacy/')
    address = models.CharField(max_length=255, verbose_name='Адрес аптеки')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона аптеки')
    slug = models.SlugField(unique=True, blank=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Преобразуем строку адреса в координаты
        if not (self.latitude and self.longitude):
            geolocator = Nominatim(user_agent="pharmacist")
            location_data = geolocator.geocode(self.address)
            if location_data:
                self.latitude = location_data.latitude
                self.longitude = location_data.longitude

        super().save(*args, **kwargs)

    # def set_location(self, latitude, longitude):
    #     self.location = Point(longitude, latitude)
    #     self.save()



class Pharmacist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    expirience = models.PositiveIntegerField()
    license_number = models.PositiveIntegerField()
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'{self.user.first_name} - {self.user.last_name}'


"""MEDICINE"""


class Medicine(models.Model):
    pharmacies = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='medicine_images/')
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.PositiveBigIntegerField()
    quantity = models.PositiveBigIntegerField()
    type_of_med = models.CharField(max_length=255)
    manuf_date = models.DateField(auto_now_add=True)
    usage = models.CharField(max_length=255)
    indications = models.CharField(max_length=255)


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        str_ = f"{self.name}-{self.type_of_med}-{self.price}"
        if detect_language(str_) == 'ru':
            str_ = tr_slugify(str_)
            self.slug = str_
        else:
            self.slug = slugify(str_)
        if not self.image:
            self.image = '/images/crying_cat.jpg'
        return super().save(force_insert, force_update, using, update_fields)


    def __str__(self) -> str:
        return f'{self.name} - {self.price}'