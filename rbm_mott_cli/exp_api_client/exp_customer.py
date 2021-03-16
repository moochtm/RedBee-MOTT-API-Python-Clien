
from .exp_business_unit import BusinessUnit


class Customer:
    def __init__(self, customer_id, request_maker):
        self.id = customer_id
        self._request_maker = request_maker

    # CALLS

    # OBJECTS

    def business_unit(self, business_unit):
        return BusinessUnit(business_unit, self.id, self._request_maker)


