import logging
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

logger = logging.getLogger(__name__)


@require_POST
def submit_contact(request):
    """Handle contact form submissions with dual HTML and JSON support."""
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or \
              request.content_type == 'application/json' or \
              request.headers.get('accept') == 'application/json'

    form = ContactForm(request.POST)
    if form.is_valid():
        contact_message = form.save()

        # Optional email notification
        if getattr(settings, 'EMAIL_HOST', None) and getattr(settings, 'CONTACT_RECIPIENT_EMAIL', None):
            try:
                send_mail(
                    subject=f"New Portfolio Message from {contact_message.name}",
                    message=(
                        f"From: {contact_message.name} <{contact_message.email}>\n\n"
                        f"Message:\n{contact_message.message}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                logger.warning(f"Could not dispatch email notification: {e}")

        success_text = "Thank you! Your message has been sent successfully. I will get back to you shortly."
        if is_ajax:
            return JsonResponse({'status': 'success', 'message': success_text})

        messages.success(request, success_text)
        return redirect('/#contact')

    # If errors occurred
    error_msg = "Please check the form fields and try again."
    if form.errors:
        first_err = next(iter(form.errors.values()))[0]
        error_msg = f"{first_err}"

    if is_ajax:
        return JsonResponse({'status': 'error', 'message': error_msg, 'errors': form.errors}, status=400)

    messages.error(request, error_msg)
    return redirect('/#contact')

