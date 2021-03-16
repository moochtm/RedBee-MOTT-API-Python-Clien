
from .mgmt_asset import Asset
from .mgmt_tag import Tag
from .mgmt_product import Product, ProductOffering


class BusinessUnit:
    def __init__(self, business_unit, customer, request_maker):
        self.id = business_unit
        self._customer = customer
        self._request_maker = request_maker

    def languages(self):
        url = 'api/v1/customer/{0}/businessunit/{1}/definedvalues/languages'.format(self._customer, self.id)
        print(self._request_maker.get(url=url))

    def asset(self, id=None):
        return Asset(id=id, customer=self._customer, business_unit=self.id, request_maker=self._request_maker)

    def tag(self):
        return Tag(request_maker=self._request_maker, customer=self._customer, business_unit=self.id)

    def product(self):
        return Product(request_maker=self._request_maker, customer=self._customer, business_unit=self.id)

    def product_offering(self):
        return ProductOffering(request_maker=self._request_maker, customer=self._customer, business_unit=self.id)

