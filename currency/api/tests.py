from django.test import TestCase
from .models import Currency, Rate
import decimal

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RateTestCase(APITestCase):
    def setUp(self):
        # add some currencies
        usd = Currency.objects.create(name="USD", description="United States Dollar")
        rub = Currency.objects.create(name="RUB", description="Russian Ruble")
        eur = Currency.objects.create(name="EUR", description="Euro")

        # add some rates
        Rate.objects.create(currency=usd, value=1)
        Rate.objects.create(currency=rub, value=55.8066856)
        Rate.objects.create(currency=eur, value=0.8951752)

    def convert_by_hand(self, amount, from_currency, to_currency):
        """
        Supporting function for convert api check.
        """
        from_rate = Rate.objects.get(currency__name=from_currency, obsolete=False).value
        to_rate = Rate.objects.get(currency__name=to_currency, obsolete=False).value
        result = decimal.Decimal(amount) / from_rate * to_rate;
        #print('{0} {1} -> {2} = {3}'.format(amount, from_currency, to_currency, result))

        return result.quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_UP)

    def test_get_all_currencies(self):
        """
        Ensure we can get all currencies.
        """
        url = reverse('currency')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Currency.objects.count())

    def test_get_currency_details(self):
        """
        Currency details.
        """
        data = {'name': 'USD'}
        url = reverse('currency-details', kwargs=data)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rate'], 1)

    def test_get_currency_details_not_found(self):
        """
        Currency details with incorrect currency.
        """
        data = {'name': 'NOTFOUND'}
        url = reverse('currency-details', kwargs=data)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_convert(self):
        """
        Currencies conversions.
        """
        # convert USD to USD ;)
        data = {'amount': '1', 'from_currency': 'USD', 'to_currency': 'USD'}
        url = reverse('convert', kwargs=data)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)

        # convert RUB to EUR
        data = {'amount': '3', 'from_currency': 'RUB', 'to_currency': 'EUR'}
        url = reverse('convert', kwargs=data)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'],
                         self.convert_by_hand(data['amount'], data['from_currency'], data['to_currency']))

        # convert incorrect amount param
        data = {'amount': '1.2.3..', 'from_currency': 'RUB', 'to_currency': 'EUR'}
        url = reverse('convert', kwargs=data)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # convert incorrect from currency param
        data = {'amount': '1', 'from_currency': 'NOTFOUND', 'to_currency': 'EUR'}
        url = reverse('convert', kwargs=data)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # convert incorrect to currency param
        data = {'amount': '1', 'from_currency': 'USD', 'to_currency': 'NOTFOUND'}
        url = reverse('convert', kwargs=data)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
