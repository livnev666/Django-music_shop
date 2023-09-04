from decimal import Decimal
from django.conf import settings
from magazine.models import Product


class Cart(object):

    # 1
    def __init__(self, request):
        """
        Инициализация корзины
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохраняем ПУСТУЮ карзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # 5
    def __iter__(self):
        """
        Перебираем товар в корзине и получаем товары из БД
        """
        product_ids = self.cart.keys()
        # получаем товары и добавляем его в корзину
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # 6
    def __len__(self):
        """
        считаем сколько товаров в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    # 2
    def product_add(self, product, quantity=1, update_quantity=False):
        """
        Добавляем товар в корзину или обновляем его количество
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    #3
    def save(self):
        # Сохраняем товар
        self.session.modified = True

    # 4
    def remove(self, product):
        # Удаление товара
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # 7
    def get_total_price(self):
        #  получаем общую стоимость товаров
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    # 8
    def clear_cart(self):
        # очищаем корзину
        del self.session[settings.CART_SESSION_ID]
        self.save()