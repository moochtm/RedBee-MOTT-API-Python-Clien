
from .mgmt_asset import Asset
from .mgmt_business_unit import BusinessUnit
from .mgmt_tag import Tag
from .mgmt_product import Product, ProductOffering

class Customer:
    def __init__(self, customer_id, request_maker):
        self.id = customer_id
        self._request_maker = request_maker

    # CALLS

    def get_features(self):
        url = 'api/v1/customer/{0}/features'.format(self.id)
        print(self._request_maker.get(url=url))

    # OBJECTS

    def business_unit(self, business_unit):
        return BusinessUnit(business_unit, self.id, self._request_maker)

    def tag(self):
        return Tag(request_maker=self._request_maker, customer=self.id)

    def product(self):
        return Product(request_maker=self._request_maker, customer=self.id)

    def product_offering(self):
        return ProductOffering(request_maker=self._request_maker, customer=self.id)

    def asset(self):
        return Asset(request_maker=self._request_maker, customer=self.id)
