from typing import List
from datetime import datetime
from .types import MailingStatistic, MailingContact, MassMailing

def search_mass_mailing_list_ids_by_name(self, names: List[str]) -> List[int]:
    """Search for mass mailing lists by names."""
    return self.connection.env['mailing.list'].search([
        ('name', 'ilike', names)
    ])

def fetch_mass_mailing_lists_by_id(self, list_ids: List[int]) -> List[str]:
    """Fetch mass mailing list details by IDs."""
    return self.connection.env['mailing.list'].read(
        list_ids,
        ['name', 'contact_ids','active', 'mailing_count', 'mailing_ids']
    )

def search_mass_mailing_ids_by_subject(self, subjects: List[str]) -> List[int]:
    """Search for mass mailings by subjects."""
    return self.connection.env['mailing.mailing'].search([
        ('subject', 'ilike', subjects)
    ])

def search_mass_mailing_ids_by_date_range(self, start_timestamp: int, end_timestamp: int) -> List[int]:
    """Search for mass mailings within a date range using Unix timestamps."""
    start_date = datetime.fromtimestamp(start_timestamp)
    end_date = datetime.fromtimestamp(end_timestamp)

    return self.connection.env['mailing.mailing'].search([
        ('sent_date', '>=', start_date.strftime('%Y-%m-%d %H:%M:%S')),
        ('sent_date', '<=', end_date.strftime('%Y-%m-%d %H:%M:%S'))
    ])

def fetch_mass_mailings_by_id(self, mailing_ids: List[int]) -> List[MassMailing]:
    """Fetch mass mailing details by IDs."""
    return self.connection.env['mailing.mailing'].read(
        mailing_ids,
        ['name', 'subject', 'sent_date', 'state', 'mailing_type', 'contact_list_ids', 'total', 'sent', 'opened', 'clicked', 'replied', 'bounced', 'failed']
    )

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

def search_mass_mailing_statistics_ids_by_mailing_id_and_date_range(self, mailing_ids: List[int], start_timestamp: int, end_timestamp: int) -> List[MailingStatistic]:
    """Search mass mailing statistics for specific mass mailings within a date range using Unix timestamps."""
    start_date = datetime.fromtimestamp(start_timestamp)
    end_date = datetime.fromtimestamp(end_timestamp)

    return self.connection.env['mailing.trace'].search([
        ('mass_mailing_id', 'in', mailing_ids),
        ('sent', '>=', start_date.strftime('%Y-%m-%d %H:%M:%S')),
        ('sent', '<=', end_date.strftime('%Y-%m-%d %H:%M:%S'))
    ])

def fetch_mass_mailing_statistics_by_id(self, stat_ids: List[int]) -> List[MailingStatistic]:
    """Fetch mass mailing statistics by IDs."""
    return self.connection.env['mailing.trace'].read(
        stat_ids,
        ['mass_mailing_id', 'model', 'res_id', 'email', 'trace_status', 'sent_datetime', 'open_datetime', 'reply_datetime', 'failure_type']
    )

def search_contact_ids_by_email(self, emails: List[str]) -> List[int]:
    """Search for mailing list contacts by emails."""
    return self.connection.env['mailing.contact'].search([
        ('email', 'in', emails)
    ])

def search_contact_ids_by_mailing_id(self, mailing_ids: List[int]) -> List[int]:
    """Search for mailing list contacts that exist in ALL of the specified mass mailings."""
    domain = ['&'] * (len(mailing_ids) - 1)  # Create n-1 AND operators
    for mailing_id in mailing_ids:
        domain.extend([('list_ids', 'in', [mailing_id])])
    return self.connection.env['mailing.contact'].search(domain)

def fetch_contacts_by_id(self, contact_ids: List[int]) -> List[MailingContact]:
    """Fetch mailing list contact details."""
    return self.connection.env['mailing.contact'].read(
        contact_ids,
        ['name', 'company_name', 'email', 'list_ids', 'subscription_ids']
    )


# Aggregate functions provide higher level functionality by combining multiple lower level functions
def fetch_mass_mailing_lists_by_name(self, names: List[str]) -> List[str]:
    """Fetch mass mailing lists by names."""
    return fetch_mass_mailing_lists_by_id(self, search_mass_mailing_list_ids_by_name(self, names))

def fetch_mass_mailings_by_subject(self, subjects: List[str]) -> List[MassMailing]:
    """Fetch mass mailings by subjects."""
    return fetch_mass_mailings_by_id(self, search_mass_mailing_ids_by_subject(self, subjects))

def fetch_mass_mailings_by_date_range(self, start_timestamp: int, end_timestamp: int) -> List[MassMailing]:
    """Fetch mass mailings within a date range using Unix timestamps."""
    return fetch_mass_mailings_by_id(self,
        search_mass_mailing_ids_by_date_range(self, start_timestamp, end_timestamp)
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

def fetch_mass_mailing_statistics_by_mailing_id_and_date_range(self, mailing_ids: List[int], start_timestamp: int, end_timestamp: int) -> List[MailingStatistic]:
    """Fetch mass mailing statistics for specific mass mailings within a date range using Unix timestamps."""
    return fetch_mass_mailing_statistics_by_id(self,
        search_mass_mailing_statistics_ids_by_mailing_id_and_date_range(self, mailing_ids, start_timestamp, end_timestamp)
    )

def fetch_contacts_by_email(self, emails: List[str]) -> List[MailingContact]:
    """Fetch mailing list contacts by emails."""
    return fetch_contacts_by_id(self, search_contact_ids_by_email(self, emails))

def fetch_contacts_by_mailing_id(self, mailing_ids: List[int]) -> List[MailingContact]:
    """Fetch mailing list contacts for specific mass mailings."""
    return fetch_contacts_by_id(self, search_contact_ids_by_mailing_id(self, mailing_ids))
