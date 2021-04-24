import sqlite3
from reportlab.lib import colors, pagesizes
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime

today = datetime.date.today()

d1 = today.strftime("%b-%d-%Y")

filename = "pdfmaker.pdf".format(d1)
conn = sqlite3.connect('Hiccups.db')  # create a DB if there is not one
c = conn.cursor()
c.execute('''SELECT 
    SKU,
    CASE
        WHEN LENGTH(prodDesc) > 50 THEN
            substr(prodDesc, 1, 50) || "..."
        ELSE
            prodDesc
        END shortProdDesc,
        
    unitsInStock
FROM products
WHERE unitsInStock == 0
LIMIT 20 ;''')

data = c.fetchall()
labels= ['SKU', 'Product Description', 'Quantity']

data.insert(0, labels)
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
pdf = SimpleDocTemplate(
    filename,
    pagesize = letter
)

table = Table(data)
style = TableStyle([
    ('BACKGROUND', (0,0), (3,0), colors.lightblue),
    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Arial'),
    ('FONTSIZE', (0,0), (-1,0), 14),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),

])

table.setStyle(style)

elems = []
elems.append(table)

pdf.build(elems)