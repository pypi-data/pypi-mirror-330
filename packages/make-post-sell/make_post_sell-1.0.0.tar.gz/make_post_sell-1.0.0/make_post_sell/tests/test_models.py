import unittest

import mock

from ..models import User, Coupon, Shop, is_user_name_valid
from ..models.meta import now_timestamp

mock_always_none = mock.Mock(return_value=None)
mock_always_true = mock.Mock(return_value=True)
mock_false_then_true = mock.Mock(side_effect=[False, False, True])


class TestUser(unittest.TestCase):
    @mock.patch("make_post_sell.models.user.is_user_name_available", mock_always_true)
    def setUp(self):
        self.user = User("russell@ballestrini.net")

    def test_created_timestamp_set(self):
        self.assertGreater(self.user.created_timestamp, 100000)

    def test_email_set(self):
        self.assertEqual(self.user.email, "russell@ballestrini.net")

    def test_new_password(self):
        raw_password = self.user.new_password()
        self.assertEqual(len(raw_password), 6)

    def test_check_password_success(self):
        raw_password = self.user.new_password()
        self.assertTrue(self.user.check_password(raw_password))

    def test_check_password_failure(self):
        raw_password = self.user.new_password()
        self.assertFalse(self.user.check_password("fake password"))

    def test_is_user_name_valid(self):
        self.assertTrue(is_user_name_valid("validusername"))
        self.assertTrue(is_user_name_valid("validusername2"))
        self.assertTrue(is_user_name_valid("ValidUsername"))
        self.assertTrue(is_user_name_valid("valid-username"))
        self.assertTrue(is_user_name_valid("valid username"))

        self.assertFalse(is_user_name_valid("invalid!!!"))
        self.assertFalse(is_user_name_valid(""))

    @mock.patch("make_post_sell.models.user.is_user_name_available", mock_always_true)
    def test_generate_user_name_no_dash_prefix(self):
        u = User("tim@example.com")
        self.assertFalse(u.name.startswith("-"))


class TestCart(unittest.TestCase):

    # TODO: please test the fitness of the the Cart model.
    #
    #       We have deliberately not written these tests but we should
    #       before going to much further. Unit tests are much faster and
    #       more grainular than functional tests.
    #
    #       I'm moving forward without creating these tests because I have
    #       a functional test running as a safety net.
    #
    #       That said unit tests are much better at capturing expected
    #       behavior and have better tooling for test and codepath coverage.
    #
    #       Please help write unit tests soon!

    def setUp(self):
        pass

    def validate_attached_coupon_codes(self):
        """Make sure all coupons attached to the cart met the terms."""
        pass

class TestCoupon(unittest.TestCase):
    @mock.patch("make_post_sell.models.user.is_user_name_available", mock_always_true)
    def setUp(self):

        # if the year is 2040 and this code is still in use and these tests
        # break, it is safe to raise this date another +20 years.
        future_date = "2040-01-15"
        past_date = "2020-01-15"

        self.shop = Shop(
            "my-shop",
            "860-555-5555",
            "1 wayward way",
            "my shop description",
        )
        self.coupon = Coupon(
            shop=self.shop,
            code="a-coupon-code",
            description="a valid coupon",
            action_type="dollar-off",
            action_value=500,
            max_redemptions=100,
            max_redemptions_per_user=1,
            expiration_date=future_date,
            cart_qualifier = 20,
        )
        self.old_coupon = Coupon(
            shop=self.shop,
            code="old-coupon-code",
            description="a invalid coupon",
            action_type="dollar-off",
            action_value=500,
            max_redemptions=100,
            max_redemptions_per_user=1,
            expiration_date=past_date,
            cart_qualifier = 20,
        )
        self.disabled_coupon = Coupon(
            shop=self.shop,
            code="disabled-coupon-code",
            description="a disabled coupon",
            action_type="dollar-off",
            action_value=500,
            max_redemptions=100,
            max_redemptions_per_user=1,
            expiration_date=future_date,
            cart_qualifier = 20,
        )
        self.disabled_coupon.disabled = True

    def test_coupon_code(self):
        self.assertNotEqual(self.coupon.code, "invalid-code")
        self.assertEqual(self.coupon.code, "a-coupon-code")

        # make sure coupon is not expired.
        self.assertTrue(self.coupon.is_valid)
        self.assertTrue(self.coupon.is_not_expired)

        # test inverse.
        self.assertFalse(self.coupon.is_expired)
        self.assertFalse(self.coupon.is_not_valid)


    def test_expired_coupon_code(self):
        self.assertEqual(self.old_coupon.code, "old-coupon-code")

        # make sure old_coupon is_expired and is_not_valid
        self.assertTrue(self.old_coupon.is_expired)
        self.assertTrue(self.old_coupon.is_not_valid)

        # test inverse.
        self.assertFalse(self.old_coupon.is_valid)
        self.assertFalse(self.old_coupon.is_not_expired)


    def test_disabled_coupon_code(self):
        self.assertEqual(self.disabled_coupon.code, "disabled-coupon-code")

        # make sure disabled_coupon is_not_expired and is_not_valid
        self.assertTrue(self.disabled_coupon.is_not_expired)
        self.assertTrue(self.disabled_coupon.is_not_valid)

        # test inverse.
        self.assertFalse(self.disabled_coupon.is_valid)
        self.assertFalse(self.disabled_coupon.is_expired)
