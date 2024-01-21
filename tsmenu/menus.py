import os
from tsdef import *
from .interaction import *
from enum import Enum

from tsdocx import render_all

from datetime import timedelta

import jsonpickle as jp

from tsconfig import TSConfig

std_datefmt_mappings = {
    "today": lambda: Date.today(),
    "yesterday": lambda: Date.today() - timedelta(1)
}

def std_datefmt(s: str) -> Date:
    s = s.lower()

    if s in std_datefmt_mappings: return std_datefmt_mappings[s]()
    elif "+" in s: return Date.today() + timedelta(int(s.replace("+", '').strip()))
    elif "-" in s: return Date.today() - timedelta(int(s.replace("-", '').strip()))
    
    return Date(*reversed(list(map(lambda part: int(part.strip()), s.split('/')))))

def menu_main(collection: Collection) -> None:
    """Show main menu"""
    

    selected = generic_select("What would you like to do?", [
        (1, "Create New Invoice"),
        (2, "Create Invoice From Timesheet(s)"),
        (3, "Create Timesheet"),
        (4, "Create Timesheet From CSV"),
        (5, "Render")
    ])
    
    to_write = None

    match selected:
        case 1:
            to_write = menu_invoice()

        case 2:
            to_write = menu_invoice_from_timesheets(collection)

        case 3:
            to_write = menu_timesheet()

        case 4:
            to_write = menu_timesheet_csv()

        case 5:
            menu_render(collection)

        case _:
            print("Invalid menu option...")
            return
        
    if to_write:
        type_name = type(to_write).__name__.lower()
        collection.store(to_write, generic_get(f"Name for new '{type_name}'"))
            
            
def menu_timesheet_csv() -> Timesheet:
    # Get path to the csv file
    csv_path: str = generic_get("CSV timesheet entries path")
    
    if not os.path.isfile(csv_path):
        print(f"CSV file {csv_path} doesn't exist..! Try again...")
        return menu_timesheet_csv()
    
    # Read the CSV file
    with open(csv_path, "r") as f:
        lines = [l.removesuffix('\n').split(',') for l in f.readlines()]
        
    if not all(len(l) == 3 for l in lines):
        print("CSV needs 3 per line!")
        return
    
    # Convert each to a timesheet entry
    try:
        entries = [
            TimesheetEntry(
                std_datefmt(l[0]),
                float(l[1]),
                str(l[2])
            ) for l in lines
        ]
        
    except ValueError:
        print("At least one line in the CSV was an invalid timesheet entry!\nEach entry needs 3 values:\n -> date (dd/mm/yy)\n -> hours (float)\n -> description (str)")
        return
    
    # Return a timesheet
    return Timesheet(
        TSConfig.get("contractor:name"),
        generic_get("Timesheet title (i.e., project)", default="Project"),
        TSConfig.get("hourly_rate"),
        entries
    )


def menu_render(collection: Collection) -> None:
    no_items_rendered = render_all(
        collection,
        TSConfig.get("templates:timesheet"),
        TSConfig.get("templates:invoice"),
        generic_get("Render output path (relative to collection)", "rendered")
    )

    print(f"{no_items_rendered} items successfully rendered!")

def menu_collection() -> Collection:
    dirname = generic_get("Collection directory")
    os.makedirs(dirname, exist_ok=True)
    return Collection(dirname)


def menu_invoice_party(party_type: PartyType) -> InvoiceParty:
    """Show menu to create an invoice party"""
    hprint(f"Create party [{party_type.value}]")
    if party_type == PartyType.From:
        print("Filling from config: 'contractor'")
        return InvoiceParty(
            TSConfig.get("contractor:name", lambda: generic_get("Name")),
            TSConfig.get("contractor:address", lambda: generic_get("Address")),
            TSConfig.get("contractor:business_number", lambda: generic_get("Business number (e.g. ABN)"))
        )
    
    else:
        return InvoiceParty(
            generic_get("Name"),
            generic_get("Address"),
            generic_get("Business number (e.g. ABN)")
        )
    

def menu_invoice_lines() -> list[InvoiceLine]:
    result: list[InvoiceLine] = []
    hprint("Invoice lines (Ctrl+C to stop)")
    while True:
        try:
            result.append(InvoiceLine(
                generic_get("Quantity", default=1, typecast=int, do_strip=True),
                generic_get("Description"),
                generic_get("Price (each)", typecast=float, do_strip=True)
            ))        
            
        except KeyboardInterrupt:
            pprint("Finished getting invoice lines...")
            break


def menu_invoice() -> Invoice:
    """Show menu for invoice"""
    return Invoice(
        generic_get("Invoice number"),
        generic_get("Issue date", typecast=std_datefmt),
        generic_get("Due date", typecast=std_datefmt),
        menu_invoice_party(PartyType.From),
        menu_invoice_party(PartyType.To),
        Payment(
            TSConfig.get("payment:bsb"),
            TSConfig.get("payment:account")
        ),
        menu_invoice_lines()
    )
    

def menu_invoice_from_timesheets(collection: Collection) -> Invoice:
    timesheets = collection.timesheets
    return Invoice(
        generic_get("Invoice number"),
        start_date := max(entry.day for timesheet in timesheets for entry in timesheet.entries),
        start_date + timedelta(generic_get("Due period (days from last timesheet entry)", 14, typecast=int, do_strip=True)),
        menu_invoice_party(PartyType.From),
        menu_invoice_party(PartyType.To),
        Payment(
            TSConfig.get("payment:bsb"),
            TSConfig.get("payment:account")
        ),
        [
            InvoiceLine(
                ts.total_hrs,
                f"Hour of work (week starting {ts.week_of})",
                TSConfig.get("hourly_rate")
            ) for ts in timesheets
        ]
    )


def menu_timesheet() -> Timesheet:
    """Show menu for timesheet"""
    entries = []
    hprint("Timesheet entries (Ctrl+C to stop)")
    try:
        while True:
            entries.append(menu_timesheet_entry())

    
    except KeyboardInterrupt:
        print("Finished getting timesheet entries")

    return Timesheet(
        TSConfig.get("contractor:name"),
        generic_get("Timesheet title (i.e., project)", default="Project"),
        TSConfig.get("hourly_rate"),
        entries
    )
    
def menu_timesheet_entry() -> TimesheetEntry:
    """Show menu for timesheet entry"""
    return TimesheetEntry (
        generic_get("Day", typecast=std_datefmt),
        generic_get("Hours worked", typecast=float),
        generic_get("Description", "")
    )
    
