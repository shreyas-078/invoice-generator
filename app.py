from flask import Flask, render_template, request, jsonify, Response  # Backend Server
from reportlab.lib.pagesizes import letter  # To create a new document with a template
from reportlab.lib import colors  # For Colors
import os
from reportlab.lib.styles import (
    ParagraphStyle,
)  # To add paragraph styling
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Image,
    Spacer,
)  # Reportlab Utility for customization
import os, shutil

from torch import normal

# Creating Flask App
app = Flask(__name__, static_folder="static", static_url_path="/static")

store_name = ""
store_phone = ""
store_address = "Billing Address: "
store_gstin = ""

store_transactions = []
store_tax = ""
store_tax_num = 0
time = ""
date = ""
shop_logo_path = ""  # Store Logo Path


# Reportlab Function to create paragraph
def create_paragraph(text, style):
    return Paragraph(text, style)


# Homepage
@app.route("/")
def home():
    global store_address, store_gstin, store_name, store_phone, store_transactions, shop_logo_path
    store_name = ""
    store_phone = ""
    store_address = "Billing Address: "
    store_gstin = ""

    store_transactions = []
    shop_logo_path = ""  # Store Logo Path
    return render_template("index.html")


def template_1():
    story = []

    # Creating a PDF Document Template
    doc = SimpleDocTemplate(
        "invoices/template-1-invoice.pdf",
        pagesize=letter,
        topMargin=-30,
        leftMargin=50,
        bottomMargin=0,
    )

    # Style for Top Heading for Store Name
    top_heading_style_left = ParagraphStyle(
        name="Top-Heading",
        fontWeight="bold",
        fontName="Helvetica",
        fontSize=32,
        textColor=colors.black,
        spaceAfter=20,
        alignment=0,
        leading=40,
        leftIndent=30,
    )

    tax_heading_style = ParagraphStyle(
        name="Tax-Heading",
        fontWeight="bold",
        fontName="Helvetica",
        fontSize=32,
        textColor=colors.black,
        alignment=1,
        spaceBefore=35,
        spaceAfter=40,
    )

    # Style for normal text
    normal_style = ParagraphStyle(
        name="Normal-Text",
        fontWeight="bold",
        fontName="Times-Roman",
        fontSize=18,
        textColor=colors.black,
        spaceAfter=20,
        alignment=2,
        leading=15,
    )

    table_heading_style = ParagraphStyle(
        name="Table-Headings",
        fontWeight="bold",
        fontName="Times-Roman",
        fontSize=18,
        textColor=colors.black,
        spaceAfter=20,
        alignment=1,
    )

    subheading_style = ParagraphStyle(
        name="Subheading-Text",
        fontName="Times-Roman",
        fontSize=18,
        textColor=colors.black,
        alignment=0,
        leading=15,
    )

    normal_bottom_style = ParagraphStyle(
        name="Normal-Text",
        fontWeight="bold",
        fontName="Helvetica",
        fontSize=22,
        textColor=colors.black,
        alignment=2,
        spaceBefore=10,
        spaceAfter=15,
    )

    gstin_left_style = ParagraphStyle(
        name="Normal-Text",
        fontWeight="bold",
        fontName="Helvetica",
        fontSize=22,
        textColor=colors.black,
        alignment=0,
        spaceAfter=20,
    )

    shop_logo = Image(
        shop_logo_path, width=80, height=60, kind="proportional"
    )  # Creating an image and Adjusting width and height as needed

    shop_header = store_name
    shop_header_paragraph = create_paragraph(shop_header, top_heading_style_left)

    shop_address_paragraph = create_paragraph(store_address, subheading_style)

    table_style = TableStyle(
        [
            ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]
    )

    another_table_style = TableStyle(
        [
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]
    )

    datetime_para = create_paragraph(
        f"Date: {date} <br /> <br /> Time: {time} <br /> <br /> Contact Ph: {store_phone}",
        normal_style,
    )

    shop_logo_table = Table(
        [[shop_logo, shop_header_paragraph]], colWidths=[80, None], rowHeights=[150]
    )

    shop_logo_table.setStyle(another_table_style)

    story.append(shop_logo_table)

    gstin_para = create_paragraph(f"GSTIN: {store_gstin}", gstin_left_style)

    story.append(gstin_para)

    address_datetime_table = [
        [shop_address_paragraph, datetime_para],
    ]
    address_datetime_table_design = Table(
        address_datetime_table, colWidths=[150, None], rowHeights=[50]
    )

    address_datetime_table_design.setStyle(table_style)
    story.append(address_datetime_table_design)

    tax_invoice_heading = create_paragraph("TAX INVOICE", tax_heading_style)

    story.append(tax_invoice_heading)

    transaction_table_style = TableStyle(
        [
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey,
            ),  # Set Background for all columns of first row to grey
            (
                "ALIGN",
                (0, 0),
                (-1, 0),
                "CENTER",
            ),  # Center align all items in first row
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Times-Roman"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 1), (-1, -1), "Times-Roman"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ],
    )

    item_name_para = create_paragraph("Item Name", table_heading_style)
    item_description_para = create_paragraph("Description", table_heading_style)
    item_amount_para = create_paragraph("Item Amount", table_heading_style)
    item_quantity_para = create_paragraph("Item Quantity", table_heading_style)
    total_amount = create_paragraph("Total Amount", table_heading_style)

    transaction_table = [
        [
            item_name_para,
            item_description_para,
            item_amount_para,
            item_quantity_para,
            total_amount,
        ]
    ]

    # Create Array iterating only the values of itemsArray received from frontend
    total_amt_arr = []
    for i in store_transactions:

        total_amt = int(i.get("itemAmount")) * int(i.get("itemQuantity"))
        total_amt_arr.append(total_amt)
        total_amt_str = f"Rs. {str(total_amt)}"

        transaction_table.append(
            [
                create_paragraph(i.get("itemName"), normal_style),
                create_paragraph(i.get("itemDescription"), normal_style),
                create_paragraph(f"Rs. {i.get('itemAmount')}", normal_style),
                create_paragraph(i.get("itemQuantity"), normal_style),
                create_paragraph(
                    total_amt_str,
                    normal_style,
                ),
            ]
        )

    transaction_table_row_heights = [50]

    for i in range(len(transaction_table) - 1):
        max_row_height = int(len(store_transactions[i].get("itemDescription"))) * 2 + 25
        transaction_table_row_heights.append(max_row_height)

    transaction_table_design = Table(
        transaction_table,
        colWidths=[100, 140, 100, 100, 100],
        rowHeights=transaction_table_row_heights,
    )

    transaction_table_design.setStyle(transaction_table_style)
    story.append(transaction_table_design)

    subtotal_amt = sum(total_amt_arr)
    subtotal_para = f"SUBTOTAL: Rs. {subtotal_amt}"

    subtotal_para_design = create_paragraph(subtotal_para, normal_bottom_style)

    story.append(subtotal_para_design)

    total_after_taxes_text = create_paragraph(
        f"TOTAL (after taxes) (+{store_tax}): Rs. {round(subtotal_amt + (store_tax_num/100)*subtotal_amt)}",
        normal_bottom_style,
    )
    story.append(total_after_taxes_text)

    doc.build(story)
    return "./invoices/template-1-invoice.pdf"


