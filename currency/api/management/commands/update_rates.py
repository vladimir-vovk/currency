from django.core.management.base import BaseCommand, CommandError
from api.models import Currency, Rate
import urllib.request, json


class Command(BaseCommand):
    help = 'Update rates from https://openexchangerates.org'

    def handle(self, *args, **options):
        # get rates from external api
        response = urllib.request.urlopen(urllib.request.Request(
            'https://openexchangerates.org/api/latest.json?app_id=de9f58366488451fa3d6ac53c101e6fa')).read()
        data = json.loads(response.decode('utf-8'))

        # update our rates
        currencies = Currency.objects.all()

        for currency in currencies:
            # check if rate value exist
            rate_value = data['rates'].get(currency.name)
            if (not rate_value):
                raise CommandError('Rate for {0} not found!'.format(currency.name))

            # update all not obsolete rates
            Rate.objects.filter(currency=currency, obsolete=False).update(obsolete=True)

            # add new rate
            rate = Rate.objects.create(currency=currency, value=rate_value)
            rate.save()

            # self.stdout.write('{0} = {1} updated!'.format(currency.name, rate_value))

        self.stdout.write('Rates successfully updated!')
