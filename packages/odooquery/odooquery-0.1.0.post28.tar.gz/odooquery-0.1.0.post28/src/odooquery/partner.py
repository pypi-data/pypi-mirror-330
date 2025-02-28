from typing import List
from .types import Partner

def fetch_partners(self, domain: List, order: str) -> List[Partner]:
    """Base function to fetch partners matching given criteria."""
    fields = ['name', 'email', 'phone', 'mobile', 'street', 'street2', 'city',
              'state_id', 'country_id', 'zip', 'customer_rank', 'supplier_rank']

    records = self.auto_paginated_search_read('res.partner', domain, fields, order)

    return [{
        'id': partner['id'],
        'name': partner['name'],
        'email': partner['email'],
        'phone': partner['phone'],
        'mobile': partner['mobile'],
        'street': partner['street'],
        'street2': partner['street2'],
        'city': partner['city'],
        'state_id': partner['state_id'][0] if isinstance(partner['state_id'], (list, tuple)) else partner['state_id'],
        'country_id': partner['country_id'][0] if isinstance(partner['country_id'], (list, tuple)) else partner['country_id'],
        'zip': partner['zip'],
        'customer_rank': partner['customer_rank'],
        'supplier_rank': partner['supplier_rank']
    } for partner in records]

def fetch_partners_by_email(self, emails: List[str], order: str) -> List[Partner]:
    """Fetch partners by email addresses."""
    return self.fetch_partners([
        ('email', 'in', emails)
    ], order)

def fetch_partners_by_name(self, names: List[str], order: str) -> List[Partner]:
    """Fetch partners by names."""
    return self.fetch_partners([
        ('name', 'in', names)
    ], order)

def fetch_customers_above_rank(self, min_rank: int, order: str) -> List[Partner]:
    """Fetch partners that are customers with minimum rank."""
    return self.fetch_partners([
        ('customer_rank', '>=', min_rank)
    ], order)

def fetch_suppliers_above_rank(self, min_rank: int, order: str) -> List[Partner]:
    """Fetch partners that are suppliers with minimum rank."""
    return self.fetch_partners([
        ('supplier_rank', '>=', min_rank)
    ], order)
