from django_selenium.management.commands import test_selenium

class Command(test_selenium.Command):

    def handle(self, *test_labels, **options):
        super(Command, self).handle(*test_labels, **options)
