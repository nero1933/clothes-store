from rest_framework.reverse import reverse

from ecommerce.models import ProductVariation
from ecommerce.utils.tests.tests_mixins import TestAPIEcommerce


class TestShoppingCartItem(TestAPIEcommerce):

    def setUp(self):
        self.user = self.create_user()
        self.jwt_access_token = self.get_jwt_access_token()

        self.url_name = 'shopping_cart_items-list'
        self.url_name_detail = 'shopping_cart_items-detail'

    def test_authenticated_request(self):
        """
        Display shopping cart items only when authenticated request
        """
        response = self.client.get(reverse(self.url_name), format='json')
        self.assertEqual(response.status_code, 401, 'Shopping cart must not be displayed to unauthorized users')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.jwt_access_token)
        response = self.client.get(reverse(self.url_name), format='json')
        self.assertEqual(response.status_code, 200, 'Shopping cart must be displayed to authorized users')


    def test_duplicates(self):
        """
        There must not be the same 'product_variation_id' for
        different 'shopping_cart_item' objects in one cart
        """

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.jwt_access_token)

        # self.product_qs = self.create_products()
        self.create_products()

        product_variation = ProductVariation.objects \
            .select_related('product_item').values('pk', 'product_item__price').first()

        pk = product_variation['pk']
        price = product_variation['product_item__price']

        data = {
            'product_variation': pk,
            'quantity': 1
        }

        response = self.client.post(reverse(self.url_name), data, format='json')
        self.assertEqual(response.status_code, 201, 'Fist item must be created successfully')

        response = self.client.post(reverse(self.url_name), data, format='json')
        self.assertEqual(response.status_code, 201, 'Second item must be created successfully')

        response = self.client.get(reverse(self.url_name), data, format='json')
        self.assertEqual(response.status_code, 200, 'User must see his shopping cart')
        self.assertEqual(response.data[0]['quantity'], 2, "Item's quantity must be equal to 2")
        self.assertEqual(response.data[0]['item_price'], (2 * price), f"'item_price' must be equal to {(2 * price)}")
        self.assertEqual(len(response.data), 1, 'It must be only one item in the shopping cart')

        # Create new user
        self.create_user('user@user.user')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_jwt_access_token('user@user.user'))

        # Users must have different shopping carts
        response = self.client.get(reverse(self.url_name), format='json')
        self.assertEqual(response.status_code, 200, 'New user must see his shopping cart')
        self.assertEqual(len(response.data), 0, "New user's shopping cart must be empty")

    def test_max_quantity(self):
        """
        Quantity must not be greater than the 'qty_in_stock'
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.jwt_access_token)
        self.create_products()

        product_variation_qs = ProductVariation.objects \
            .select_related('product_item').values('pk', 'qty_in_stock')[:2]

        # Cache the query
        q = [x for x in product_variation_qs]
        qty_in_stock_1 = q[0]['qty_in_stock']
        qty_in_stock_2 = q[1]['qty_in_stock']

        data_1 = {
            'product_variation': q[0]['pk'],
            'quantity': 2 * qty_in_stock_1
        }

        data_2 = {
            'product_variation': q[1]['pk'],
            'quantity': 2 * qty_in_stock_2
        }

        def check_quantity():
            response = self.client.get(reverse(self.url_name), format='json')
            self.assertEqual(response.status_code, 200, 'Code must be 200')
            self.assertEqual(len(response.data), 2, 'In shopping cart must be two items')

            self.assertEqual(response.data[0]['quantity'],qty_in_stock_1,
                             f'Quantity must be equal to {qty_in_stock_1}')
            self.assertEqual(response.data[1]['quantity'], qty_in_stock_2,
                             f'Quantity must be equal to {qty_in_stock_2}')

        # When the first time items are added they will be created
        # Check that quantity after creation is not larger than qty_in_stock
        self.client.post(reverse(self.url_name), data_1, format='json')
        self.client.post(reverse(self.url_name), data_2, format='json')
        check_quantity()

        # When items which are already in the card are added second time they will be updated
        # Check that quantity after update is not larger than qty_in_stock
        self.client.post(reverse(self.url_name), data_1, format='json')
        self.client.post(reverse(self.url_name), data_2, format='json')
        check_quantity()

        # Check that quantity after update (using PATCH) is not larger than qty_in_stock
        response = self.client.get(reverse(self.url_name), format='json')
        kwargs_1 = {'pk': response.data[0]['id']}
        kwargs_2 = {'pk': response.data[1]['id']}

        response = self.client.patch(reverse(self.url_name_detail, kwargs=kwargs_1), data_1, format='json')
        self.assertEqual(response.status_code, 200, 'Code must be 200')

        response = self.client.patch(reverse(self.url_name_detail, kwargs=kwargs_2), data_2, format='json')
        self.assertEqual(response.status_code, 200, 'Code must be 200')

        check_quantity()

    def test_add_out_of_stock_item(self):
        """
        Items must not be added to shopping cart
        if qty_in_stock is 0
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.jwt_access_token)
        self.create_products()

        product_variation = ProductVariation.objects \
            .select_related('product_item').first()

        product_variation.qty_in_stock = 0
        product_variation.save()

        data = {
           "product_variation": product_variation.pk,
           "quantity": 1
        }

        response = self.client.post(reverse(self.url_name), data, format='json')
        self.assertEqual(response.status_code, 400, "Product can't be added due to out of stock")

        response = self.client.get(reverse(self.url_name), format='json')
        self.assertEqual(response.status_code, 200, 'Code must be 200')
        self.assertEqual(len(response.data), 0, 'Cart must be empty')

    def test_discount_price(self):
        """
        Apply discount 20% and 10% to product item
        Try to get 'item_price' and 'item_discount_price'
        'item_discount_price' must be ('price' - 30%) * quantity
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.jwt_access_token)
        self.create_products()
        discount_1 = self.create_discount(name='discount 1', discount_rate=10)
        discount_2 = self.create_discount(name='discount 2', discount_rate=20)

        product_variation = ProductVariation.objects \
            .select_related('product_item') \
            .prefetch_related('product_item__discount') \
            .first()

        product_variation.product_item.discount.set([discount_1, discount_2])
        product_price = product_variation.product_item.price

        # print()
        # print('product_variation')
        # print(product_variation)
        # print()
        # print('product_variation.pk', product_variation.pk)
        # print('product_price', product_price)
        # print()

        data = {
           "product_variation": product_variation.pk,
           "quantity": 10
        }

        response = self.client.post(reverse(self.url_name), data, format='json')
        self.assertEqual(response.status_code, 201, 'Product must be successfully added')

        # print()
        # print(response.data)
        # print()
        # print("response.data['id']", response.data['id'])
        # print("response.data['product_variation']", response.data['product_variation'])
        # print("response.data['quantity']", response.data['quantity'])
        # print("response.data['item_price']", response.data['item_price'])
        # print("response.data['item_discount_price']", response.data['item_discount_price'])
        # print()

        self.assertEqual(response.data['item_price'], (product_price * data['quantity']),
                         f"'item_price' must be {(product_price * data['quantity'])}"
                         f" but it is {response.data['item_price']}")

        self.assertEqual(response.data['item_discount_price'], int((product_price * 0.7)) * data['quantity'],
                         f"'discount_price' must be {int((product_price * 0.7)) * data['quantity']}"
                         f"but it is {response.data['item_discount_price']}")

        # test
