"""vendor_sheets.py: one order sheet per seller, in the team's purchase-form layout (run from repo root)."""
import csv, os, re
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

SRC = "docs/full-order-sheet.csv"
OUT = "docs/vendor-orders"
HDR = ["Item", "Quantity", "Cost per Item", "Total Cost", "Item/SKU Number", "Other Specs if Applicable ", "Link", "Total"]
WIDTHS = {"A": 45, "B": 9, "C": 14.29, "D": 11, "E": 28, "F": 60, "G": 86.29, "H": 11}
FILL = PatternFill("solid", fgColor="FFF4B083")
USD = '_("$"* #,##0.00_);_("$"* \\(#,##0.00\\);_("$"* "-"??_);_(@_)'
BOARD = {"Drone parts (1 drone)": "Drone", "Flight controller parts (1 board)": "Flight controller", "Charging board parts (1 board)": "Charging board"}

rows = [r for r in csv.reader(open(SRC, encoding="utf-8-sig")) if r and r[1] and r[0] != "Group"]
sellers = []
for r in rows:
    if r[1] not in sellers:
        sellers.append(r[1])

def sku(r):
    m = re.search(r"amazon\.com/dp/([A-Z0-9]{10})", r[5])
    if m:
        return m.group(1)
    return "" if "/s?k=" in r[5] else r[3]

def item(r):
    # Drone parts are named by product; electronic parts read better by what they are
    return r[3] if r[0].startswith("Drone") else r[4]

def specs(r):
    keep = [s.strip() for s in re.split(r"(?<=\.)\s+", r[8]) if s.strip()]
    keep = [s for s in keep if not s.startswith(("Buy ", "Was ", "Take the price", "Provisional"))]
    text = " ".join(keep[:2])
    extra = r[4] if r[0].startswith("Drone") else ""
    return "; ".join(x for x in [BOARD.get(r[0], ""), extra, text] if x)

def fill_sheet(ws, seller_rows):
    ws.append(HDR)
    for c in ws[1]:
        c.font = Font(bold=True); c.fill = FILL
    for i, r in enumerate(seller_rows, start=2):
        ws.append([item(r), int(r[2]), float(r[6]) if r[6] else None, "=B%d*C%d" % (i, i), sku(r), specs(r), r[5], "=D%d" % i])
        for col in "CDH":
            ws["%s%d" % (col, i)].number_format = USD
        ws["G%d" % i].hyperlink = r[5]
    n = len(seller_rows) + 2
    ws["G%d" % n] = "Please select fastest shipping available"; ws["G%d" % n].font = Font(bold=True)
    ws["H%d" % n] = 0; ws["H%d" % n].number_format = USD
    ws["G%d" % (n + 1)] = "Grand Total"; ws["G%d" % (n + 1)].font = Font(bold=True)
    ws["H%d" % (n + 1)] = "=SUM(H2:H%d)" % n; ws["H%d" % (n + 1)].font = Font(bold=True); ws["H%d" % (n + 1)].number_format = USD
    for k, v in WIDTHS.items():
        ws.column_dimensions[k].width = v

os.makedirs(OUT, exist_ok=True)
combined = Workbook(); combined.remove(combined.active)
for s in sellers:
    sr = [r for r in rows if r[1] == s]
    wb = Workbook(); fill_sheet(wb.active, sr); wb.active.title = s[:31]
    wb.save(os.path.join(OUT, s.lower().replace(" ", "-") + ".xlsx"))
    fill_sheet(combined.create_sheet(s[:31]), sr)
    print("%-18s %2d lines  $%.2f" % (s, len(sr), sum(int(r[2]) * float(r[6]) for r in sr if r[6])))
combined.save(os.path.join(OUT, "all-vendors.xlsx"))
