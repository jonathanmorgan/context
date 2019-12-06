# context

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3523031.svg)](https://doi.org/10.5281/zenodo.3523031)

Generalized django application framework for tracking entities and traits of and relations between them.

<!-- TOC -->

context is a django application for capturing entities and relationships between entities.

# Installation and configuration

I've created ansible scripts with all the steps that you can configure and run against Ubuntu 18.04 or 16.04 (VM, cloud server, or physical machine).

These scripts are in my "ansible-patterns" repository: [https://github.com/jonathanmorgan/ansible-patterns](https://github.com/jonathanmorgan/ansible-patterns)

These ansible scripts can also be used to just setup a server with virtualenvwrapper, postgresql, apache, django, jupyterhub, and R, without context.  See the readme for detailed instructions.

Chances are I'll make dockerfile(s) for this eventually, too, but for now, there's ansible.

I've left in a few notes below, regarding different package and installation choices, but the best doc is the ansible repo.

## Python packages

- depending on database:

    - postgresql - psycopg2 - Before you can connect to Postgresql with this code, you need to do the following (based on [http://initd.org/psycopg/install/](http://initd.org/psycopg/install/)):

        - install the PostgreSQL client if it isn't already installed.  On linux, you'll also need to install a few dev packages (python-dev, libpq-dev) ( [source](http://initd.org/psycopg/install/) ).
        - install the psycopg2 python package.  Install using pip (`sudo pip install psycopg2`).  
        
    - mysql - mysqlclient - Before you can connect to MySQL with this code, you need to do the following:
    
        - mysqlclient

            - install the MySQL client if it isn't already installed.  On linux, you'll also need to install a few dev packages (python-dev, libmysqlclient-dev) ( [source](http://codeinthehole.com/writing/how-to-set-up-mysql-for-python-on-ubuntu/) ).
            - install the mysqlclient python package using pip (`(sudo) pip install mysqlclient`).

- python packages that I find helpful:

    - ipython - `(sudo) pip install ipython`

## settings.py - Configure logging, database, applications:

The following are some django settings you might want to tweak in the settings.py file in your django project.  If you created a project named "research", this will be located at `research/research/settings.py`.

### logging

Edit the `research/research/settings.py` file and update it with details of your logging configuration
    
- Example that logs any messages INFO and above to standard out:

        import logging

        logging.basicConfig(
            level = logging.INFO,
            format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        )

- Example that logs any messages INFO and above to a file:

        import logging

        logging.basicConfig(
            level = logging.INFO,
            format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            filename = '<log_folder>/django-context_text.log',
            filemode = 'w'
        )

    - WHERE `<log_folder>` is a folder that any users that will be used to interact with context_text have access to.  This includes the user your web server runs as (for admins and other django web pages) and the user you use to develop, and so that might run things from the python shell.

        - the easiest way to get this working:

            - make the `<log_folder>` somewhere outside the web root.
            - set the permissions on `<log_folder>` to 777.
            - create the file `django-context_text.log` there.
            - set its permissions also to 777.

        - This is not necessarily optimally secure, but truly securing this is beyond the scope of this README.

- You can set `level` to any of the following, which are organized from most detail (`logging.DEBUG`) to least (`logging.CRITICAL`):

    - `logging.DEBUG`
    - `logging.INFO`
    - `logging.WARNING`
    - `logging.ERROR`
    - `logging.CRITICAL`

- Python logging HOWTO: [https://docs.python.org/2/howto/logging.html](https://docs.python.org/2/howto/logging.html)
- Python logging cookbook: [https://docs.python.org/2/howto/logging-cookbook.html](https://docs.python.org/2/howto/logging-cookbook.html)

### database

Edit the research/research/settings.py file and update it with details of your database configuration.

In general, for any database other than sqlite3, in your database system of choice you'll need to:

- create a database for django to use (I typically use `context_text`).

    - postgresql - at the unix command line:
    
            # su to the postgres user
            su - postgres
            
            # create the database at the unix shell
            #createdb <database_name>
            createdb context_text

- create a database user for django to use that is not an admin (I typically use `django_user`).

    - postgresql - at the unix command line:
    
            # su to the postgres user
            su - postgres
            
            # create the user at the unix shell
            #createuser --interactive -P <username>
            createuser --interactive -P django_user

- give the django database user all privileges on the django database.
- place connection information for the database - connecting as your django database user to the django database - in settings.py.

An example for postgresql looks like this:

    DATABASES = {
        'default': {        
            # PostgreSQL - context_text
            'ENGINE': 'django.db.backends.postgresql', # Add 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'context_text',                      # Or path to database file if using sqlite3.
            'USER': 'django_user',                      # Not used with sqlite3.
            'PASSWORD': '<db_password>',                  # Not used with sqlite3.
            'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
        },
    }

More information:
    
- [https://docs.djangoproject.com/en/dev/intro/tutorial01/#database-setup](https://docs.djangoproject.com/en/dev/intro/tutorial01/#database-setup)
- [https://docs.djangoproject.com/en/dev/ref/settings/#databases](https://docs.djangoproject.com/en/dev/ref/settings/#databases)

# Testing

## Basic tests

- test by going to the URL:

        http://<your_server>/research/admin/

- and then logging in with the django superuser created by ansible scripts.

## Unit Tests

The context project has unit tests that can auto-run.  These tests use django's testing framework, based on the Python `unittest` package.

### Configuration

#### Database configuration

In order to run unit tests, your database configuration in `settings.py` will need to be connecting to the database with a user who is allowed to create databases.  When django runs unit tests, it creates a test database, then deletes it once testing is done.
- _NOTE: This means the database user you use for unit testing SHOULD NOT be the user you'd use in production.  The production database user should not be able to do anything outside a given database._

### Running unit tests

To run unit tests, at the command line in your django project/site folder (where `manage.py` lives):

    python manage.py test context.tests
    
Specific sets of tests:
          
- context model instances:

    - test Entity_Identifier_Type model
    
            python manage.py test context.tests.models.test_Entity_Identifier_Type_model

    - test Entity_Identifier model
    
            python manage.py test context.tests.models.test_Entity_Identifier_model

    - test Entity_Trait model
    
            python manage.py test context.tests.models.test_Entity_Trait_model

    - test Entity model
    
            python manage.py test context.tests.models.test_Entity_model

- Exporting network data:

    - test NetworkDataRequest class
    
            python manage.py test context.tests.export.network.test_NetworkDataRequest_class

## Test data

There is a set of test data stored in the `fixtures` folder inside this django application.  The files:

- **_`context-sourcenet_entities_and_relations.json`_** - Entity and Relation metadata based on sourcenet project.

### Using unittest data for development

- create a database where the unit test data can live.  I usually call it the name of the main production database ("`research`") followed by "`_test`".  Easiest way to do this is to just create the database, then give the same user you use for your production database the same access they have for production for this test database as well.

    - postgresql example, where production database name is "`research`" and database user is "`django_user`":

            CREATE DATABASE research_test;
            GRANT ALL PRIVILEGES ON DATABASE research_test TO django_user;

- update the DATABASES dictionary in settings.py of the application that contains context_text to point to your test database (in easy example above, could just change the 'NAME' attribute in the 'default' entry to "`research_test`" rather than "`research`".
- cd into your django application's home directory, activate your virtualenv if you created one, then run "`python manage.py migrate`" to create all the tables in the database.

        cd <django_app_directory>
        workon research
        python manage.py migrate

- use the command "`python manage.py createsuperuser`" to make an admin user, for logging into the django admins.

        python manage.py createsuperuser

- load the unit test fixtures into the database:

        python manage.py loaddata context-sourcenet_entities_and_relations.json
