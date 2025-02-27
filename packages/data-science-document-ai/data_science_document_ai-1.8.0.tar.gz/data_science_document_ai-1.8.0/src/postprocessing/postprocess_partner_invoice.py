"""This module contains the postprocessing functions for the partner invoice."""
from src.postprocessing.common import extract_string


def postprocessing_partner_invoice(partner_invoice):
    """Apply postprocessing to the partner invoice data."""
    # flatten the invoice amount
    for amount in partner_invoice.get("invoiceAmount", {}):
        if isinstance(amount, list):
            amount = amount[0]
        if isinstance(amount, dict):
            for amount_key, val in amount.items():
                partner_invoice[f"invoiceAmount_{amount_key}"] = val
            break
    # remove invoiceAmount -comes from doc ai-
    partner_invoice.pop("invoiceAmount")
    # remove containers -comes from doc ai-
    partner_invoice.pop("containers")

    key_updates = {
        'pod': 'portOfDischarge',
        'pol': 'portOfLoading',
        'containerSize': 'containerType',
        'invoiceAmount_currencyCode': 'currencyCode',
        'invoiceAmount_grandTotal': 'grandTotal',
        'invoiceAmount_vatAmount': 'vatAmount',
        'invoiceAmount_vatApplicableAmount': 'totalAmountGross',
        'invoiceAmount_vatPercentage': 'vatPercentage',
        'name': 'lineItemDescription',
        'unit': 'quantity'
        }

    def update_keys(d, key_updates):
        """
        Recursively updates keys in a dictionary according to a mapping provided in key_updates.
        
        d: The original dictionary
        key_updates: A dictionary mapping old key names to new key names
        
        return A new dictionary with updated key names
        """
        if isinstance(d, dict):
            return {key_updates.get(k, k): update_keys(v, key_updates) for k, v in d.items()}
        elif isinstance(d, list):
            return [update_keys(item, key_updates) for item in d]
        else:
            return d

    updated_data = update_keys(partner_invoice, key_updates)

    return updated_data
