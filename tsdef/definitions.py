from dataclasses import dataclass
from enum import Enum
from datetime import date as Date, timedelta
import json
import os
from types import NoneType
from tshelpers import iter_read
import jsonpickle as jp


class Weekday(Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"
    

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


@dataclass
class Invoice:
    identifier: str
    date: Date
    due_date: Date
    bill_from: InvoiceParty
    bill_to: InvoiceParty
    lines: list[InvoiceLine]
    
    @property
    def total(self): return sum(line.price for line in self.lines)


@dataclass
class TimesheetEntry:
    day: Date
    hours: float
    description: str


@dataclass
class Timesheet:
    entries: list[TimesheetEntry]
    
    @property
    def total_hrs(self): return sum(entry.hours for entry in self.entries)
    
    @property
    def week_of(self): return (earliest := min(entry.day for entry in self.entries)) - timedelta(earliest.weekday)

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

        except:
            # Ignore invalids
            pass

        return res

    @property
    def invoices(self):
        return [value for value in self.items if type(value) is Invoice]


    @property
    def timesheets(self):
        return [value for value in self.items if type(value) is Timesheet]
