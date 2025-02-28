# Django fobi email router

A django-fobi handler plugin to send the content of a form to different e-mails addresses, depending on a value of a form field.

## Install

1. Install module
   ```bash
   python3 -m pip install djangofobi-email-router
   ```

2. Add it to your INSTALLED_APPS
   ```
   "djangofobi_email_router",
   ```

3. Create a fobi form with at least one choice field (select, select multiple, checkbox select multiple or radio)
4. Add an `E-mail router` handler, fill in the name of your choice field and the e-mails corresponding to the different possible values

### Requirements

* `django-fobi`

## Screenshot

![preview djangofobi-email-router](https://gitlab.com/kapt/open-source/djangofobi-email-router/-/raw/main/preview.png)
