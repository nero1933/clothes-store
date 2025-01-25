import uuid

from rest_framework.reverse import reverse

from ecommerce.models import UserProfile, Payment
from ecommerce.utils.tests.mixins import TestAPIOrder


class TestReviews(TestAPIOrder):

    def setUp(self):
        super().setUp()

    def test_reviews(self):

        data = {
            'comment': 'good',
            'rating': 5,
        }

        # 'review_id' & 'review_url' must be None until order isn't paid
        response = self.create_guest_order()
        self.assertEqual(response.status_code, 201, 'Order must be created successfully')
        order_id = response.data.get('id', None)

        response = self.client.get(reverse(self.url_order_detail, kwargs={'pk': order_id}))
        self.assertEqual(response.status_code, 200, 'Guest must see his order details')
        order_items = response.data.get('order_item', {})

        oi_1 = order_items[0]
        oi_2 = order_items[1]

        review_id_1 = oi_1.get('review_id', None)
        review_url_1 = oi_1.get('review_url', None)

        review_id_2 = oi_2.get('review_id', None)
        review_url_2 = oi_2.get('review_url', None)

        self.assertTrue(all(True if x is None else False for x in
                            [review_id_1, review_url_1, review_id_2, review_url_2]),
                        'There have to be no reviews')

        # User can't create a review until order isn't paid

        payment_obj = Payment.objects.get(order_id=order_id)
        payment_obj.payment_bool = True
        payment_obj.save()

        response = self.client.get(reverse(self.url_order_detail, kwargs={'pk': order_id}))
        self.assertEqual(response.status_code, 200, 'Guest must see his order details')
        order_items = response.data.get('order_item', {})

        oi_1 = order_items[0]
        review_url_1 = oi_1.get('review_url', None)

        payment_obj.payment_bool = False
        payment_obj.save()

        response = self.client.post(review_url_1, data=data)
        self.assertEqual(response.status_code, 403,
                         'Must be 403 PermissionDenied. User can not create review until order is not paid')

        payment_obj.payment_bool = True
        payment_obj.save()

        # After order was paid user must see 'review_url'

        response = self.client.get(reverse(self.url_order_detail, kwargs={'pk': order_id}))
        self.assertEqual(response.status_code, 200, 'Guest must see his order details')
        order_items = response.data.get('order_item', {})

        oi_1 = order_items[0]
        oi_2 = order_items[1]

        review_id_1 = oi_1.get('review_id', None)
        review_url_1 = oi_1.get('review_url', None)

        review_id_2 = oi_2.get('review_id', None)
        review_url_2 = oi_2.get('review_url', None)

        self.assertTrue(all(True if x is None else False for x in [review_id_1, review_id_2]),
                        "There have to be no reviews id's")
        self.assertTrue(all(self.is_valid_url(x) for x in [review_url_1, review_url_2]),
                        'There have to be url for each order item')

        # After order was paid user can create a review

        response = self.client.post(review_url_1, data=data)
        self.assertEqual(response.status_code, 201,
                         'Review must be created successfully')
        review_id = response.data.get('id', None)

        # Try to create two reviews
        response = self.client.post(review_url_1, data=data)
        self.assertEqual(response.status_code, 400,
                         'User can not review twice same product (same order item)')

        # After review was left 'review_id' must change to int
        response = self.client.get(reverse(self.url_order_detail, kwargs={'pk': order_id}))
        self.assertEqual(response.status_code, 200, 'Guest must see his order details')
        order_items = response.data.get('order_item', {})

        oi_1 = order_items[0]
        oi_2 = order_items[1]

        review_id_1 = oi_1.get('review_id', None)
        review_id_2 = oi_2.get('review_id', None)

        self.assertTrue(review_id == review_id_1,
                        f'Review of first order item must be {review_id}')
        self.assertTrue(review_id_2 is None,
                        'Review of second order item must be None')

        # review access (get else user review, create else user review)

        # After review was created user can update it

        new_data = {
            'comment': 'bad',
            'rating': 1,
        }

        review_url_1_detail = review_url_1 + f'{review_id}/'

        response = self.client.patch(review_url_1_detail, data=new_data)
        self.assertEqual(response.status_code, 200, 'Status code after update must me 200 OK')
        self.assertTrue(response.data['comment'] == new_data['comment']
                        and response.data['rating'] == new_data['rating'],
                        'Review must be updated successfully')


        response = self.client.delete(review_url_1_detail)
        self.assertEqual(response.status_code, 204, 'Review must be deleted successfully')

        response = self.client.get(reverse(self.url_order_detail, kwargs={'pk': order_id}))
        self.assertEqual(response.status_code, 200, 'Guest must see his order details')
        order_items = response.data.get('order_item', {})

        oi_1 = order_items[0]
        review_id_1 = oi_1.get('review_id', None)
        review_url_1 = oi_1.get('review_url', None)

        self.assertTrue(review_id_1 is None and self.is_valid_url(review_url_1),
                        'Review id must be None and there have yo be a url')

        response = self.client.post(review_url_1, data=data)
        self.assertEqual(response.status_code, 201, 'Review must be created successfully')

        response = self.client.get(reverse(self.url_order_detail, kwargs={'pk': order_id}))
        self.assertEqual(response.status_code, 200, 'Guest must see his order details')
        order_items = response.data.get('order_item', {})

        oi_1 = order_items[0]
        oi_2 = order_items[1]

        review_id_1 = oi_1.get('review_id', None)
        review_url_1 = oi_1.get('review_url', None)
        review_url_2 = oi_2.get('review_url', None)
        review_url_detail_1 = review_url_1 + f'{review_id_1}/'

        #
        # Test review crud access
        #

        # create user

        self.client.credentials()

        test_email = uuid.uuid4().hex + '@domain.com'
        test_password = '123456789'
        test_user = UserProfile.objects.create_user(test_email, 'John', 'Doe', test_password)
        test_user.is_active = True
        test_user.save()
        self.assertEqual(test_user.is_guest, False, 'user.is_guest must be False')

        test_data = {'email': test_email, 'password': test_password}

        r = self.client.post(reverse(self.url_token), test_data)
        self.assertEqual(r.status_code, 200, 'User must be able to log in')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + r.data.get('access'))

        # After other user was created try to get access to reviews

        response = self.client.post(review_url_2, data=data)
        self.assertEqual(response.status_code, 404, 'User cant create review for other user')

        response = self.client.get(review_url_detail_1)
        self.assertEqual(response.status_code, 404, 'User cant get review for other user')

        response = self.client.patch(review_url_detail_1, data=data)
        self.assertEqual(response.status_code, 404, 'User cant patch review for other user')

        response = self.client.delete(review_url_detail_1)
        self.assertEqual(response.status_code, 404, 'User cant delete review for other user')
