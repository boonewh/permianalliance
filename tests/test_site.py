import json
import os
from pathlib import Path
import re
import ssl
import subprocess
import sys
import unittest
from unittest.mock import patch

os.environ['SECRET_KEY'] = 'local-test-only-permian-secret'
os.environ['RECAPTCHA_PUBLIC_KEY'] = 'local-test-key'
os.environ['RECAPTCHA_PRIVATE_KEY'] = 'local-test-private'
os.environ['MAIL_USERNAME'] = 'sender@example.com'
from app import app, mail
from secure_mail import VerifiedConnection


class SiteTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, WTF_CSRF_ENABLED=True, RECAPTCHA_ENABLED=True)
        self.client = app.test_client()
        self.fields = dict(name='Test Visitor', email='visitor@example.com',
                           subject='Fittings inquiry', message='Please quote a poly tee.')

    def token(self):
        page = self.client.get('/contact').get_data(as_text=True)
        return re.search(r'name="csrf_token"[^>]*value="([^"]+)"', page)[1]

    def test_pages_assets_and_structured_data(self):
        for route in ('/', '/shower', '/climate', '/office', '/trash', '/outfitting', '/pressure', '/heaters', '/steamer', '/contact'):
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)
            html = response.get_data(as_text=True)
            data = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)[1])
            self.assertEqual(data['telephone'], '+1-432-250-4778')
            self.assertIn('1701 E County Rd 148', html)
        for asset in Path('static').rglob('*'):
            if asset.is_file():
                with self.client.get('/'+asset.as_posix()) as response:
                    self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get('/absent').status_code, 404)

    def test_sitemap_and_contact_redirects(self):
        import xml.etree.ElementTree as ET
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        ET.fromstring(response.data)
        response.close()
        for route in ('/ContactUs.html', '/ContactUs'):
            response = self.client.get(route)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/contact')

    def test_success_keeps_recipient_sender_and_reply_to(self):
        with patch.object(mail, 'send') as send:
            response = self.client.post('/contact', data={**self.fields, 'csrf_token':self.token()})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/contact?success=True')
        message = send.call_args.args[0]
        self.assertEqual(message.recipients, ['hryan@permianalliance.com'])
        self.assertEqual(message.sender, 'sender@example.com')
        self.assertEqual(message.reply_to, self.fields['email'])
        self.assertIn(self.fields['message'], message.body)
        self.assertIn(b'Thank you', self.client.get(response.location).data)

    def test_missing_csrf_rejects_mail(self):
        with patch.object(mail, 'send') as send:
            self.client.post('/contact', data=self.fields)
            send.assert_not_called()

    def test_recaptcha_stays_enabled_outside_testing(self):
        token = self.token()
        app.config['TESTING'] = False
        with patch.object(mail, 'send') as send:
            self.assertEqual(self.client.post('/contact', data={**self.fields, 'csrf_token':token}).status_code, 200)
            send.assert_not_called()

    def test_mail_failure_does_not_disclose_exception(self):
        with patch.object(mail, 'send', side_effect=RuntimeError('private SMTP credential detail')):
            response = self.client.post('/contact', data={**self.fields, 'csrf_token':self.token()})
        self.assertIn(b'Please try again later', response.data)
        self.assertNotIn(b'private SMTP credential detail', response.data)

    def test_invalid_and_oversized_fields_rejected(self):
        for changes in ({'name':''}, {'email':'invalid'}, {'subject':'writing offer'}, {'email':'kayleighbpsteamship@gmail.com'},
                        {'subject':'inquiry\r\nBcc: attacker@example.com'},
                        {'subject':'x'*201}, {'message':'x'*10001}):
            with self.subTest(changes=list(changes)):
                with patch.object(mail, 'send') as send:
                    self.client.post('/contact', data={**self.fields, **changes, 'csrf_token':self.token()})
                    send.assert_not_called()
        response = self.client.post('/contact', data={'message':'x'*70000})
        self.assertEqual(response.status_code, 413)

    def test_required_secret(self):
        for secret in ('', 'default_secret'):
            env = dict(os.environ, SECRET_KEY=secret)
            result = subprocess.run([sys.executable, '-c', 'import app'], env=env, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b'Set SECRET_KEY', result.stderr)

    def test_smtp_tls_verified_before_login(self):
        with patch('secure_mail.smtplib.SMTP') as smtp:
            with app.app_context():
                connection = VerifiedConnection(app.extensions['mail'])
                connection.configure_host()
            context = smtp.return_value.starttls.call_args.kwargs['context']
            self.assertTrue(context.check_hostname)
            self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
            self.assertEqual(smtp.call_args.kwargs['timeout'], 15)
        with patch('secure_mail.smtplib.SMTP') as smtp:
            smtp.return_value.starttls.side_effect = ssl.SSLCertVerificationError('untrusted')
            with app.app_context():
                with self.assertRaises(ssl.SSLCertVerificationError):
                    VerifiedConnection(app.extensions['mail']).configure_host()
            smtp.return_value.login.assert_not_called()
            smtp.return_value.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
