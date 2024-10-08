import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from forms import ContactForm
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret')

# Configure Flask-Mail for Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # Your Gmail address
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # Your Gmail app password

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
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY') # Get your API key from https://console.developers.google.com
    if form.validate_on_submit():
        msg = Message(form.subject.data,
                      sender=form.email.data,
                      recipients=['boonewh@gmail.com'])
        msg.body = f"""
        This email was sent from the Permian Alliance website contact form.
        From: {form.name.data} <{form.email.data}>
        Subject: {form.subject.data}

        {form.message.data}
        """
        mail.send(msg)
        flash('Thank you for your message. We\'ll get back to you shortly.', 'success')
        return redirect(url_for('contact', success=True))
    return render_template('contact.html', form=form, success=request.args.get('success', False), google_maps_api_key=google_maps_api_key)

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