from . import partner, messages
from typing import List, Literal
from .types import Order, OrderLine, Transfer, TransferLine
from datetime import datetime

# Define valid order states
OrderState = Literal['draft', 'sent', 'sale', 'done', 'cancel']

def fetch_orders(self, domain: List, order: str) -> List[Order]:
    """Base function to fetch orders matching given criteria."""
    fields = ['name', 'partner_id', 'date_order', 'state', 'amount_total',
              'order_line', 'invoice_status', 'message_ids', 'picking_ids']

    records = self.auto_paginated_search_read('sale.order', domain, fields, order)

    return [{
        'id': order['id'],
        'name': order['name'],
        'order_line': order['order_line'],
        'state': order['state'],
        'date_order': order['date_order'],
        'partner_id': order['partner_id'][0] if isinstance(order['partner_id'], (list, tuple)) else order['partner_id'],
        'partner_name': order['partner_id'][1] if isinstance(order['partner_id'], (list, tuple)) else '',
        'amount_total': order['amount_total'],
        'invoice_status': order['invoice_status'],
        'picking_ids': order['picking_ids'],
        'message_ids': order['message_ids']
    } for order in records]

def fetch_order_lines(self, domain: List, order: str) -> List[OrderLine]:
    """Base function to fetch order lines matching given criteria."""
    fields = ['order_id', 'product_id', 'product_uom_qty', 'price_unit',
              'price_subtotal', 'state', 'qty_delivered', 'qty_invoiced']

    records = self.auto_paginated_search_read('sale.order.line', domain, fields, order)

    return [{
        'id': line['id'],
        'order_id': line['order_id'][0] if isinstance(line['order_id'], (list, tuple)) else line['order_id'],
        'product_id': line['product_id'][0] if isinstance(line['product_id'], (list, tuple)) else line['product_id'],
        'product_uom_qty': line['product_uom_qty'],
        'price_unit': line['price_unit'],
        'price_subtotal': line['price_subtotal'],
        'state': line['state'],
        'qty_delivered': line['qty_delivered'],
        'qty_invoiced': line['qty_invoiced']
    } for line in records]

def fetch_transfers(self, domain: List, order: str) -> List[Transfer]:
    """Base function to fetch transfers matching given criteria."""
    fields = ['name', 'state', 'date_done', 'location_id', 'location_dest_id',
              'move_line_ids_without_package', 'message_ids']

    records = self.auto_paginated_search_read('stock.picking', domain, fields, order)

    return [{
        'id': transfer['id'],
        'name': transfer['name'],
        'state': transfer['state'],
        'date_done': transfer['date_done'],
        'location_id': transfer['location_id'][0] if isinstance(transfer['location_id'], (list, tuple)) else transfer['location_id'],
        'location_name': transfer['location_id'][1] if isinstance(transfer['location_id'], (list, tuple)) else '',
        'location_dest_id': transfer['location_dest_id'][0] if isinstance(transfer['location_dest_id'], (list, tuple)) else transfer['location_dest_id'],
        'location_dest_name': transfer['location_dest_id'][1] if isinstance(transfer['location_dest_id'], (list, tuple)) else '',
        'move_lines': transfer['move_line_ids_without_package'],
        'message_ids': transfer['message_ids']
    } for transfer in records]

def fetch_transfer_lines(self, domain: List, order: str) -> List[TransferLine]:
    """Base function to fetch transfer lines matching given criteria."""
    fields = ['product_id', 'product_reference_code', 'qty_done', 'quantity_product_uom']

    records = self.auto_paginated_search_read('stock.move.line', domain, fields, order)

    return [{
        'id': line['id'],
        'product_id': line['product_id'][0] if isinstance(line['product_id'], (list, tuple)) else line['product_id'],
        'product_name': line['product_id'][1] if isinstance(line['product_id'], (list, tuple)) else '',
        'reference_code': line['product_reference_code'],
        'quantity': line['quantity_product_uom'],
        'quantity_done': line['qty_done']
    } for line in records]

# By-field fetch functions for orders
def fetch_orders_by_partner(self, partner_ids: List[int], order: str) -> List[Order]:
    """Fetch orders for specific partners."""
    return self.fetch_orders([('partner_id', 'in', partner_ids)], order)

def fetch_orders_by_state(self, state: OrderState, order: str) -> List[Order]:
    """Fetch orders in specific state."""
    return self.fetch_orders([('state', '=', state)], order)

def fetch_orders_by_date_range(self, start_timestamp: int, end_timestamp: int, order: str) -> List[Order]:
    """Fetch orders within a date range using Unix timestamps."""
    start_date = datetime.fromtimestamp(start_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    end_date = datetime.fromtimestamp(end_timestamp).strftime('%Y-%m-%d %H:%M:%S')

    return self.fetch_orders([
        ('date_order', '>=', start_date),
        ('date_order', '<=', end_date)
    ], order)

# By-field fetch functions for order lines
def fetch_order_lines_by_order(self, order_ids: List[int], order: str) -> List[OrderLine]:
    """Fetch order lines for specific orders."""
    return self.fetch_order_lines([('order_id', 'in', order_ids)], order)

def fetch_order_lines_by_product(self, product_ids: List[int], order: str) -> List[OrderLine]:
    """Fetch order lines for specific products."""
    return self.fetch_order_lines([('product_id', 'in', product_ids)], order)

# By-field fetch functions for transfers
def fetch_transfers_by_order(self, order_ids: List[int], order: str) -> List[Transfer]:
    """Fetch transfers for specific orders."""
    return self.fetch_transfers([('sale_id', 'in', order_ids)], order)

def fetch_transfers_by_state(self, state: str, order: str) -> List[Transfer]:
    """Fetch transfers in specific state."""
    return self.fetch_transfers([('state', '=', state)], order)

# By-field fetch functions for transfer lines
def fetch_transfer_lines_by_transfer(self, transfer_ids: List[int], order: str) -> List[TransferLine]:
    """Fetch transfer lines for specific transfers."""
    return self.fetch_transfer_lines([('picking_id', 'in', transfer_ids)], order)

def fetch_transfer_lines_by_product(self, product_ids: List[int], order: str) -> List[TransferLine]:
    """Fetch transfer lines for specific products."""
    return self.fetch_transfer_lines([('product_id', 'in', product_ids)], order)
