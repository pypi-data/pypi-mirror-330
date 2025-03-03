# needed to grab test stripe keys from environment vars.
# MPS_TEST_STRIPE_PUBLIC_API_KEY & MPS_TEST_STRIPE_SECRET_API_KEY
from os import environ

import transaction
import unittest
import webtest
import stripe

from ..models import get_tm_session

from ..models.meta import Base

from ..models.shop import Shop, get_shop_by_name

from ..models.user import get_or_create_user_by_email

from ..models.cart import get_cart_by_id, get_all_carts

from ..models.stripe_user_shop import get_all_stripe_customer_objects

from ..models.product import get_product_by_id, get_all_products

from ..models.coupon import get_coupons_by_code

from ..lib.currency import dollars_to_cents, cents_to_dollars

from pyramid.paster import get_appsettings

import mock
from mock import patch


# todo we should pick a new file to put test helpers.
mock_always_true = mock.Mock(return_value=True)


# todo we should pick a new file to put test helpers.
class FunctionalTests(unittest.TestCase, object):
    def setUp(self):
        from make_post_sell import main

        self.settings = get_appsettings("test.ini")

        self.app = main({}, **self.settings)

        self.testapp = webtest.TestApp(self.app)

        self.session_factory = self.app.registry["dbsession_factory"]
        self.engine = self.session_factory.kw["bind"]
        Base.metadata.create_all(bind=self.engine)

        self.dbsession = get_tm_session(self.session_factory, transaction.manager)

    def tearDown(self):
        # log out current user.
        self.testapp.get("/log-out")
        # drop all tables in database.
        transaction.abort()
        Base.metadata.drop_all(bind=self.engine)


class UnauthenticatedFunctionalTests(FunctionalTests):
    def test_root_home_page(self):
        res = self.testapp.get("/", status=200)
        self.assertIn(b"log in", res.body)
        self.assertIn(b"Cart $0.00 (0)", res.body)

    def test_new_product_redirects(self):
        redirect_res = self.testapp.get("/p/new", status=302)
        res = redirect_res.follow()
        self.assertIn(b"You must log in to access that area.", res.body)

    def test_new_shop_redirects(self):
        redirect_res = self.testapp.get("/s/new", status=302)
        res = redirect_res.follow()
        self.assertIn(
            b"To create a new shop, please verify your email address below.", res.body
        )

    def test_user_settings_redirects(self):
        redirect_res = self.testapp.get("/u/settings", status=302)
        res = redirect_res.follow()
        self.assertIn(
            b"To view your settings, please verify your email address below.", res.body
        )

    @patch("smtplib.SMTP")
    def test_user_log_in(self, mock_smtp):
        redirect_res1 = self.testapp.post(
            "/join-or-log-in", {"email": "test@example.com"}
        )
        self.assertIn(
            b"Check email for a 6 digit verification code to log in. test@example.com",
            redirect_res1.follow().body,
        )


