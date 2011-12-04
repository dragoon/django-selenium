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

How to use it
=============

Define **selenium specific** settings in your **settings.py** file.

Local
-----
Local run in this case means that you're using Firefox, Chrome or IE driver, and therefore you don't
need running selenium server, because these drivers work with the browsers directly.

So, if you plan to use **selenium locally**, then you should define the following settings:

-  Set ``SELENIUM_DISPLAY`` if you plan to run selenium tests on display other than "``:0``" (on VNCServer/Xvfb for example).
   See ``settings.py`` for other settings available.

- Set ``SELENIUM_DRIVER`` for corresponding browser driver in selenium.


Remote
------

- Set ``SELENIUM_DRIVER = 'Remote'`` in your settings file.

- Set ``SELENIUM_CAPABILITY`` to the desired value.

-  Probaly set ``SELENIUM_PATH`` to point to the selenium-server.jar on your system, for example
   ``/home/dragoon/selenium-server-2.6.jar``. This setting is required if you want to start
   selenium server along with tests. You don't need this if you keep your selenium server
   running using other methods.

- Set ``SELENIUM_HOST`` to point to the IP/hostname of your remote selenium server.

- Set ``SELENIUM_TESTSERVER_HOST`` to the IP address/hostname of the machine where test server is running
  (e.g. **192.168.1.2**).

See settings.py file to see some examples.

Common
------

#. Set ``TEST_RUNNER = 'django_selenium.test_runner.SeleniumTestRunner'``
   or subclass ``SeleniumTestRunner`` to make your own test runner with
   extended functionaliity.

#. Write some selenium tests for your apps in a module ``seltests.py``.
   Subclass selenium tests from ``django_selenium.testcases.SeleniumTestCase``.
#. Add custom management command to override default test command::

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
``django_selenium.jenkins_runner.JenkinsTestRunner``.

You can specify this class for ``TEST_RUNNER`` setting, and ``manage.py jenkins`` command will also execute selenium tests and generate reports for them.

MyDriver class
==============

| ``MyDriver`` class from ``django_selenium.tescases`` offers extended functionality on top of ``selenium.webdriver.remote.webdriver.WebDriver`` class.
It has a number of convinient shortcuts to handle frequently used operations, see source code for details, documentation will be here soon.

.. _Django: http://www.djangoproject.com/
.. _Selenium: http://seleniumhq.org/
.. _django-jenkins: https://github.com/kmmbvnr/django-jenkins


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

