from rest_framework import generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from .models import Currency, Rate
import decimal
import time


class CurrencyConvert(APIView):
    def get(self, request, from_currency, to_currency, amount):
        try:
            amount_decimal = decimal.Decimal(amount);
        except decimal.InvalidOperation:
            raise ParseError(detail='Invalid "amount" parameter!')

        try:
            from_rate = Rate.objects.get(currency__name=from_currency, obsolete=False).value
        except Rate.DoesNotExist:
            raise NotFound(detail='There is no such currency "{}"'.format(from_currency))

        try:
            to_rate = Rate.objects.get(currency__name=to_currency, obsolete=False).value
        except Rate.DoesNotExist:
            raise NotFound(detail='There is no such currency "{}"'.format(to_currency))

        result = amount_decimal / from_rate * to_rate;
        rate = to_rate / from_rate

        return Response({'amount': amount,
                         'from': from_currency,
                         'to': to_currency,
                         'timestamp': int(time.time()),
                         'rate': rate.quantize(decimal.Decimal('0.0001'), rounding=decimal.ROUND_HALF_UP),
                         'result': result.quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_UP),
                         'raw_result': result})

class CurrencyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ( 'name', 'description' )

class CurrencyList(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencyListSerializer

class CurrencyDetailsSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()

    def get_rate(self, obj):
        return obj.rates.filter(obsolete=False)[0].value

    class Meta:
        model = Currency
        fields = ('name', 'description', 'rate', )

class CurrencyDetails(generics.RetrieveAPIView):
    queryset = Currency.objects.all()
    lookup_field = 'name'
    serializer_class = CurrencyDetailsSerializer

class APINotFound(APIView):
    def get(self, request):
        return Response({
            'error': True,
            'status': 404,
            'description': 'Requested API not found, please check and try again.'
        })

