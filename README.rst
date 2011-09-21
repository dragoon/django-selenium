========================
Django Test Coverage App
========================

.. contents::

What is it?
===========
A test coverage reporting tool that utilizes `Ned Batchelder`_'s
excellent coverage.py_ to show how much of your code is exercised with
your tests.

Dependencies
============
* Django_ 1.2 and above.
* Selenium_ 2.5.0 and above.

How do I use it?
================
Install as a Django app
-----------------------
1. Place the entire ``django_coverage`` app in your third-party apps
   directory.
2. Update your ``settings.INSTALLED_APPS`` to include ``django_coverage``.
3. Include test coverage specific settings in your own settings file.
   See ``settings.py`` for more detail.

Once you've completed all the steps, you'll have a new custom command
available to you via ``manage.py test_coverage``. It works just like
``manage.py test``.

Use it as a test runner
-----------------------
You don't have to install ``django_coverage`` as an app if you don't want
to. You can simply use the test runner if you like.

1. Update ``settings.TEST_RUNNER =
   'django_seleinum.test_runner.SeleniumTestRunner'``
2. Include specific selenium settings in your own settings file.
   See ``settings.py`` for more detail.
3. Run ``manage.py test`` like you normally do.

And that's it.


.. _Django: http://www.djangoproject.com/
.. _Selenium: http://seleniumhq.org/
