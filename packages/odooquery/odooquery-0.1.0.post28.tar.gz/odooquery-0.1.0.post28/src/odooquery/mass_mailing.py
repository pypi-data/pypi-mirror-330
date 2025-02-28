from typing import List
from datetime import datetime
from .types import MailingStatistic, MailingContact, MassMailing
from .utils.query import auto_paginated_search_read

def fetch_mailings(self, domain: List, order: str = None) -> List[MassMailing]:
    """Base function to fetch mass mailings matching given criteria."""
    fields = ['name', 'subject', 'sent_date', 'state', 'mailing_type',
              'contact_list_ids', 'total', 'sent', 'opened', 'clicked',
              'replied', 'bounced', 'failed']

    records = auto_paginated_search_read(self, 'mailing.mailing', domain, fields, order)

    return [{
        'id': mailing['id'],
        'name': mailing['name'],
        'subject': mailing['subject'],
        'sent_date': mailing['sent_date'],
        'state': mailing['state'],
        'mailing_type': mailing['mailing_type'],
        'contact_list_ids': mailing['contact_list_ids'],
        'total': mailing['total'],
        'sent': mailing['sent'],
        'opened': mailing['opened'],
        'clicked': mailing['clicked'],
        'replied': mailing['replied'],
        'bounced': mailing['bounced'],
        'failed': mailing['failed'],
    } for mailing in records]

def fetch_mailings_by_subject(self, subjects: List[str], order: str = None) -> List[MassMailing]:
    """Fetch mass mailings by subjects."""
    return self.fetch_mailings([('subject', 'ilike', subjects)], order)

def fetch_mailings_by_date_range(self, start_timestamp: int, end_timestamp: int,
                               order: str = None) -> List[MassMailing]:
    """Fetch mass mailings within a date range using Unix timestamps."""
    start_date = datetime.fromtimestamp(start_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    end_date = datetime.fromtimestamp(end_timestamp).strftime('%Y-%m-%d %H:%M:%S')

    return self.fetch_mailings([
        ('sent_date', '>=', start_date),
        ('sent_date', '<=', end_date)
    ], order)

def fetch_mailing_statistics(self, domain: List, order: str = None) -> List[MailingStatistic]:
    """Base function to fetch mailing statistics matching given criteria."""
    fields = ['mass_mailing_id', 'model', 'res_id', 'email', 'trace_status',
              'sent_datetime', 'open_datetime', 'reply_datetime', 'failure_type']

    records = auto_paginated_search_read(self, 'mailing.trace', domain, fields, order)

    return [{
        'id': stat['id'],
        'mass_mailing_id': stat['mass_mailing_id'][0] if isinstance(stat['mass_mailing_id'], (list, tuple)) else stat['mass_mailing_id'],
        'model': stat['model'],
        'res_id': stat['res_id'],
        'email': stat['email'],
        'trace_status': stat['trace_status'],
        'failure_type': stat['failure_type'],
        'sent_datetime': stat['sent_datetime'],
        'open_datetime': stat['open_datetime'],
        'reply_datetime': stat['reply_datetime'],
    } for stat in records]

def fetch_mailing_statistics_by_email(self, emails: List[str], order: str = None) -> List[MailingStatistic]:
    """Fetch mass mailing statistics for specific emails."""
    return self.fetch_mailing_statistics([('email', 'in', emails)], order)

def fetch_mailing_statistics_by_date_range(self, start_timestamp: int, end_timestamp: int,
                                         order: str = None) -> List[MailingStatistic]:
    """Fetch mass mailing statistics within a date range using Unix timestamps."""
    start_date = datetime.fromtimestamp(start_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    end_date = datetime.fromtimestamp(end_timestamp).strftime('%Y-%m-%d %H:%M:%S')

    return self.fetch_mailing_statistics([
        ('sent_datetime', '>=', start_date),
        ('sent_datetime', '<=', end_date)
    ], order)

def fetch_contacts(self, domain: List, order: str = None) -> List[MailingContact]:
    """Fetch mailing list contacts matching the given domain."""
    fields = ['name', 'company_name', 'email', 'list_ids', 'subscription_ids']

    records = auto_paginated_search_read(self, 'mailing.contact', domain, fields, order)

    return [{
        'id': contact['id'],
        'name': contact['name'],
        'company_name': contact['company_name'],
        'email': contact['email'],
        'list_ids': contact['list_ids'],
        'subscription_ids': contact['subscription_ids'],
    } for contact in records]

def fetch_contacts_by_email(self, emails: List[str], order: str = None) -> List[MailingContact]:
    """Fetch mailing list contacts by emails."""
    return self.fetch_contacts([('email', 'in', emails)], order)
