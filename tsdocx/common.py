import os
from docxtpl import DocxTemplate
from tsdef import Collection, Invoice, Timesheet
from tshelpers import dictify

def render_timesheet(timesheet: Timesheet, template: DocxTemplate, out_path: str):
    template.render(dictify(timesheet))
    template.save(os.path.join(out_path, f"{timesheet.week_of}.timesheet.docx"))


def render_invoice(invoice: Invoice, template: DocxTemplate, out_path: str):
    template.render(dictify(invoice))
    template.save(os.path.join(out_path, f"{invoice.identifier}.invoice.docx"))


def render_all(collection: Collection, p_tpl_timesheet: str, p_tpl_invoice: str, rel_out_path: str = "render") -> int:
    """Renders all Timesheets and Invoices in `collection`"""
    if not all(os.path.isfile(p) for p in (p_tpl_invoice, p_tpl_timesheet)):
        raise FileNotFoundError(f"One of both templates not found")
    
    docx_timesheet = DocxTemplate(p_tpl_timesheet)
    docx_invoice = DocxTemplate(p_tpl_invoice)
    
    out_path = os.path.join(collection.directory_path, rel_out_path)
    
    os.makedirs(out_path, exist_ok=True)
    
    timesheets = collection.timesheets
    invoices = collection.invoices
    
    # Do all timesheet rendering
    for timesheet in timesheets:
        try:
            render_timesheet(timesheet, docx_timesheet, out_path)
        except Exception as e:
            raise e
            print(f"Timesheet render failed: {e}")
        
    # Do all invoice rendering
    for invoice in invoices:
        try:
            render_invoice(invoice, docx_invoice, out_path)
        except Exception as e:
            print(f"Invoice render failed: {e}")
    
    return len(timesheets) + len(invoices)
    