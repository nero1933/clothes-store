from rest_framework.reverse import reverse

from ecommerce.models import ProductVariation
from ecommerce.utils.tests.tests_mixins import TestMixin


class TestShoppingCartItem(TestMixin):

    def setUp(self):
        self.user = self.create_user()
        self.jwt_access_token = self.get_jwt_access_token()
        #self.product_qs = self.create_products()
        #self.discount_1 = self.create_discount()
        #self.discount_2 = self.create_discount(name='discount 2', discount_rate=20)

        self.url_name = 'shopping_cart_items-list'

    def test_authenticated_request(self):
        response = self.client.get(reverse(self.url_name), format='json')
        self.assertEqual(response.status_code, 401, 'Shopping cart must not be displayed to unauthorized users')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.jwt_access_token)
        response = self.client.get(reverse(self.url_name), format='json')
        self.assertEqual(response.status_code, 200, 'Shopping cart must be displayed to authorized users')


    def test_shopping_cart_duplicates(self):
        # Try to add two same products
        # No same 'product_variation_id' for different 'shopping_cart_item' objects

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.jwt_access_token)

        self.product_qs = self.create_products()
        product_variation = ProductVariation.objects.all()[0].pk

        data = {
            "product_variation": product_variation,
            "quantity": 1
        }

        response = self.client.post(reverse(self.url_name), data, format='json')
        self.assertEqual(response.status_code, 201, 'Item must be created successfully')

        response = self.client.post(reverse(self.url_name), data, format='json')
        self.assertEqual(response.status_code, 201, 'Item must be created successfully 2')


        # response = self.client.post(reverse(url_name), data, format='json')
    #
    #     response = self.get_response('GET', url_name)
        # self.assertEqual(response.status_code, 200, 'Shopping cart must be displayed to authorized users')
    #
    #     response = self.get_response('POST', url_name, data=data)
    #     self.assertEqual(response.status_code, 201, 'Product must be successfully added')
    #
    #     response = self.get_response('POST', url_name, data=data)
    #     self.assertEqual(response.status_code, 201, 'Product must be successfully added')
    #
    #     response = self.get_response('GET', url_name)
    #     self.assertEqual(response.status_code, 200, 'Shopping cart items must be displayed to authorized users')
    #     self.assertEqual(len(response.data), 1, 'There must be only one product')
    #     self.assertEqual(response.data[0]['quantity'], 2, "'quantity' must be equal to 2")
    #     self.assertEqual(response.data[0]['item_price'], 58.00, "'price' must be equal to 58.00")
    #
    # def test_shopping_cart_create_quantity(self):
    #     # Try to create quantity of product in shopping cart to 1000
    #     # Quantity must be equal to in stock quantity (50 and 100)
    #
    #     url_name = 'shopping_cart_items-list'
    #     data1 = {
    #        "product_item_size_quantity": self.pisq_1.pk,
    #        "quantity": 1000
    #     }
    #     data2 = {
    #        "product_item_size_quantity": self.pisq_2.pk,
    #        "quantity": 1000
    #     }
    #
    #     response = self.get_response('POST', url_name, data=data1)
    #     self.assertEqual(response.status_code, 201, 'Product must be successfully added')
    #
    #     response = self.get_response('POST', url_name, data=data2)
    #     self.assertEqual(response.status_code, 201, 'Product must be successfully added')
    #
    #     response = self.get_response('GET', url_name)
    #     self.assertEqual(response.status_code, 200, 'Shopping cart items must be displayed to authorized users')
    #     self.assertEqual(response.data[0]['quantity'], 100, 'Quantity must be equal to 100')
    #     self.assertEqual(response.data[1]['quantity'], 50, 'Quantity must be equal to 50')
    #     self.assertEqual(len(response.data), 2, 'There must be two products.')
    #
    # def test_shopping_cart_update_quantity(self):
    #     # Try to update quantity of product in shopping cart to 1000
    #     # Quantity must be equal to in stock quantity (100)
    #
    #     url_name = 'shopping_cart_items-list'
    #     url_name_for_update = 'shopping_cart_items-detail'
    #     data = {
    #        "product_item_size_quantity": self.pisq_1.pk,
    #        "quantity": 1
    #     }
    #     data_for_update = {
    #        "product_item_size_quantity": self.pisq_2.pk,
    #        "quantity": 1000
    #     }
    #
    #     response = self.get_response('POST', url_name, data=data)
    #     self.assertEqual(response.status_code, 201, 'Product must be successfully added')
    #
    #     reverse_kwargs = {'pk': response.data['id']}
    #
    #     response = self.get_response('PUT', url_name_for_update, data=data_for_update, reverse_kwargs=reverse_kwargs)
    #     self.assertEqual(response.status_code, 200, 'Product must be successfully updated')
    #     self.assertEqual(response.data['quantity'], 100, 'Quantity must de equal to 100')
    #
    #     response = self.get_response('GET', url_name)
    #     self.assertEqual(response.status_code, 200, 'Product must be successfully added')
    #     self.assertEqual(response.data[0]['quantity'], 100, 'Quantity must de equal to 100')
    #
    # def test_add_out_of_stock_item(self):
    #     # Try to add a product which is out of stock
    #     # Request must be bad request 400
    #
    #     url_name = 'shopping_cart_items-list'
    #     self.pisq_1.quantity = 0 # out of stock
    #     self.pisq_1.save()
    #     data = {
    #        "product_item_size_quantity": self.pisq_1.pk,
    #        "quantity": 1
    #     }
    #
    #     response = self.get_response('POST', url_name, data=data)
    #     self.assertEqual(response.status_code, 400, "Product can't be added due to out of stock")
    #
    # def test_discount_price(self):
    #     # Apply discount 20% to product item
    #     # Try to get 'item_price' and 'discount_price'
    #     # 'discount_price' must be 'item_price' - 20%
    #
    #     self.create_discount()
    #     self.pi_1.discount = self.discount_1  # Apply discount to 'nike t-shirt' product item
    #     self.pi_1.save()
    #
    #     url_name = 'shopping_cart_items-list'
    #     data = {
    #        "product_item_size_quantity": self.pisq_1.pk,
    #        "quantity": 1
    #     }
    #
    #     response = self.get_response('POST', url_name, data=data)
    #     self.assertEqual(response.status_code, 201, 'Product must be successfully added')
    #     self.assertEqual(response.data['item_price'], Decimal('29.00'), "'item_price' must be Decimal('29.00')")
    #     self.assertEqual(response.data['discount_price'], Decimal('23.20'), "'discount_price' must be Decimal('23.20')")
