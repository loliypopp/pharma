from django.db import models
from main.models import CustomUser
from pharmacist.models import Medicine, Pharmacy


class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True)
    address = models.CharField(max_length=255, null=True)
    phone = models.PositiveIntegerField(null=True)


    def __str__(self):
        return self.user.first_name
    


class Order(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.PositiveIntegerField(default=0)
    status_choices = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='PENDING')
    pharmacy = models.ForeignKey(Pharmacy, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}-{self.user.user.username}-{self.total_price}-{self.pharmacy}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.medicine.name}-{self.quantity}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        self.order.total_price += self.medicine.price * self.quantity
        self.order.save()

    def delete(self, using=None, keep_parents=False):
        self.order.total_price -= self.medicine.price * self.quantity
        self.order.save()
        return super().delete(using, keep_parents)

    def get_item_price(self):
        if self.medicine:
            return self.medicine.price * self.quantity
        return 0


class Cart(models.Model):
    user = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='cart')
    total_price = models.PositiveIntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.user.user.username}-{self.total_price}"
    

    def create_order(self):
        order = Order.objects.create(user=self.user, total_price=self.total_price)
        cart_items = self.cartitems.all()

        for cart_item in cart_items:
            OrderItem.objects.create(order=order, medicine=cart_item.medicine, quantity=cart_item.quantity)



    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True, related_name='items')
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self) -> str:
        return f"{self.medicine.name}-{self.quantity}"


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


    def get_item_price(self):
        if self.product:
            return self.product.price * self.quantity
        return 0

    



