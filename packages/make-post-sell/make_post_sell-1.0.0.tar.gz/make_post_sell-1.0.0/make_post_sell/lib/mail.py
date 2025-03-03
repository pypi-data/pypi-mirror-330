# quote email address in OTP so that a plus address
# is not  decoded as a space during authentication.
try:
    # Python 2.
    from urllib import quote_plus
except ImportError:
    # Python 3.
    from urllib.parse import quote_plus

from make_post_sell.lib.mail_messages import (
    WELCOME_1_TEXT,
    WELCOME_1_HTML,
    PURCHASE_1_TEXT,
    PURCHASE_1_HTML,
    SALE_1_TEXT,
    SALE_1_HTML,
    INVITE_1_TEXT,
    INVITE_1_HTML,
)

import dkim
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Catch socket errors when postfix isn't running...
from socket import error as socket_error
import logging

log = logging.getLogger(__name__)


def send_email(
    to_email,
    sender_email,
    subject,
    message_text,
    message_html,
    relay="localhost",
    dkim_private_key_path="",
    dkim_selector="",
    dkim_signature_algorithm="ed25519-sha256",
    debug_mode=False,
):
    # The `email` library assumes it is working with string objects.
    # The `dkim` library assumes it is working with byte objects.
    # This function performs the acrobatics to make them both happy.

    if isinstance(message_text, bytes):
        # Needed for Python 3.
        message_text = message_text.decode()

    if isinstance(message_html, bytes):
        # Needed for Python 3.
        message_html = message_html.decode()

    sender_domain = sender_email.split("@")[-1]
    msg = MIMEMultipart("alternative")
    msg.attach(MIMEText(message_text, "plain"))
    msg.attach(MIMEText(message_html, "html"))
    msg["To"] = to_email
    msg["From"] = sender_email
    msg["Subject"] = subject

    try:
        # Python 3 libraries expect bytes.
        msg_data = msg.as_bytes()
    except:
        # Python 2 libraries expect strings.
        msg_data = msg.as_string()

    if dkim_private_key_path and dkim_selector:
        try:
            # The dkim library uses regex on byte strings so everything
            # needs to be encoded from strings to bytes.
            with open(dkim_private_key_path) as fh:
                dkim_private_key = fh.read()
            headers = [b"To", b"From", b"Subject"]
            sig = dkim.sign(
                message=msg_data,
                selector=str(dkim_selector).encode(),
                domain=sender_domain.encode(),
                privkey=dkim_private_key.encode(),
                include_headers=headers,
                signature_algorithm=dkim_signature_algorithm.encode(),
            )
            # Add the dkim signature to the email message headers.
            # Decode the signature back to string_type because later on
            # the call to msg.as_string() performs its own bytes encoding...
            msg["DKIM-Signature"] = sig[len("DKIM-Signature: ") :].decode()

            try:
                # Python 3 libraries expect bytes.
                msg_data = msg.as_bytes()
            except AttributeError:  # For Python 2 compatibility
                # Python 2 libraries expect strings.
                msg_data = msg.as_string()
        except Exception as e:
            if debug_mode:
                log.error(f"DKIM signing failed: {str(e)}")
            raise

    try:
        s = smtplib.SMTP(relay)
        s.sendmail(sender_email, [to_email], msg_data)
        s.quit()
        return msg
    except (socket_error, smtplib.SMTPException) as e:
        error_msg = f"Failed to send email: {str(e)}"

        if debug_mode:
            # Log the error first for quick scanning
            log.error(error_msg)
            # Then log the email details
            log.info(
                f"""

Email Contents:
To: {to_email}
From: {sender_email}
Subject: {subject}

Text Content:
{message_text}

HTML Content:
{message_html}
                """
            )

        if not debug_mode:
            raise
        return None


def send_pyramid_email(request, to_email, subject, message_text, message_html):
    """Thin wrapper around `send_email` to customize settings using request object."""
    default_sender = f"no-reply@{request.domain}"
    sender_email = request.app.get("email.sender", default_sender)
    subject = f"{subject} | {request.app.get('email.subject_postfix', request.domain)}"
    relay = request.app.get("email.relay", "localhost")
    dkim_private_key_path = request.app.get("email.dkim_private_key_path", "")
    dkim_selector = request.app.get("email.dkim_selector", "")
    dkim_signature_algorithm = request.app.get(
        "email.dkim_signature_algorithm", "ed25519-sha256"
    )

    send_email(
        to_email,
        sender_email,
        subject,
        message_text,
        message_html,
        relay,
        dkim_private_key_path,
        dkim_selector,
        dkim_signature_algorithm,
        request.debug_mode,
    )


