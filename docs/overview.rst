Overview
========

Hashtag Brews is a Django based site that will contain the following applications:

* An open source beer database containing a catalogue of hops, grains and yeasts
* A homebrew planner and timer to track the stages of a brewing process
* A vendor site where homebrew supply vendors can track their inventories
* A homebrew recipe creator that will allow brewers to create a recipe with the options to use ingredients based on a vendor's inventory and choose a pre-planned recipe from a vendor

Setup
-----

1. Download Python 3 and install at https://python.org
2. Install virtualenv
3. Create virtualenv with python3 executable and activate
4. Create project directory and cd into directory
5. Clone using git (don't forget to install requirements.txt)
    $ git clone https://talaniz715@bitbucket.org/talaniz715/hashtagbrews.git/wiki
6. Run unit tests
    python manage.py test
7. Run `python manage.py runserver` then run functional tests `python functional_tests.py`
8. If tests pass, ready to contribute!

Requirements
------------

Hashtag brews requires the following:

* alabaster==0.7.7
* Babel==2.3.4
* coverage==4.0.3
* Django==1.9.1
* django-coverage-plugin==1.2.2
* django-debug-toolbar==1.4
* django-debug-toolbar-django-info==0.2.0
* django-extensions==1.6.1
* docutils==0.12
* imagesize==0.7.1
* Jinja2==2.8
* MarkupSafe==0.23
* psycopg2==2.6.1
* Pygments==2.1.3
* pytz==2016.4
* selenium==2.52.0
* six==1.10.0
* snowballstemmer==1.2.1
* Sphinx==1.4.1
* sqlparse==0.1.18
* Werkzeug==0.11.4
* wheel==0.24.0

Planning
--------

`Page Design Mockups Here
<https://bitbucket.org/talaniz715/hashtagbrews/wiki/Catalogue%20Page%20Designs>`_

1. Homebrew Materials Database
    * Finish functional test to add hops (includes unit tests to save to db, etc.) - Completed
    * Refactor to use templating - Completed
    * Add edit and delete hops views - Completed
    * Refactor: Homebrew Database Main Page - Completed
    * Add grains and yeasts code - Almost completed
    * Add uniqe record error handling
    * Move to class based views
    * Add user authentication

2. Homebrew Planner and Timer
    * Design & implement pybrew library
    * Initial functional testing for users
    * Database design (one to many, many to many)

3. Vendor/Inventory Site
    * Needs planning
    * UI design for vendor/purchasers

4. Hombrew Recipe Creator
    * Needs planning
    * Braintree API sandbox setup

To Do
-----

* Homebrew database pages need additional tightening (divs)
* Unit and functional tests for yeasts
* Pybrew library development
* Sprint planning for homebrew planner, inventory site and homebrew recipe creator
* Separate local and production environment settings