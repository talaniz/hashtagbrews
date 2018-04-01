Hashtag Brews
=============

[![Build Status](https://travis-ci.org/talaniz/hashtagbrews.svg?branch=master)](https://travis-ci.org/talaniz/hashtagbrews)

A Django based site that will contain the following applications:
* An open source beer database containing a catalogue of hops, grains and yeasts
* A homebrew planner and timer to track the stages of a brewing process
* A vendor site where homebrew supply vendors can track their inventories
* A homebrew recipe creator that will allow brewers to create a recipe with the options to use ingredients based on a vendor's inventory and choose a pre-planned recipe from a vendor

## Setup

1. Download Python 3 and install at https://python.org
2. Install virtualenv
3. Create virtualenv with python3 executable and activate
4. Create project directory and cd into directory
5. Clone using git: ``` $ git clone https://github.com/talaniz/hashtagbrews.git```
6. Run unit tests: ```python manage.py test``` (should be run with development settings)
7. Run ```python manage.py test functional_tests``` (should be run with development settings)
8. If tests pass, ready to contribute!

## Planning

1. Homebrew Materials Database

    * Finish functional test to add hops (includes unit tests to save to db, etc.) - Completed
    * Refactor to use templating - Completed
    * Add grains and yeasts code - Completed
    * Test Suites: tests for all 3 models - Completed
    * Add error handling - Completed
    * Move to class based views - Completed
    * Add update and delete views - Completed
    * Add user authentication - Completed
    * Add user registration - Completed

2. Homebrew Planner and Timer
    * Needs planning

3. Vendor/Inventory Site
    * Needs planning

4. Hombrew Recipe Creator
    * Needs planning

## To Do
* Homebrew database and hops pages need additional formatting
* Sprint planning for homebrew planner, inventory site and homebrew recipe creator