class AuthenticatedFunctionalTests(FunctionalTests):
    def setUp(self):
        super(AuthenticatedFunctionalTests, self).setUp()

        self.shop1_params = {
            "name": "russell's shop",
            "phone_number": "555-555-8688",
            "billing_address": "555 example way\nnorth pole\n555555\n",
            "description": "russell's shop sells some great digital downloads.",
            "stripe_public_api_key": environ["MPS_TEST_STRIPE_PUBLIC_API_KEY"],
            "stripe_secret_api_key": environ["MPS_TEST_STRIPE_SECRET_API_KEY"],
            "domain_name": "localhost.localhost",
        }

        self.shop2_params = {
            "name": "joe's shop",
            "phone_number": "555-555-9998",
            "billing_address": "55 example st\nnorth pole\n555555\n",
            "description": "joe's shop sells some bad digital downloads.",
            "stripe_public_api_key": environ["MPS_TEST_STRIPE_PUBLIC_API_KEY"],
            "stripe_secret_api_key": environ["MPS_TEST_STRIPE_SECRET_API_KEY"],
            "domain_name": "localhost.localhost",
        }

        self.product1_params = {
            "title": "russell's product",
            "description": "russell's product",
            "price": "3.50",
            "is_sellable": "on",
            "submit": True,
        }

        self.coupon1_params = {
            "code": "camp31",
            "description": "Slippery Halloween Party",
            "action_type": "dollar-off",
            "action_value": "3.50",
            "max_redemptions": "100",
            "cart_qualifier": "10",
            "max_redemptions_per_user": "1",
            "expiration_date": "2030-10-31",
        }

        # create test user1 and user2.
        self.user1 = get_or_create_user_by_email(self.dbsession, "test1@example.com")
        self.user2 = get_or_create_user_by_email(self.dbsession, "test2@example.com")

        # capture user credentials needed for authentication.
        self.user1_creds = (
            "test1@example.com",
            # returns the raw auto-generated password used
            # in one-time-password links OTP
            self.user1.new_password(),
        )
        self.user2_creds = (
            "test2@example.com",
            # returns the raw auto-generated password used
            # in one-time-password links OTP
            self.user2.new_password(),
        )

        # flush new users to database.
        self.dbsession.add(self.user1)
        self.dbsession.add(self.user2)
        self.dbsession.flush()

        # commit the transaction.
        transaction.manager.commit()

        # requery User objects to avoid detached instance error.
        self.user1 = get_or_create_user_by_email(self.dbsession, "test1@example.com")
        self.user2 = get_or_create_user_by_email(self.dbsession, "test2@example.com")

    def _clean_up_user(self, user):
        # print("deleteing user {} from dbsession.".format(user.name))
        self.dbsession.delete(user)

    def _clean_up_shop(self, shop):
        self.dbsession.delete(shop)

    def _clean_up_stripe(self):
        """clean up remote Stripe API by removing Customer objects."""
        customers = get_all_stripe_customer_objects(self.dbsession)
        # print("cleaning remote Stripe API by removing {} Customer objets.".format(len(customers)))
        for customer in customers:
            customer.delete()

    def tearDown(self):
        """Delete test users and shop in between tests."""

        # clean up remote Stripe API by removing Customer objects.
        self._clean_up_stripe()

        # log out and delete the test_users in between tests.
        self._clean_up_user(self.user1)
        self._clean_up_user(self.user2)

        # self.dbsession.flush()
        # transaction.manager.commit()
        super(AuthenticatedFunctionalTests, self).tearDown()

    def log_in_user(self, user_creds):
        # Set the email in the session before posting to the verification challenge
        self.testapp.post("/join-or-log-in", {"email": user_creds[0]})

        # Simulate entering the OTP
        res_login = self.testapp.post(
            "/verification-challenge", {"raw-otp": user_creds[1], "submit": True}
        )

        # Attach csrf to class if needed
        res_csrf = self.testapp.get("/")
        # self.csrf = res_csrf.form.fields["csrf_token"][0].value
        return res_login

    def test_prevent_verification_code_brute_force(self):
        """do not accept valid verification challenge code after failures."""

        # store invlaid pass code.
        valid_creds = self.user1_creds
        invalid_creds = (self.user1_creds[0], "invalid")

        for i in range(0, 12):
            self.log_in_user(invalid_creds)

        self.log_in_user(valid_creds)

        self.dbsession.refresh(self.user1)

        self.assertEqual(self.user1.password_attempts, 13)
        self.assertEqual(self.user1.authenticated, False)

    def test_a_girl_has_no_name(self):
        """A new user configures a display name."""
        self.log_in_user(self.user1_creds)

        res = self.testapp.post(
            "/u/settings", {"name": "russell", "full_name": "russell ballestrini"}
        )

        res_body = res.body.decode()

        self.assertIn("russell", res_body)
        self.assertIn("russell ballestrini", res_body)
        self.assertIn("You set your public display name.", res_body)
        self.assertIn("You set your private full name.", res_body)

        self.testapp.get("/log-out")

        self.log_in_user(self.user1_creds)
        res = self.testapp.get("/u/settings")
        res_body = res.body.decode()

        self.dbsession.refresh(self.user1)
        self.dbsession.refresh(self.user2)

        self.assertIn(self.user1.name, res_body)
        self.assertNotIn(self.user2.name, res_body)

    def test_new_product_without_a_shop(self):
        self.log_in_user(self.user2_creds)
        redirect_res = self.testapp.get("/p/new", status=302)
        res = redirect_res.follow()
        self.assertIn(b"You must have a shop editor role to access that.", res.body)

    def test_create_new_shop(
        self, user_creds=None, shop_params=None, log_out_user=False
    ):
        if user_creds is None:
            user_creds = self.user1_creds

        if shop_params is None:
            shop_params = self.shop1_params

        # log in with given user credentials.
        self.log_in_user(user_creds)

        # create a new shop.
        redirect_res = self.testapp.post("/s/new", shop_params)
        res = redirect_res.follow()
        self.assertIn(
            "Great work, you created a shop! You may continue to setup your shop or start posting products!",
            res.body.decode(),
        )

        # query the new shop from database.
        shop = get_shop_by_name(self.dbsession, shop_params["name"])

        # prove that shop is not ready.
        self.assertFalse(shop.is_ready)
        self.assertTrue(shop.is_not_ready)

        # add stripe keys to the newly created shop to make it ready.
        res = self.testapp.post(f"/s/{shop.id}/settings", shop_params)
        res_body = res.body.decode()
        self.assertIn(
            "You set the shop's stripe_public_api_key.",
            res_body,
        )
        self.assertIn(
            "You set the shop's stripe_secret_api_key.",
            res_body,
        )

        # refresh shop attributes from database.
        self.dbsession.refresh(shop)

        # prove that shop is ready.
        self.assertTrue(shop.is_ready)
        self.assertFalse(shop.is_not_ready)

        if log_out_user:
            self.testapp.get("/log-out")

        return shop

    def test_new_shop_invalid_shop_name(self):
        self.log_in_user(self.user1_creds)
        params = self.shop1_params
        params["name"] = "$$$ russell's shop"
        res = self.testapp.post("/s/new", params)
        self.assertIn(
            "Invalid shop name, only use alpha numeric, spaces, dashes, or periods.",
            res.body.decode(),
        )

    def test_new_shop_missing_required_field(self):
        self.log_in_user(self.user2_creds)
        params = self.shop2_params
        del params["phone_number"]
        res = self.testapp.post("/s/new", params)
        self.assertIn("You must fill out all fields.", res.body.decode())

    def test_new_shop_name_already_in_use(self):
        self.log_in_user(self.user1_creds)
        params = self.shop1_params
        self.testapp.post("/s/new", params)
        res = self.testapp.post("/s/new", params)
        self.assertIn(
            "That shop name is already in use. Please pick another.", res.body.decode()
        )

    def test_new_product_missing_required_fields(self):
        # log in and create a new shop.
        shop = self.test_create_new_shop(
            user_creds=self.user1_creds,
            shop_params=self.shop1_params,
            log_out_user=False,
        )

        product_params = self.product1_params
        del product_params["description"]
        # redirect_res1 = self.testapp.post("/p/new", product_params)
        # res = redirect_res1.follow()
        res = self.testapp.post(f"/p/new?shop_id={shop.id}", product_params)
        self.assertIn("You must fill out all fields.", res.body.decode())

    def test_new_product(
        self, user_creds=None, shop_params=None, product_params=None, log_out_user=False
    ):
        if user_creds is None:
            user_creds = self.user1_creds

        if shop_params is None:
            shop_params = self.shop1_params

        if product_params is None:
            product_params = self.product1_params

        # log in and create a new shop.
        shop = self.test_create_new_shop(
            user_creds=user_creds,
            shop_params=shop_params,
        )

        redirect_res = self.testapp.post(f"/p/new?shop_id={shop.id}", product_params)
        res = redirect_res.follow()
        self.assertIn("Great, next you may upload files.", res.body.decode())

        if log_out_user:
            self.testapp.get("/log-out")

    def test_new_product_when_user_does_not_have_editor_role_on_shop(self):
        # log in user1.
        self.log_in_user(self.user1_creds)

        # have user1 create a new shop.
        params = self.shop1_params
        res = self.testapp.post("/s/new", params)

        # get the new shop_id from the response location attribute.
        shop_id = res.location.split("/")[-2]

        # log out user1.
        self.testapp.get("/log-out")

        # log in user2.
        self.log_in_user(self.user2_creds)

        # make user2 create a new product on a shop she doesn't own.
        params = self.product1_params
        redirect_res = self.testapp.post(f"/p/new?shop_id={shop_id}", params)
        res = redirect_res.follow()
        self.assertIn(
            "You must have a shop editor role to access that.", res.body.decode()
        )

    def test_new_product_price_history(self):
        self.test_new_product(
            user_creds=self.user1_creds,
            shop_params=self.shop1_params,
            product_params=self.product1_params,
        )

        # get the Product object from database.
        all_products = get_all_products(self.dbsession)
        product = all_products.one()

        self.assertEqual(product.price, 3.50)
        self.assertEqual(product.price, product.price_history[0].price)
        self.assertEqual(product.price_history.count(), 1)
        self.assertEqual(product.price_in_cents, 350)

    # this patch requires an argument added to test method `mock_smtp`.
    @patch("smtplib.SMTP")
    @patch("make_post_sell.models.Product.is_ready", mock_always_true)
    def test_cart_checkout_for_shop(self, mock_smtp):
        # 1. log in as user1.
        # 2. create new shop.
        # 3. make new shop ready for checkout.
        # 4. create new product.
        # 5. log out user1.
        self.test_new_product(
            user_creds=self.user1_creds,
            shop_params=self.shop1_params,
            product_params=self.product1_params,
            log_out_user=True,
        )

        # get the Product object from database.
        all_products = get_all_products(self.dbsession)
        product = all_products.one()

        shop = get_shop_by_name(self.dbsession, self.shop1_params["name"])

        # print("{},{},{}".format(product.id, product.title, product.price))

        # log in user2.
        self.log_in_user(self.user2_creds)

        # add product to cart.
        redirect_res1 = self.testapp.get(
            f"/cart/add?product_id={product.id}&shop_id={shop.id}"
        )
        redirect_res2 = redirect_res1.follow()
        res = redirect_res2.follow()
        res_body = res.body.decode()

        self.assertIn('You added "russell\'s product" to your cart.', res_body)

        carts = get_all_carts(self.dbsession)

        # make sure we have 4 carts. request.active_cart & request.session_cart for each user.
        self.assertEqual(4, carts.count())

        self.dbsession.refresh(shop)
        self.dbsession.refresh(self.user1)
        self.dbsession.refresh(self.user2)

        user_1_cart = shop.get_active_cart_for_user(self.user1)
        user_2_cart = shop.get_active_cart_for_user(self.user2)

        # make sure user1 has 0 items in active Cart.
        self.assertEqual(0, user_1_cart.count)

        # make sure user2 has 1 item in active Cart.
        self.assertEqual(1, user_2_cart.count)

        redirect_res = self.testapp.get(
            f"/u/cart/{user_2_cart.id}/checkout?shop_id={shop.id}"
        )
        redirect_res2 = redirect_res1.follow()
        res = redirect_res2.follow()
        self.assertIn("Please enter your payment information.", res.body.decode())

        # the stripe migration to SetupIntents broke this end-to-end test routine.
        """
        res = self.testapp.post(
            "/billing/add-card?shop_id={}".format(shop.id),
            {
                "email": self.user2.email,
                "stripeToken": "tok_visa",
            },
        )

        res = self.testapp.get(
            "/u/cart/{}/checkout?shop_id={}".format(
                user_2_cart.id,
                shop.id
            )
        )
        res_body = res.body.decode()
     
        self.assertIn("Please confirm your order.", res_body)
        self.assertIn("Visa", res_body)
        self.assertIn("Are you sure you want to charge", res_body)

        redirect_res1 = self.testapp.get(
            "/u/cart/{}/complete/checkout?shop_id={}".format(
                user_2_cart.id,
                shop.id
            )
        )
        redirect_res2 = redirect_res1.follow()
        res = redirect_res2.follow()
        res_body = res.body.decode()
        self.assertIn("Success, you have completed the purchase!", res_body)

        # refresh shop attributes from database.
        self.dbsession.refresh(shop)

        stripe_customer = shop.stripe_customer(self.user2)

        stripe_charge = shop.list_stripe_charges(stripe_customer).data[0]

        self.assertEqual(
            stripe_charge.amount,
            dollars_to_cents(self.product1_params["price"]),
        )
        """

    @patch("make_post_sell.models.Product.is_ready", mock_always_true)
    def make_new_coupon_for_shop(self, coupon_params=None):
        # 1. log in as user1.
        # 2. create new shop.
        # 3. make new shop ready for checkout.
        # 4. create new product.
        self.test_new_product(
            user_creds=self.user1_creds,
            shop_params=self.shop1_params,
            product_params=self.product1_params,
        )

        # query the new shop from database.
        shop = get_shop_by_name(self.dbsession, self.shop1_params["name"])

        if coupon_params is None:
            coupon_params = self.coupon1_params
        else:
            # merge in any given params.
            tmp = self.coupon1_params.copy()
            tmp.update(coupon_params)
            coupon_params = tmp

        # create a new shop coupon.
        res = self.testapp.post(
            f"/s/{shop.id}/coupon/new",
            coupon_params,
        )
        return res

    def test_new_coupon_for_shop(self):
        res = self.make_new_coupon_for_shop()
        res = res.follow()
        self.assertIn("You created a new coupon!", res.body.decode())

    def test_new_coupon_missing_params(self):
        coupon_params = self.coupon1_params
        del coupon_params["code"]
        res = self.make_new_coupon_for_shop(coupon_params)
        self.assertIn("Please submit all required fields.", res.body.decode())

    # this patch requires an argument added to test method `mock_smtp`.
    @patch("smtplib.SMTP")
    @patch("make_post_sell.models.Product.is_ready", mock_always_true)
    def test_checkout_with_coupon_code(self, mock_smtp):
        res = self.make_new_coupon_for_shop()
        res = res.follow()
        self.assertIn("You created a new coupon!", res.body.decode())

        # log out user1.
        self.testapp.get("/log-out")

        # log in user2.
        self.log_in_user(self.user2_creds)

        # query the new shop from database.
        shop = get_shop_by_name(self.dbsession, self.shop1_params["name"])

        coupons = get_coupons_by_code(self.dbsession, self.coupon1_params["code"])
        coupon = coupons[0]

        # apply coupon to user2's active cart.
        self.testapp.post(f"/coupon/apply?&coupon_id={coupon.id}&shop_id={shop.id}")

        # verify coupon was applied.
        res_redirect1 = self.testapp.get(f"/cart?shop_id={shop.id}")
        res = res_redirect1.follow()
        res_body = res.body.decode()
        self.assertIn("Slippery Halloween Party", res_body)
        self.assertIn("3.50", res_body)
        self.assertIn("camp31", res_body)

        # get the Product object from database.
        all_products = get_all_products(self.dbsession)
        product = all_products.one()

        # add product to user2's active cart.
        self.testapp.get(f"/cart/add?product_id={product.uuid_str}&shop_id={shop.id}")

        # the stripe migration to SetupIntents broke this end-to-end test routine.
        """
        # add billing details for user2 for this shop.
        res = self.testapp.post(
            "/billing/add-card?shop_id={}".format(shop.id),
            {
                "email": self.user2.email,
                "stripeToken": "tok_visa",
            },
        )

        # why is this None?
        user_2_cart = shop.get_active_cart_for_user(self.user2)

        # attempt to checkout before coupon is properly qualified.
        # shop total must be over cart_qualifier (test defaults to $10).
        res_redirect1 = self.testapp.get(
            "/u/cart/{}/checkout?shop_id={}".format(
                user_2_cart.id,
                shop.id
            )
        )
        res = res_redirect1.follow()
        self.assertIn("Please review coupon terms: shop total not met.", res.body.decode())

        # add more product to user2's active cart, to pass cart_qualifier.
        self.testapp.get("/cart/add?product_id={}&shop_id={}".format(product.uuid_str, shop.id))
        self.testapp.get("/cart/add?product_id={}&shop_id={}".format(product.uuid_str, shop.id))

        # checkout coupon confirmation unblocked. 
        res = self.testapp.get(
            "/u/cart/{}/checkout?shop_id={}".format(
                user_2_cart.id,
                shop.id
            )
        )
        self.assertIn("Please confirm your order.", res.body.decode())
        """
