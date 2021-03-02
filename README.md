# Build status

[![image](https://api.travis-ci.org/ustream/openduty.svg)](https://travis-ci.org/ustream/openduty)
[![Requirements Status](https://requires.io/github/forkwhilefork/openduty/requirements.svg?branch=master)](https://requires.io/github/forkwhilefork/openduty/requirements/?branch=master)


# What is this?
**Openduty** is an incident escalation tool, just like [Pagerduty](http://pagerduty.com). It has a Pagerduty-compatible API too.

# Integrations
Has been tested with Nagios, works well for us. Any Pagerduty Notifier using the Pagerduty API should work without a problem.
[Icinga2 config](https://github.com/deathowl/OpenDuty-Icinga2) for openduty integration

# Notifications
XMPP, email, SMS, Phone (via Twilio), Push notifications (via Pushover and Prowl), and Slack, HipChat, Rocket.chat are supported at the moment.

# Current status
Openduty is in Beta status, it can be considered stable at the moment, however major structural changes can appear anytime (not affecting the API, or the Notifier structure)

# Contribution guidelines
Yes, please. You are welcome.

# Feedback
Any feedback is welcome

# Getting started:
```
sudo easy_install pip
sudo pip install virtualenv
virtualenv env --python python2.7
. env/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=openduty.settings_dev
python manage.py syncdb
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```
now, you can start hacking on it.

# Running as a service with systemd
*OpenDuty can be ran as a service with the help of gunicorn and systemd*
```
cp -r systemd/gunicorn.service.* /etc/systemd/system/

cp -r systemd/celery.service* /etc/systemd/system/

// EDIT VARIABLES IN *.service.d/main.conf TO REFLECT YOUR ENV
vi /etc/systemd/system/gunicorn.service.d/main.conf
vi /etc/systemd/system/celery.service.d/main.conf

systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

```

# After you've changed your models please run:
```
./manage.py schemamigration openduty --auto
./manage.py schemamigration notification --auto
./manage.py migrate

```

# If you see a new file appearing in migrations directory when pulling from upstream please run
```
./manage.py migrate
```

# Default login:
root/toor

# Celery worker:
```
celery -A openduty worker -l info
```

# Login using basic authentication with LDAP-backend

Add the following snippet to your settings_prod/dev.py, dont forget about import

```
AUTH_LDAP_SERVER_URI = "ldap://fqdn:389"
AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_START_TLS = False
AUTH_LDAP_MIRROR_GROUPS = True #Mirror LDAP Groups as Django Groups, and populate them as well.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=Group,dc=domain,dc=com",
    ldap.SCOPE_SUBTREE, "(&(objectClass=posixGroup)(cn=openduty*))"
)
AUTH_LDAP_GROUP_TYPE = PosixGroupType()

AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=People,dc=domain,dc=com",
ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_USER_ATTR_MAP = {
"first_name": "uid",
"last_name": "sn",
"email": "mail"
}


AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
  'openduty.middleware.basicauthmiddleware.BasicAuthMiddleware',
)

```
