from . import messages
from typing import List, Dict, Any
from .types import Ticket
from .utils.text_processing import _strip_html
from datetime import datetime

def fetch_tickets(self, domain: List, order: str = None) -> List[Ticket]:
    """Fetch helpdesk tickets matching given domain."""
    fields = ['name', 'partner_id', 'partner_name', 'partner_email', 'description',
              'message_ids', 'stage_id', 'create_date']

    records = self.auto_paginated_search_read('helpdesk.ticket', domain, fields, order)

    return [{
        "id": ticket['id'],
        "subject": ticket['name'],
        "author_id": ticket['partner_id'][0] if isinstance(ticket['partner_id'], (list, tuple)) else ticket['partner_id'],
        "author_name": ticket['partner_name'],
        "author_email": ticket['partner_email'],
        "description": ticket['description'],
        "messages": sorted(
            [m for m in messages.fetch_messages_by_id(self, ticket['message_ids'])
             if m['body'] and m['body'].strip()],
            key=lambda x: x['date'],
            reverse=True
        ),
        "stage_id": ticket['stage_id'][0] if isinstance(ticket['stage_id'], (list, tuple)) else ticket['stage_id'],
        "stage_name": ticket['stage_id'][1] if isinstance(ticket['stage_id'], (list, tuple)) else '',
        "create_date": ticket['create_date']
    } for ticket in records]

def fetch_ticket_summaries(self, domain: List, order: str = None) -> List[Dict[str, Any]]:
    """Fetch basic ticket information for listings."""
    fields = ['name', 'partner_name', 'description', 'write_date', 'stage_id']

    records = self.auto_paginated_search_read('helpdesk.ticket', domain, fields, order)

    return [{
        "id": ticket['id'],
        "subject": ticket['name'],
        "author_name": ticket['partner_name'],
        "description": _strip_html(ticket['description']),
        "write_date": ticket['write_date'],
        "stage": ticket['stage_id'][1] if isinstance(ticket['stage_id'], (list, tuple)) else ''
    } for ticket in records]

def fetch_tickets_by_author_email(self, emails: List[str]) -> List[Ticket]:
    """Fetch helpdesk tickets by author emails."""
    return self.fetch_tickets([('partner_email', 'in', emails)])

def fetch_tickets_by_partner_id(self, partner_ids: List[int]) -> List[Ticket]:
    """Fetch helpdesk tickets by partner IDs."""
    return self.fetch_tickets([('partner_id', 'in', partner_ids)])

def fetch_tickets_updated_since(self, timestamp: int, limit: int = 50) -> List[Ticket]:
    """Fetch helpdesk tickets updated since the given timestamp."""
    update_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return self.fetch_tickets(
        [('write_date', '>=', update_date)],
        order='write_date DESC'
    )

def fetch_ticket_summaries_by_author_email(self, emails: List[str]) -> List[Dict[str, Any]]:
    """Fetch basic ticket information by author emails."""
    return self.fetch_ticket_summaries([('partner_email', 'in', emails)])

def fetch_ticket_summaries_by_partner_id(self, partner_ids: List[int]) -> List[Dict[str, Any]]:
    """Fetch basic ticket information for display in listings by partner IDs. Does not include messages or most user info."""
    return self.fetch_ticket_summaries([('partner_id', 'in', partner_ids)])

def fetch_ticket_summaries_updated_since(self, timestamp: int, limit: int) -> List[Dict[str, Any]]:
    """Fetch basic ticket information for display in listings updated since the given timestamp. Does not include messages or most user info."""
    update_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return self.fetch_ticket_summaries(
        [('write_date', '>=', update_date)],
        order='write_date DESC'
    )