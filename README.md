![hashtagbrews.jpg](https://bitbucket.org/repo/XyqX5R/images/4021472849-hashtagbrews.jpg)
=============

Hashtag Brews is a Django based site that will contain the following applications:

* An open source beer database containing a catalogue of hops, grains and yeasts
* A homebrew planner and timer to track the stages of a brewing process
* A vendor site where homebrew supply vendors can track their inventories
* A homebrew recipe creator that will allow brewers to create a recipe with the options to use ingredients based on a vendor's inventory and choose a pre-planned recipe from a vendor

## Setup

1. Download Python 3 and install at https://python.org
2. Install virtualenv
3. Create virtualenv with python3 executable and activate
4. Create project directory and cd into directory
5. Clone using git: ``` $ git clone https://talaniz715@bitbucket.org/talaniz715/hashtagbrews.git/wiki```
6. Run unit tests: ```python manage.py test```
7. Run ```python manage.py runserver``` then run functional_tests ```python functional_tests.py```
8. If tests pass, ready to contribute!

## Planning
### [Sprint Plans Detail] ###
[Sprint Plans Detail]: https://bitbucket.org/talaniz715/hashtagbrews/wiki/Sprint%20Planning

### [Page Design Mockups Here] ###
[Page Design Mockups Here]: https://bitbucket.org/talaniz715/hashtagbrews/wiki/Catalogue%20Page%20Designs

1. Homebrew Materials Database
    * Finish functional test to add hops (includes unit tests to save to db, etc.) - Completed
    * Refactor to use templating - Completed
    * Add edit and delete hops views - edit completed
    * Add grains and yeasts code
    * Test Suites: Adjust tests to test all 3 categories at once (hops, grains, yeasts)
    * Add error handling
    * Move to class based views
    * Add update and delete views
    * Add user authentication.

2. Homebrew Planner and Timer
    * Needs planning

3. Vendor/Inventory Site
    * Needs planning

4. Hombrew Recipe Creator
    * Needs planning

## To Do
* Homebrew database and hops pages need additional formatting
* Template refactoring with `{% include 'page.html %}'` tags
* Unit and functional tests for grains and yeasts
* Convert functional and unit tests to test suites
* Sprint planning for homebrew planner, inventory site and homebrew recipe creator

## Code Coverage Status


|             Name            | Stmts  |  Miss   | Cover |
|:---------------------------:|:------:|:-------:|:-----:|
|homebrewdatabase/admin.py    |    1   |    0    | 100%  |
|homebrewdatabase/forms.py    |    7   |    0    | 100%  |
|homebrewdatabase/models.py   |   21   |    1    |  95%  |
|homebrewdatabase/views.py    |   27   |    2    |  93%  |
|manage.py                    |    6   |    0    | 100%  |
|TOTAL                        |    62  |     3   |  95%  |