@app.route("/default", methods=["POST"])
def default_post():
    global store_name, store_address, store_phone, store_gstin
    data = request.get_json()
    store_address += data.get("address")
    store_name = data.get("shopName")
    store_phone = data.get("phNo")
    store_gstin = data.get("gstin")
    return jsonify({"message": "Successful Upload of Data"})


@app.route("/default-page", methods=["GET"])
def default_get():
    if store_phone == store_gstin == store_address == store_name == "":
        return "<h1 style='text-align: center; font-family: Arial, sans-serif; width:100%;'>An Error Occured, this could happen if you try to load the default page without providing store details.<h1>"
    return render_template("default.html")


@app.route("/upload-transaction", methods=["POST"])
def upload_transaction():
    global time, date, store_transactions, store_tax, store_tax_num
    data = request.get_json()
    time = data.get("time")
    date = data.get("date")
    store_transactions = data.get("transactions")
    store_tax = data.get("totalTax")
    store_tax_num = int(store_tax[: len(store_tax) - 1])
    path = template_1()
    pdf_raw = ""
    with open(path, "rb") as f:
        pdf_raw = f.read()
    return Response(pdf_raw, mimetype="application/pdf")


@app.route("/upload-file", methods=["POST"])
def upload_file_handler():
    global shop_logo_path
    data = request.files["file"]
    upload_path = os.path.join(os.getcwd(), f"uploads")
    data.save(os.path.join(upload_path, data.filename))
    shop_logo_path = f"uploads/{data.filename}"
    return jsonify({"message": "File Uploaded Successfully"})


def clear_folders(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


if __name__ == "__main__":
    clear_folders("./invoices")
    clear_folders("./uploads")
    app.run("0.0.0.0", port=6969)
