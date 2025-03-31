from django.shortcuts import render
from .forms import ContactForm
from .email_utils import send_email, send_auto_reply  # Import auto-reply function

def contact_view(request):
    success_message = None  # Initialize success message

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # form.save()

            # Send email to the admin
            subject = f"New Inquiry from {form.cleaned_data['name']}"
            message = f"From: {form.cleaned_data['email']}\n\n{form.cleaned_data['message']}"
            recipient = "contact@petwellnessvets.com"

            try:
                send_email(subject, message, recipient)  # Send admin notification
                send_auto_reply(form.cleaned_data['email'], form.cleaned_data['name'])  # Send auto-reply to user
                success_message = "Your message has been sent successfully!"
            except Exception as e:
                success_message = f"Failed to send email: {str(e)}"

            form = ContactForm()  # Reset form after submission

    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form, "success_message": success_message})
