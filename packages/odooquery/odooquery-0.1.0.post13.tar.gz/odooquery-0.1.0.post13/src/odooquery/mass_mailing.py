from typing import List
from datetime import datetime
from .types import MailingStatistic, MailingContact, MassMailing

def search_mailing_ids_by_subject(self, subjects: List[str]) -> List[int]:
    """Search for mass mailings by subjects."""
    return self.connection.env['mail.mass_mailing'].search([
        ('subject', 'ilike', subjects)
    ])

def search_mailing_ids_by_date_range(self, start_timestamp: int, end_timestamp: int) -> List[int]:
    """Search for mass mailings within a date range using Unix timestamps."""
    start_date = datetime.fromtimestamp(start_timestamp)
    end_date = datetime.fromtimestamp(end_timestamp)

    return self.connection.env['mail.mass_mailing'].search([
        ('sent_date', '>=', start_date.strftime('%Y-%m-%d %H:%M:%S')),
        ('sent_date', '<=', end_date.strftime('%Y-%m-%d %H:%M:%S'))
    ])

def fetch_mailings_by_id(self, mailing_ids: List[int]) -> List[MassMailing]:
    """Fetch mass mailing details by IDs."""
    return [{
        'id': mailing['id'],
        'name': mailing['name'],
        'subject': mailing['subject'],
        'sent_date': mailing['sent_date'],
        'state': mailing['state'],
        'mailing_model': mailing['mailing_model'],
        'statistics_ids': mailing['statistics_ids'],
        'contact_list_ids': mailing['contact_list_ids']
    } for mailing in self.connection.env['mail.mass_mailing'].read(
        mailing_ids,
        ['name', 'subject', 'sent_date', 'state', 'mailing_model', 'statistics_ids', 'contact_list_ids']
    )]

def search_mass_mailing_statistics_ids_by_mailing_id(self, mailing_ids: List[int]) -> List[MailingStatistic]:
    """Search statistics for specific mass mailings."""
    return self.connection.env['mailing.trace'].search([
        ('mass_mailing_id', 'in', mailing_ids)
    ])

def search_mass_mailing_statistics_ids_by_email(self, emails: List[str]) -> List[MailingStatistic]:
    """Search mass mailing statistics for specific emails."""
    return self.connection.env['mailing.trace'].search([
        ('email', 'in', emails)
    ])

def search_mass_mailing_statistics_ids_by_date_range(self, start_timestamp: int, end_timestamp: int) -> List[MailingStatistic]:
    """Search mass mailing statistics within a date range using Unix timestamps."""
    start_date = datetime.fromtimestamp(start_timestamp)
    end_date = datetime.fromtimestamp(end_timestamp)

    return self.connection.env['mailing.trace'].search([
        ('sent', '>=', start_date.strftime('%Y-%m-%d %H:%M:%S')),
        ('sent', '<=', end_date.strftime('%Y-%m-%d %H:%M:%S'))
    ])

def fetch_mass_mailing_statistics_by_id(self, stat_ids: List[int]) -> List[MailingStatistic]:
    """Fetch mass mailing statistics by IDs."""
    return [{
        'id': stat['id'],
        'mass_mailing_id': stat['mass_mailing_id'][0] if isinstance(stat['mass_mailing_id'], (list, tuple)) else stat['mass_mailing_id'],
        'model': stat['model'],
        'res_id': stat['res_id'],
        'email': stat['email'],
        'sent_datetime': stat['sent_datetime'],
        'open_datetime': stat['open_datetime'],
        'click_datetime': stat['click_datetime'],
        'bounce_datetime': stat['bounce_datetime'],
        'exception': stat['exception']
    } for stat in self.connection.env['mailing.trace'].read(
        stat_ids,
        ['mass_mailing_id', 'model', 'res_id', 'email', 'sent_datetime', 'open_datetime', 'click_datetime', 'bounce_datetime', 'exception']
    )]

def search_contact_ids_by_email(self, emails: List[str]) -> List[int]:
    """Search for mailing list contacts by emails."""
    return self.connection.env['mail.mass_mailing.contact'].search([
        ('email', 'in', emails)
    ])

def search_contact_ids_by_mailing_id(self, mailing_ids: List[int]) -> List[int]:
    """Search for mailing list contacts for specific mass mailings."""
    return self.connection.env['mail.mass_mailing.contact'].search([
        ('mass_mailing_id', 'in', mailing_ids)
    ])

def fetch_contacts_by_id(self, contact_ids: List[int]) -> List[MailingContact]:
    """Fetch mailing list contact details."""
    return [{
        'id': contact['id'],
        'name': contact['name'],
        'email': contact['email'],
        'list_ids': contact['list_ids'],
        'unsubscribed': contact['unsubscribed'],
        'opt_out': contact['opt_out']
    } for contact in self.connection.env['mail.mass_mailing.contact'].read(
        contact_ids,
        ['name', 'email', 'list_ids', 'unsubscribed', 'opt_out']
    )]


# Aggregate functions provide higher level functionality by combining multiple lower level functions
def fetch_mailings_by_subject(self, subjects: List[str]) -> List[MassMailing]:
    """Fetch mass mailings by subjects."""
    return fetch_mailings_by_id(self, search_mailing_ids_by_subject(self, subjects))

def fetch_mailings_by_date_range(self, start_timestamp: int, end_timestamp: int) -> List[MassMailing]:
    """Fetch mass mailings within a date range using Unix timestamps."""
    return fetch_mailings_by_id(self,
        search_mailing_ids_by_date_range(self, start_timestamp, end_timestamp)
    )

def fetch_mass_mailing_statistics_by_mailing_id(self, mailing_ids: List[int]) -> List[MailingStatistic]:
    """Fetch mass mailing statistics for specific mass mailings."""
    return fetch_mass_mailing_statistics_by_id(self, search_mass_mailing_statistics_ids_by_mailing_id(self, mailing_ids))

def fetch_mass_mailing_statistics_by_email(self, emails: List[str]) -> List[MailingStatistic]:
    """Fetch mass mailing statistics for specific emails."""
    return fetch_mass_mailing_statistics_by_id(self, search_mass_mailing_statistics_ids_by_email(self, emails))

def fetch_mass_mailing_statistics_by_date_range(self, start_timestamp: int, end_timestamp: int) -> List[MailingStatistic]:
    """Fetch mass mailing statistics within a date range using Unix timestamps."""
    return fetch_mass_mailing_statistics_by_id(self,
        search_mass_mailing_statistics_ids_by_date_range(self, start_timestamp, end_timestamp)
    )

def fetch_contacts_by_email(self, emails: List[str]) -> List[MailingContact]:
    """Fetch mailing list contacts by emails."""
    return fetch_contacts_by_id(self, search_contact_ids_by_email(self, emails))

def fetch_contacts_by_mailing_id(self, mailing_ids: List[int]) -> List[MailingContact]:
    """Fetch mailing list contacts for specific mass mailings."""
    return fetch_contacts_by_id(self, search_contact_ids_by_mailing_id(self, mailing_ids))
