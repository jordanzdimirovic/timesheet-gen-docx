from tsdef import *
from .interaction import *
from enum import Enum


def menu_main() -> None:
    """Show main menu"""
    selected = generic_select("What would you like to do?", [
        (1, "Create New Invoice"),
        (2, "Create Invoice From Timesheet(s)"),
        (3, "Create Timesheet"),
        (4, "Render Invoices"),
        (5, "Render Timesheets")
        
    ])
    
    if selected == 1:
        # Get invoice
        invoice = menu_invoice()
        

def menu_invoice_party(party_name: str) -> InvoiceParty:
    """Show menu to create an invoice party"""
    hprint(f"Create party [{party_name}]")
    return InvoiceParty(
        generic_get("Name"),
        generic_get("Address"),
        generic_get("Business number (e.g. ABN)")
    )
    

def menu_invoice_lines() -> list[InvoiceLine]:
    result: list[InvoiceLine] = []
    hprint("Invoice lines (Ctrl+C to stop)")
    try:
        result.append(InvoiceLine(
            generic_get("Quantity", default=1, typecast=int, do_strip=True),
            generic_get("Description"),
            generic_get("Price (each)", typecast=float, do_strip=True)
        ))        
        
    except KeyboardInterrupt:
        pprint("Finished getting invoice lines...")
        pass


def menu_invoice() -> Invoice:
    """Show menu for invoice"""
    return Invoice(
        generic_get("Invoice number"),
        generic_get("Issue date"),
        generic_get("Due date"),
        menu_invoice_party("Bill To"),
        menu_invoice_party("Bill From"),
        menu_invoice_lines()
    )
    

def menu_invoice_from_timesheets(timesheets: list[Timesheet]) -> Invoice:
    return Invoice(
        generic_get("Invoice number"),
        max(d for d in map(lambda entry: entry.))
    )


def menu_timesheet() -> Timesheet:
    """Show menu for timesheet"""
    
    
def menu_timesheet_entry() -> TimesheetEntry:
    """Show menu for timesheet entry"""
    return TimesheetEntry (
        
    )
    
