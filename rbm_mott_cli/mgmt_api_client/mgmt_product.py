import logging
import json


class Product:
    def __init__(self, request_maker, customer, business_unit=None):
        self._customer = customer
        self._business_unit = business_unit
        self._request_maker = request_maker

    def get_products(self):
        if self._business_unit is not None:
            url = 'v1/customer/{0}/businessunit/{1}/product/'
            url = url.format(self._customer, self._business_unit)
        else:
            raise NotImplementedError('API Client does not support getting products at customer unit level')
            # url = 'api/v1/customer/{0}/products/'
            # url = url.format(self._customer)

        response = json.loads(self._request_maker.get(url=url).text.encode('utf-8'))
        return response

    def find_product_by_name(self, name):
        products = self.get_products()
        results = []
        for product in products:
            if product['name'] == name:
                results.append(product)
        if len(results) == 0:
            logging.info('No products found with name={0}. Returning None'.format(name))
            return None
        if len(results) > 1:
            logging.info('Multiple products found with name={0}. Returning first found'.format(name))
        return results[0]


class ProductOffering:
    def __init__(self, request_maker, customer, business_unit=None):
        self._customer = customer
        self._business_unit = business_unit
        self._request_maker = request_maker

    def get_product_offerings(self):
        raise NotImplementedError
        if self._business_unit is not None:
            url = 'api/v1/customer/{0}/businessunit/{1}/productOfferings/'
            url = url.format(self._customer, self._business_unit)
        else:
            raise NotImplementedError('API Client does not support getting products at customer unit level')
            # url = 'api/v1/customer/{0}/productOfferings/'
            # url = url.format(self._customer)

        response = json.loads(self._request_maker.get(url=url).text.encode('utf-8'))
        return response

