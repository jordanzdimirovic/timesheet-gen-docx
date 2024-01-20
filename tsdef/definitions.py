from dataclasses import dataclass
from enum import Enum
from datetime import date as Date, timedelta
import json
import os
from types import NoneType
from tshelpers import iter_read
import jsonpickle as jp

from tshelpers.helpers import pprint_date

class Weekday(Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"
    
    
WEEKDAY_NAMES = [v.value for v in Weekday]


class PartyType(Enum):
    From = "Bill From"
    To = "Bill To"


@dataclass
class InvoiceParty:
    name: str 
    address: str
    business_number: str

@dataclass
class InvoiceLine:
    quantity: int
    description: str
    unit_price: float
    
    @property
    def price(self): return self.unit_price * self.quantity
    
    @property
    def price_pretty(self): return f"${self.price:.2f}"


@dataclass
class Payment:
    bsb: str
    account: str


@dataclass
class Invoice:
    identifier: str
    date: Date
    due_date: Date
    bill_from: InvoiceParty
    bill_to: InvoiceParty
    payment: Payment
    lines: list[InvoiceLine]
    
    @property
    def total(self): return sum(line.price for line in self.lines)
    
    @property
    def total_pretty(self): return f"${self.total:.2f}"

    @property
    def date_pretty(self) -> str: return pprint_date(self.date)
    
    @property
    def due_date_pretty(self) -> str: return pprint_date(self.due_date)
    

@dataclass
class TimesheetEntry:
    day: Date
    hours: float
    description: str
    
    @property
    def day_of_week(self) -> str: return WEEKDAY_NAMES[self.day.weekday()]    


@dataclass
class Timesheet:
    name: str
    title: str
    hourly_pay: float
    
    entries: list[TimesheetEntry]
    
    @property
    def hourly_pay_fmt(self): return f"${self.hourly_pay:.2f}"

    @property
    def total_hrs(self): return sum(entry.hours for entry in self.entries)
    
    @property
    def week_of(self): return (earliest := min(entry.day for entry in self.entries)) - timedelta(earliest.weekday())

    @property
    def week_of_pretty(self): return pprint_date(self.week_of)


    @staticmethod
    def from_dict(json: dict):
        try:
            return Timesheet(
                json['entries']
            )
        except KeyError as e:
            raise ValueError("Invalid timesheet dictionary") from e

type CollectionItem = Invoice | Timesheet

@dataclass
class Collection:
    directory_path: str
    
    def store(self, obj: CollectionItem, name: str):
        if type(obj) not in (Invoice, Timesheet): raise ValueError("Can't store any object other than 'Invoice' or 'Timesheet' in Collection")
        with open(os.path.join(self.directory_path, f"{name.replace(" ", '-')}.{type(obj).__name__.lower()}.json"), "w") as f:
            f.write(jp.encode(obj))

    @property
    def items(self) -> CollectionItem:
        res = []
        try:
            for data in iter_read(self.directory_path):
                res.append(jp.decode(data))

        except Exception as e: 
            # Ignore invalids
            print(f"File couldn't be decoded: {e}")
            pass

        return res

    @property
    def invoices(self):
        return sorted((value for value in self.items if type(value) is Invoice), key = lambda inv: inv.date)


    @property
    def timesheets(self):
        items = self.items
        return sorted((value for value in items if type(value) is Timesheet), key = lambda ts: ts.week_of)
