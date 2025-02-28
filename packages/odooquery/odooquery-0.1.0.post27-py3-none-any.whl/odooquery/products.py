from typing import List
from .types import Product, ProductVariant, ProductStock, ProductTemplate

def fetch_products(self, domain: List, order: str) -> List[Product]:
    """Base function to fetch products matching given criteria."""
    fields = ['name', 'default_code', 'barcode', 'list_price', 'standard_price',
              'qty_available', 'virtual_available', 'product_tmpl_id', 'active']

    records = self.auto_paginated_search_read('product.product', domain, fields, order)

    return [{
        'id': product['id'],
        'name': product['name'],
        'default_code': product['default_code'],
        'barcode': product['barcode'],
        'list_price': product['list_price'],
        'standard_price': product['standard_price'],
        'qty_available': product['qty_available'],
        'virtual_available': product['virtual_available'],
        'product_tmpl_id': product['product_tmpl_id'][0] if isinstance(product['product_tmpl_id'], (list, tuple)) else product['product_tmpl_id'],
        'active': product['active']
    } for product in records]

def fetch_product_variants(self, domain: List, order: str) -> List[ProductVariant]:
    """Base function to fetch product variants matching given criteria."""
    fields = ['name', 'default_code', 'barcode', 'list_price', 'standard_price']

    records = self.auto_paginated_search_read('product.product', domain, fields, order)

    return [{
        'id': variant['id'],
        'name': variant['name'],
        'default_code': variant['default_code'],
        'barcode': variant['barcode'],
        'list_price': variant['list_price'],
        'standard_price': variant['standard_price']
    } for variant in records]

def fetch_product_templates(self, domain: List, order: str) -> List[ProductTemplate]:
    """Base function to fetch product templates matching given criteria."""
    fields = ['name', 'default_code', 'list_price', 'standard_price',
              'type', 'categ_id', 'product_variant_ids', 'active']

    records = self.auto_paginated_search_read('product.template', domain, fields, order)

    return [{
        'id': template['id'],
        'name': template['name'],
        'default_code': template['default_code'],
        'list_price': template['list_price'],
        'standard_price': template['standard_price'],
        'type': template['type'],
        'categ_id': template['categ_id'][0] if isinstance(template['categ_id'], (list, tuple)) else template['categ_id'],
        'product_variant_ids': template['product_variant_ids'],
        'active': template['active']
    } for template in records]

def fetch_product_templates_by_category(self, category_ids: List[int], order: str) -> List[ProductTemplate]:
    """Fetch product templates by category ids."""
    return self.fetch_product_templates([
        ('categ_id', 'in', category_ids)
    ], order)

def fetch_active_products(self, order: str) -> List[Product]:
    """Fetch all active products."""
    return self.fetch_products([('active', '=', True)], order)

def fetch_active_product_templates(self, order: str) -> List[ProductTemplate]:
    """Fetch all active product templates."""
    return self.fetch_product_templates([('active', '=', True)], order)

def fetch_stock_quants(self, domain: List, order: str) -> List[ProductStock]:
    """Base function to fetch stock quants matching given criteria."""
    fields = ['product_id', 'location_id', 'quantity', 'reserved_quantity']

    records = self.auto_paginated_read_group('stock.quant', domain, fields,
                                           ['product_id', 'location_id'])

    return [{
        'product_id': quant['product_id'][0] if isinstance(quant['product_id'], (list, tuple)) else quant['product_id'],
        'location_id': quant['location_id'][0] if isinstance(quant['location_id'], (list, tuple)) else quant['location_id'],
        'location_name': quant['location_id'][1] if isinstance(quant['location_id'], (list, tuple)) else '',
        'quantity': quant['quantity'],
        'reserved_quantity': quant['reserved_quantity'],
        'available_quantity': quant['quantity'] - quant['reserved_quantity']
    } for quant in records]

# By-field fetch functions for products
def fetch_products_by_code(self, codes: List[str], order: str) -> List[Product]:
    """Fetch products by default codes."""
    return self.fetch_products([('default_code', 'in', codes)], order)

def fetch_products_by_barcode(self, barcodes: List[str], order: str) -> List[Product]:
    """Fetch products by barcodes."""
    return self.fetch_products([('barcode', 'in', barcodes)], order)

def fetch_products_by_template(self, template_ids: List[int], order: str) -> List[Product]:
    """Fetch products by template ids."""
    return self.fetch_products([('product_tmpl_id', 'in', template_ids)], order)

# By-field fetch functions for product templates
def fetch_product_templates_by_category(self, category_ids: List[int], order: str) -> List[ProductTemplate]:
    """Fetch product templates by category ids."""
    return self.fetch_product_templates([('categ_id', 'in', category_ids)], order)

def fetch_product_templates_by_code(self, codes: List[str], order: str) -> List[ProductTemplate]:
    """Fetch product templates by default codes."""
    return self.fetch_product_templates([('default_code', 'in', codes)], order)

# By-field fetch functions for stock quants
def fetch_stock_quants_by_product(self, product_ids: List[int], order: str) -> List[ProductStock]:
    """Fetch stock quants for specific products."""
    return self.fetch_stock_quants([('product_id', 'in', product_ids)], order)

def fetch_stock_quants_by_location(self, location_ids: List[int], order: str) -> List[ProductStock]:
    """Fetch stock quants for specific locations."""
    return self.fetch_stock_quants([('location_id', 'in', location_ids)], order)

# By-field fetch functions for product variants
def fetch_product_variants_by_code(self, codes: List[str], order: str) -> List[ProductVariant]:
    """Fetch product variants by default codes."""
    return self.fetch_product_variants([('default_code', 'in', codes)], order)

def fetch_product_variants_by_barcode(self, barcodes: List[str], order: str) -> List[ProductVariant]:
    """Fetch product variants by barcodes."""
    return self.fetch_product_variants([('barcode', 'in', barcodes)], order)

def fetch_product_variants_by_template(self, template_ids: List[int], order: str) -> List[ProductVariant]:
    """Fetch product variants by template ids."""
    return self.fetch_product_variants([('product_tmpl_id', 'in', template_ids)], order)

