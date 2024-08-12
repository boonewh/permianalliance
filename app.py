from flask import Flask, render_template, request, redirect, url_for, flash
from forms import ContactForm
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'secret'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.yourmailserver.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True


mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/shower')
def shower():
    return render_template('shower.html') 

@app.route('/environmental')
def environmental():
    return render_template('environmental.html') 

@app.route('/office')
def office():
    return render_template('office.html') 

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(form.subject.data,
                      sender=form.email.data,
                      recipients=['boonewh'])
        msg.body = f"""
        This email was sent from the website contact form.
        From: {form.name.data} <{form.email.data}>
        Subject: {form.subject.data}

        {form.message.data}
        """
        mail.send(msg)
        flash('Thank you for your message. We\'ll get back to you shortly.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)