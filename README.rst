========================
Django Selenium Integration
========================

.. contents::

What is it?
===========
| **Django-selenium** is a toolset that provides seamless integration for Django_ framework
  with a Selenium_ testing tool.
It allows to write and execute **selenium tests** just as usual ones.

Dependencies
============
* Django_ 1.2 and above.
* Selenium_ 2.5.0 and above.

* django-jenkins_ if you are going to use **JenkinsTestRunner** from this package.

How do I use it?
================

1. Update ``settings.TEST_RUNNER = 'django_selenium.test_runner.SeleniumTestRunner'``
   or subclass ``SeleniumTestRunner`` to make your own test runner with
   extended functionaliity.
2. Include selenium-specific settings in your own settings file.
   One setting that you must always define is ``SELENIUM_PATH``.
   It should point to the selenium-server.jar on your system, for example
   ``/home/dragoon/selenium-server-2.6.jar``
   See ``settings.py`` for other settings available.
3. Write some selenium tests for your apps in a module ``seltests.py``.
   Subclass selenium tests from ``django_selenium.testcases.SeleniumTestCase``.
4. Add custom management command to override default test command::

       from django_selenium.management.commands import test_selenium

       class Command(test_selenium.Command):

           def handle(self, *test_labels, **options):
               super(Command, self).handle(*test_labels, **options)

   Place it somewhere in your app in ``management/commands/test.py`` (don't
   forget the __init__.py files in each directory)

5. Run ``manage.py test`` like you normally do. Now you have two extra options: ``--selenium`` and ``--selenium-only``.
   First runs selenium-specific tests after the usual ones, the last runs only selenium tests.

And that's it.

To see the integration in action, please check out test application: https://github.com/dragoon/django-selenium-testapp

Django Jenkins
==============

There is also a special test runner to execute selenium tests using django-jenkins integration:
``django_selenium.jenkins_runner.JenkinsTestRunner``. You can specify this class for ``TEST_RUNNER`` setting,
and ``manage.py jenkins`` command will also execute selenim tests and generate reports for them.

MyDriver class
==============

| ``MyDriver`` class from ``django_selenium.tescases`` offers extended functionality on top of ``selenium.webdriver.remote.webdriver.WebDriver`` class.
It has a number of convinient shortcuts to handle frequently used operations, see source code for details, documentation will be here soon.

.. _Django: http://www.djangoproject.com/
.. _Selenium: http://seleniumhq.org/
.. _django-jenkins:https://github.com/kmmbvnr/django-jenkins


South
=====

You use South to migrate your applications ? Ok, south is also overriding the
django test commands, therefore you will need to modify your custom management
command as follow::

    from django_selenium.management.commands import test_selenium
    from south.management.commands import test as test_south

    class Command(test_south.Command, test_selenium.Command):

       def handle(self, *test_labels, **options):
           super(Command, self).handle(*test_labels, **options)


    You still need to have SOUTH_TESTS_MIGRATE = False in your test_settings.py

