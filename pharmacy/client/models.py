from django.db import models
from main.models import CustomUser
from pharmacist.models import Medicine


class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True)
    address = models.CharField(max_length=255, null=True)
    phone = models.PositiveIntegerField(null=True)


    def __str__(self):
        return self.user.first_name
    



class Cart(models.Model):
    user = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='cart')
    total_price = models.PositiveIntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.user.user.username} - {self.total_price}"


    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True, related_name='items')
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self) -> str:
        return f"{self.medicine.name} - {self.quantity}"


    # def increase_quantity(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     self.quantity += 1
    #     self.cart.total_price += self.product.price
    #     self.cart.save()
    #     super().save(force_insert, force_update, using, update_fields)
        

    # def decrease_quantity(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     self.quantity -= 1
    #     self.cart.total_price -= self.product.price
    #     self.cart.save()
    #     super().save(force_insert, force_update, using, update_fields)


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.cart.total_price += self.medicine.price
        self.cart.save()
        super().save(force_insert, force_update, using, update_fields)
    

    # def delete(self, using=None, keep_parents=False):
    #     self.cart.total_price -= self.product.price * self.quantity
    #     self.cart.save()
    #     return super().delete(using, keep_parents)


    # def get_item_price(self):
    #     if self.product:
    #         return self.product.price * self.quantity
    #     return 0

    


