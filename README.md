# Koytola Backend & API Development
Koytola development repo center. Django backend with GraphQL API, dashboard and sitefront with typescript repositories can be found here.


## Database
At the moment, development database is django default db.splite3. Yet, everything is set for PostgreSQL and PostgreSQL is used in production. <br>
In order to setup the database, run makemigrations and migrate commands in venv:
```
python manage.py makemigrations
python manage.py migrate
```

## Dummy Data
When you pull the repository, run following commands in koytola dir:
```
python manage.py setup_site_settings
python manage.py populatedb --createsuperuser
```
This will generate dummy data for the platform with following superuser:<br>
email: admin@koytola.com<br>
password: admin<br>

## Django Admin Interface
For now, admin interface can be reached on /admin/ with superuser credentials.

## GraphQL API
API url can be reached on /graphql/. In order to view graphql playground, admins need to sign in on /admin/ interface.

In order to make mutations with API endpoints, users, staff members or superusers required create token with following commands on graphql playground:
```
mutation {
  tokenCreate(email: "admin@koytola.com", password: "admin") {
    token
  }
}
```

Then, copy the token in playground HTTP Headers in following format:
```
{
  "Authorization": "JWT your-token"
}
```

Then you can make mutations as the user type of token owner.

## Env Parameters
In koytola directory (same dir with settings.py), create .env file and add following parameters:
```
DEBUG=True
SECRET_KEY=<key>
CACHE_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
JWT_VERIFY_EXPIRATION=True
```
You can use any 50 character as SECRET_KEY for django. Replace <key> on the 2nd line with a secret key, similar to the example below. <br>
Example django key: %7j$x8c&2y6j$%4b3nd=pmy#^b6sp@8sc3r!d25=im4ukd8aip <br>
Ref: https://docs.djangoproject.com/en/3.1/ref/settings/#secret-key <br>

