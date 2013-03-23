
# local settings like database connection ect...
#####################################################################

DATABASE_NAME = '%(DATABASE_NAME)s'    # Or path to database file if using sqlite3.
DATABASE_HOST = '%(DATABASE_HOST)s'                      # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '%(DATABASE_PORT)s'                      # Set to empty string for default. Not used with sqlite3.


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = '%(TIMEZONE)s'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '%(STATIC_ROOT_FULL)s'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '%(STATIC_URL)s'


# Celery Broker Configuration
BROKER_HOST = '%(BROKER_HOST)s'
BROKER_PORT = %(BROKER_PORT)
BROKER_VHOST = '%(BROKER_VHOST)s'



# import premade role
ROLE = "%(ROLE)s"