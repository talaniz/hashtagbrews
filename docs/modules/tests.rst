Tests
=====

Testing is broken up into 2 parts: unit and functional.
        * Unit: makes uses of the Django (Django Test Client) & Python unit testing framework
        * Functional: uses Selenium in conjunction with the Django Live Server Test Case class

Links and summaries of each section of the test suite are provided below


Functional Testing
------------------

Functional testing is broken up into 2 types of tests:
        * Testing add, update & delete functions
        * Testing form validation


Base Class
^^^^^^^^^^

.. automodule:: functional_tests.base
    :members:
    :exclude-members: FunctionalTest

.. autoclass:: FunctionalTest()
    :members:


Add, Update & Delete
^^^^^^^^^^^^^^^^^^^^

Hops
####

.. automodule:: functional_tests.test_simple_hop_add_update_delete
    :members:
    :exclude-members: NewHopsVisitorTest

.. autoclass:: NewHopsVisitorTest()
    :members:


Grains
######

.. automodule:: functional_tests.test_simple_grain_add_update_delete
    :members:
    :exclude-members: NewGrainVisitorTest

.. autoclass:: NewGrainVisitorTest()
    :members:


Yeasts
######

.. automodule:: functional_tests.test_simple_yeast_add_update_delete
    :members:
    :exclude-members: NewYeastVisitorTest

.. autoclass:: NewYeastVisitorTest()
    :members:


Form Validation
^^^^^^^^^^^^^^^

Hops
####

.. automodule:: functional_tests.test_simple_hop_validation_form
    :members:
    :exclude-members: HopFormValidation

.. autoclass:: HopFormValidation()
    :members:


Grains
######

.. automodule:: functional_tests.test_simple_grain_validation_form
    :members:
    :exclude-Members: GrainFormValidation

.. autoclass:: GrainFormValidation()
    :members:


Yeasts
######

Not yet created



Unit Testing
------------

Unit tests currently cover views, models and forms. Each module contains testing for all 3 models: hops, grains & yeasts
        * Testing Views
        * Testing Models
        * Testing Forms

Testing Views
^^^^^^^^^^^^^

.. automodule:: homebrewdatabase.tests.test_views
    :members:
    :exclude-members: TestHomePageView, TestGrainsPageView, TestHopsPageView, TestYeastPageView

.. autoclass:: TestHomePageView()
    :members:

.. autoclass:: TestHopsPageView()
    :members:

.. autoclass:: TestGrainsPageView()
    :members:

.. autoclass:: TestYeastPageView()
    :members:


Testing Models
^^^^^^^^^^^^^^

.. automodule:: homebrewdatabase.tests.test_models
    :members:
    :exclude-members: HopModelTest, GrainModelTest, YeastModelTest

.. autoclass:: HopModelTest()
    :members:

.. autoclass:: GrainModelTest()
    :members:

.. autoclass:: YeastModelTest()
    :members:


Testing Forms
^^^^^^^^^^^^^

.. automodule:: homebrewdatabase.tests.test_forms
    :members:
    :exclude-members: HopFormTest, GrainFormTest, YeastFormTest

.. autoclass:: HopFormTest()
    :members:

.. autoclass:: GrainFormTest()
    :members:

.. autoclass:: YeastFormTest()
    :members:
