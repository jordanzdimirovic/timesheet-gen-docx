from dataclasses import dataclass
from enum import Enum
from datetime import date as Date


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
    hours = float
    description = str


@dataclass
class Timesheet:
    entries: list[TimesheetEntry]
    
    @property
    def total_hrs(self): return sum(entry.hours for entry in self.entries)
    
    @property
    def week_of(self): return 
