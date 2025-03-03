from pyramid.view import view_config

from pyramid.httpexceptions import HTTPFound, HTTPBadRequest

from . import (
    user_required,
    shop_is_ready_required,
)


@view_config(route_name="billing", renderer="billing.j2")
@user_required(
    flash_msg="Verify your email to access Payment Preferences.",
    flash_level="info",
    redirect_to_route_name="join-or-log-in",
)
@shop_is_ready_required()
def billing(request):
    stripe_user_shop = request.shop.stripe_user_shop(request.user)

    if stripe_user_shop is None:
        # create a record for this user for holding stripe billing data.
        request.shop.stripe_customer(request.user, create=True)
        stripe_user_shop = request.shop.stripe_user_shop(request.user)

    cards = saved_cards = stripe_user_shop.stripe_cards
    active_card = stripe_user_shop.active_card

    if active_card is not None:
        for i, card in enumerate(saved_cards):
            if card.id == active_card.id:
                del cards[i]

    setup_intent = request.shop.stripe.SetupIntent.create(
        payment_method_types=["card"], customer=stripe_user_shop.cus_id
    )
    return {
        "client_secret": setup_intent.client_secret,
        "cards": cards,
        "active_card": active_card,
    }


@view_config(route_name="add-card")
@user_required()
@shop_is_ready_required()
def add_card(request):
    stripe_setup_intent = request.params.get("setup_intent")
    stripe_setup_intent_client_secret = request.params.get("setup_intent_client_secret")

    stripe_user_shop = request.shop.stripe_user_shop(request.user)

    if stripe_setup_intent:
        setup_intent = request.shop.stripe.SetupIntent.retrieve(
            stripe_setup_intent,
        )

        card_ids = stripe_user_shop.stripe_card_ids

        if len(card_ids) == 1:
            stripe_user_shop.active_card_id = card_ids[0]
            request.dbsession.add(stripe_user_shop)
            request.dbsession.flush()

        request.session.flash(("You saved a new card. {}", "success"))

    return HTTPFound("/billing")


@view_config(route_name="confirm-update-card", renderer="update-card.j2")
@user_required()
@shop_is_ready_required()
def confirm_update_card(request):
    card_id = request.matchdict.get("card_id")
    stripe_user_shop = request.shop.stripe_user_shop(request.user)
    card = stripe_user_shop.get_card_by_id(card_id)
    action = request.matchdict.get("action")
    action_human = action.replace("-", " ")
    return {
        "card": card,
        "card_id": card_id,
        "action": action,
        "action_human": action_human,
        "the_title": action_human.title(),
    }


@view_config(route_name="update-card")
@user_required()
@shop_is_ready_required()
def update_card(request):
    action = request.params.get("action", None)
    card_id = request.params.get("card_id")
    stripe_user_shop = request.shop.stripe_user_shop(request.user)
    card = stripe_user_shop.get_card_by_id(card_id)

    if card_id == stripe_user_shop.active_card_id:
        request.session.flash(("Cannot update an active card.", "error"))
        return HTTPFound("/billing")

    if card_id not in stripe_user_shop.stripe_card_ids:
        request.session.flash(("Cannot update a card you do not own.", "error"))
        return HTTPFound("/billing")

    if action not in ["make-card-active", "delete-card"]:
        return HTTPBadRequest
    if "delete-card" == action:
        request.shop.stripe.PaymentMethod.detach(card_id)
        request.session.flash(("You deleted that card.", "success"))
    if "make-card-active" == action:
        stripe_user_shop.active_card_id = card_id
        request.dbsession.add(stripe_user_shop)
        request.dbsession.flush()
        request.session.flash(("You set the active card.", "success"))
    return HTTPFound("/billing")
