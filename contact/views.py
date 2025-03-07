from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import ContactForm


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()  # Save to database

            # Send an email notification
            send_mail(
                subject=f"New Inquiry from {contact_message.name}",
                message=f"From: {contact_message.email}\n\n{contact_message.message}",
                from_email="contact@petwellnessvets.com",
                recipient_list=["contact@petwellnessvets.com"],
                fail_silently=False,
            )

            return redirect("contact_success")  # Redirect to thank you page

    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})