def send_verification_digits_to_email(request, to_email, raw_digits):
    """
    Send email with raw_digits a user may pass to verify & authenticate.

    request
      the request (of the successful log in attempt)

    to_email
      the email address to send the raw_digits

    raw_digits:
      the raw (unencrypted) digits the user may use to verify & authenticate.
    """
    subject = f"Verification Code | {raw_digits}"
    message_text = WELCOME_1_TEXT.format(raw_digits)
    message_html = WELCOME_1_HTML.format(subject, raw_digits)
    send_pyramid_email(request, to_email, subject, message_text, message_html)


def send_purchase_email(request, to_email, products, total_cost):
    """
    Send purchase email to customer.

    request
      the request (of the successful log in attempt)

    to_email
      the email address to send the email to.

    products
      the list of products that the customer purchased.

    total_cost
      the total transaction price.
    """
    subject = "Your purchase was successful!"
    product_text_list = []
    for p in products:
        thumbnail = ""
        if "thumbnail1" in p.extensions:
            thumbnail = '<img src="{}/{}/thumbnail1?ts={}" style="border: 1px solid #ddd; border-radius: 4px; max-width: 184px; max-height: 184px; width: auto; height: auto;" />'.format(
                request.app["bucket.secure_uploads.get_endpoint"],
                p.s3_path,
                p.updated_timestamp,
            )

        product_text_list.append(
            f'<p><a href="{p.absolute_url(request)}">{p.title}<br/>{thumbnail}</a></p>'
        )
    product_text = "<br/>".join(product_text_list)

    message_text = PURCHASE_1_TEXT.format(f"{total_cost:.2f}", request.host_url)
    message_html = PURCHASE_1_HTML.format(
        subject, request.host_url, product_text, f"{total_cost:.2f}"
    )
    send_pyramid_email(request, to_email, subject, message_text, message_html)


def send_sale_email(request, shop, products, total_cost):
    """
    Send an email to all shop owners regarding the sale.

    request
      the request (of the successful log in attempt)

    shop
      the shop that made the sale

    products
      the list of products that the customer purchased.

    total_cost
      the total transaction price.
    """
    subject = "You made a sale!"
    product_text_list = []
    for p in products:
        thumbnail = ""
        if "thumbnail1" in p.extensions:
            thumbnail = '<img src="{}/{}/thumbnail1?ts={}" style="border: 1px solid #ddd; border-radius: 4px; max-width: 184px; max-height: 184px; width: auto; height: auto;" />'.format(
                request.app["bucket.secure_uploads.get_endpoint"],
                p.s3_path,
                p.updated_timestamp,
            )

        product_text_list.append(
            f'<p><a href="{p.absolute_url(request)}">{p.title}<br/>{thumbnail}</a></p>'
        )
    product_text = "<br/>".join(product_text_list)

    message_text = SALE_1_TEXT.format(
        f"{total_cost:.2f}", shop.absolute_sales_url(request)
    )
    message_html = SALE_1_HTML.format(
        subject, shop.absolute_sales_url(request), product_text, f"{total_cost:.2f}"
    )

    # Send a separate email for each shop owner.
    for user in shop.users:
        send_pyramid_email(request, user.email, subject, message_text, message_html)


def send_invite_email(request, to_email, user, shop):
    """
    Send an email to invite a user to join a shop.

    request
      the request (of the invitation)

    to_email
      the email address to send the shop invitation to.

    user
      the user who sent the invite.

    shop
      the shop the invitation is for.
    """
    subject = f"You have been invited to {shop.name}"
    join_link = request.route_url(
        "join-or-log-in",
        _query={"email": to_email},
    )
    message_text = INVITE_1_TEXT.format(user.email, shop.name, join_link)
    message_html = INVITE_1_HTML.format(subject, user.email, shop.name, join_link)
    send_pyramid_email(request, to_email, subject, message_text, message_html)
