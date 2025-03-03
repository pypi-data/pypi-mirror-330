from .models.cart import Cart
from .models.cart import get_cart_by_id
from .models.user import get_user_by_id
from .models.shop import get_shop_by_id
from .models.shop import get_shop_by_domain_name
from .models.shop_location import get_shop_location_by_id
from .models.product import get_product_by_id

from . import get_children_settings


def includeme(config):
    """Enhance all inbound requests with extra attributes!"""

    # Each inbound request will run these functions as-needed
    # and attach the results as attributes.

    # get the app_settings from the config file.
    app_settings = get_children_settings(config.get_settings(), "app")

    def add_debug_mode(request):
        """Return True if debug toolbar is enabled."""
        return "pyramid_debugtoolbar" in request.registry.settings.get(
            "pyramid.includes", ""
        )

    def add_user(request):
        """Return User object or None. User.authenticated may be True or False."""
        user = None
        authenticated_user_id = request.session.get("authenticated_user_id", None)

        if authenticated_user_id:
            # attach the user object from DB to the request.
            user = get_user_by_id(request.dbsession, authenticated_user_id)
            if user is not None:
                user.authenticated = True

        return user

    def add_product(request):
        """Return Product object or None from route."""
        product_id = request.matchdict.get("product_id")
        if product_id:
            return get_product_by_id(request.dbsession, product_id)

    def add_shop(request):
        """return Shop object or None."""
        # get shop_id first from query, then route, or None.

        shop_id = request.params.get("shop_id", request.matchdict.get("shop_id"))

        if shop_id:
            return get_shop_by_id(request.dbsession, shop_id)
        elif request.product:
            return request.product.shop
        else:
            if request.is_saas_domain:
                if request.user and request.user.active_shop:
                    return request.user.active_shop
            else:
                return get_shop_by_domain_name(request.dbsession, request.domain)

    def add_active_cart(request):
        """
        Load active cart for user for shop or
        create cart and add it to the user as active.

        Either way, always return a Cart.
        """
        if request.user and request.shop:
            cart = request.shop.get_active_cart_for_user(request.user)
            if cart is None:
                cart = request.shop.create_new_cart_for_user(request.user)
            return cart
        else:
            return request.session_cart

    def add_session_cart(request):
        """Return Cart from session or None."""
        cart_id = request.session.get("active_cart_id", None)
        if cart_id is not None:
            cart = get_cart_by_id(request.dbsession, cart_id)
        else:
            # if no active cart in session, create one.
            cart = Cart()
            cart.shop = request.shop
            cart.active = True
            request.session["active_cart_id"] = str(cart.id)
            request.dbsession.add(cart)
            request.dbsession.flush()
        return cart

    def add_shop_location(request):
        """
        Return the ShopLocation from session if available.
        If not, and the shop has one or more locations, set the first location as the default.
        Returns None if no locations are available.
        """
        shop_location_id = request.session.get("shop_location_id")
        if shop_location_id is not None:
            return get_shop_location_by_id(request.dbsession, shop_location_id)
        if request.shop:
            first_location = request.shop.shop_locations.first()
            if first_location:
                request.session["shop_location_id"] = str(first_location.id)
                return first_location
        return None

    def add_market(request):
        """Return Market object or None."""
        return None

    def add_spam(request):
        """Test if request looks spammy. Returns HTTP Error or False."""
        from pyramid.httpexceptions import HTTPUnauthorized

        if request.params.get("email2", "") != "":
            print(
                f"Blocked spam request from {request.remote_addr}: Hidden field populated."
            )
            return HTTPUnauthorized("You smell like a spammer.")
        return False

    def add_app(request):
        """Attach app settings dictionary."""
        return app_settings

    def add_secure_uploads_client(request):
        """returns an S3 compatible client."""
        import boto3

        # Initialize a session using DigitalOcean Spaces.
        session = boto3.session.Session()
        return session.client(
            "s3",
            region_name=request.app["bucket.secure_uploads.region"],
            endpoint_url=request.app["bucket.secure_uploads.post_endpoint"],
            aws_access_key_id=request.app["bucket.secure_uploads.access_key"],
            aws_secret_access_key=request.app["bucket.secure_uploads.secret_key"],
        )

    def add_is_shop_domain(request):
        """
        Returns True or False.
        Returns True when request domain matches the shop domain.
        """
        if request.shop is not None and request.domain == request.shop.domain_name:
            return True
        return False

    def add_saas_domain(request):
        return request.app.get("root_domain")

    def add_saas_url(request):
        return request.app.get("root_url")

    def add_is_saas_domain(request):
        """
        Returns True or False.
        Only one domain should have this method return True per deployment.

        This request method lets us:
          * show two different "home" pages
          * show only certain buttons on the SaaS domain.
        """
        root_domain = request.app.get("root_domain")
        if root_domain:
            return request.domain.endswith(root_domain)
        return False

    # Register functions to app config as request methods.
    # To prevent multiple DB lookups, cache result with `reify=True`.
    config.add_request_method(add_debug_mode, "debug_mode", reify=True)
    config.add_request_method(add_user, "user", reify=True)
    config.add_request_method(add_active_cart, "active_cart", reify=True)
    config.add_request_method(add_session_cart, "session_cart", reify=True)

    config.add_request_method(add_product, "product", reify=True)

    config.add_request_method(add_shop, "shop", reify=True)

    config.add_request_method(add_shop_location, "shop_location", reify=True)

    config.add_request_method(add_market, "market", reify=True)

    config.add_request_method(add_spam, "spam", reify=True)

    config.add_request_method(add_app, "app", reify=True)

    config.add_request_method(add_is_shop_domain, "is_shop_domain", reify=True)
    config.add_request_method(add_is_saas_domain, "is_saas_domain", reify=True)
    config.add_request_method(add_saas_domain, "saas_domain", reify=True)

    config.add_request_method(add_saas_url, "saas_url", reify=True)

    config.add_request_method(
        add_secure_uploads_client, "secure_uploads_client", reify=True
    )
