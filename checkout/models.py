# coding=utf-8
from django.db import models
from django.conf import settings

class CartItemManager(models.Manager):
    '''
        Gerenciador do carrinho de compras
    '''
    def add_item(self, cart_key, product):
        if self.filter(cart_key=cart_key, product=product).exists():
            created = False
            cart_item = self.get(cart_key=cart_key, product=product)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        else:
            created = True
            cart_item = CartItem.objects.create(
                cart_key=cart_key, product=product, price=product.price
            )
        return cart_item, created


class CartItem(models.Model):
    '''
        Carrinho de compras
    '''
    cart_key = models.CharField(
        'Chave do Carrinho', max_length=40, db_index=True
    )
    product = models.ForeignKey('catalog.Product', verbose_name='Produto')
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', max_digits=8, decimal_places=2)

    objects = CartItemManager()

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens dos Carrinhos'
        # Para não permitir a duplicação de produtos no carrinho
        unique_together = (('cart_key', 'product'),)

    def __str__(self):
        return '{} [{}]'.format(self.product, self.quantity)


class OrderManager(models.Manager):
    '''
     Evitar ficando escrevendo muita lógica na view
    '''
    def create_order(self, user, cart_items):
        # cria o pedido
        order = self.create(user=user)
        for cart_item in cart_items:
            order_item = OderItem.objects.create(
                order=order, quantity=cart_item.quantity,
                product=cart_item.product, price=cart_item.price
            )
        return order


class Order(models.Model):
    '''
        Classe Pedido
    '''
    STATUS_CHOICES = (
        (0, 'Aguardando Pagamento'),
        (1, 'Concluída'),
        (2, 'Cancelada'),
    )

    PAYMENT_OPTION_CHOICES = (
        ('deposit', 'Depósito'),
        ('pagseguro', 'PagSeguro'),
        ('paypal', 'Paypal'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário')
    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICES, default=0, blank=True
    )
    payment_option = models.CharField(
        'Opção de Pagamento', choices=PAYMENT_OPTION_CHOICES,
        max_length=20, default='deposit'
    )
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    objects = OrderManager()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return 'Pedido #{}'.format(self.pk)



class OrderItem(models.Model):
    '''
        Classe item do pedido
    '''
    order = models.ForeignKey(Order, verbose_name='Pedido', related_name='items')
    # related_name, quando criado o objeto OrderItem ele cria um atributo chamado items
    # que retorna os itens do pedido
    product = models.ForeignKey('catalog.Product', verbose_name='Produto')
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens dos pedidos'

    def __str__(self):
        return 'Pedido: #{} Produto: {}'.format(self.order, self.product)



# signals para remove um item do carrinho caso a quantidade seja menor que 1 ao salvar
def post_save_cart_item(instance, **kwargs):
    if instance.quantity < 1:
        instance.delete()


'''
    Registro da função, sender indica que a função só será executada na instancia
    de CartItem.
'''
models.signals.post_save.connect(
    post_save_cart_item, sender=CartItem, dispatch_uid='post_save_cart_item'
)
