from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


def send_invoice_email(to_email, context):
    try:
        html_content = render_to_string('invoice.html', context)
        email = EmailMessage(
            subject="Your Invoice",
            body=html_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[to_email]
        )
        
        # Mark the email as HTML
        email.content_subtype = "html"
        
        # Send the email
        email.send()
        print(f"Invoice email sent to {to_email}")
        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
        


def send_hi_email():
    print("mail send")
    subject = "Hello!"
    message = "Hi"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["dineshr33404@gmail.com"]  # Change to the actual recipient

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,  # Will raise exception if something goes wrong
    )

    print("Email sent successfully!")
 