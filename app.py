import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from forms import ContactForm
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret')

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'mail.gandi.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') 

# Configure reCAPTCHA
app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get('RECAPTCHA_PRIVATE_KEY')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/shower')
def shower():
    return render_template('shower.html') 

@app.route('/climate')
def climate():
    return render_template('climate.html') 

@app.route('/office')
def office():
    return render_template('office.html') 

@app.route('/trash')
def trash():
    return render_template('trash.html')

@app.route('/outfitting')
def outfitting():
    return render_template('outfitting.html')

@app.route('/pressure')
def pressure():
    return render_template('pressure.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')  # Get your API key from environment variable
    
    if form.validate_on_submit():
        app.logger.info("Form validated successfully.")  # Log successful validation
        try:
            msg = Message(
                subject=form.subject.data,
                sender=app.config['MAIL_USERNAME'],  # verified sender
                recipients=['hryan@permianalliance.com'],
                reply_to=form.email.data
            )
            msg.body = f"""
            This email was sent from the Permian Alliance website contact form.
            From: {form.name.data} <{form.email.data}>
            Subject: {form.subject.data}

            {form.message.data}
            """
            mail.send(msg)
            app.logger.info("Email sent successfully.")  # Log email send success
            flash("Thank you for your message. We'll get back to you shortly.", "success")
            return redirect(url_for('contact', success=True))
        except Exception as e:
            app.logger.error("Error sending email: %s", e)  # Log any email errors
            flash("An error occurred while sending your message. Please try again later.", "danger")
    else:
        app.logger.warning("Form validation failed: %s", form.errors)  # Log validation errors
        if form.recaptcha.errors:
            app.logger.warning("reCAPTCHA validation errors: %s", form.recaptcha.errors)  # Log reCAPTCHA-specific errors

    return render_template('contact.html', form=form, success=request.args.get('success') == 'True', google_maps_api_key=google_maps_api_key)


@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')

@app.route('/ContactUs.html')
def redirect_contactus_html():
    return redirect(url_for('contact'))

@app.route('/ContactUs')
def redirect_to_contact():
    return redirect(url_for('contact'))

if __name__ == '__main__':
    app.run(debug=True)