import datetime
from turtle import color
from click import clear
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
from reportlab.lib.units import inch
import json  # JSON Decoding
import os, shutil

# Creating Flask App
app = Flask(__name__, static_folder="static", static_url_path="/static")

store_name = ""
store_phone = ""
store_address = "Billing Address: "
store_gstin = ""

store_transactions = []
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
    top_heading_style = ParagraphStyle(
        name="Heading",
        fontWeight="bold",
        fontName="Helvetica",
        fontSize=32,
        textColor=colors.black,
        spaceAfter=20,
        alignment=1,
        leading=40,
    )

    # Style for normal text
    normal_style = ParagraphStyle(
        name="Normal-Text",
        fontWeight="bold",
        fontName="Times-Roman",
        fontSize=14,
        textColor=colors.black,
        spaceAfter=20,
        alignment=0,
    )

    subheading_style = ParagraphStyle(
        name="Subheading-Text",
        fontName="Times-Roman",
        fontSize=15,
        textColor=colors.black,
        alignment=0,
    )

    shop_logo = Image(
        shop_logo_path, width=80, height=60
    )  # Creating an image and Adjusting width and height as needed

    shop_header = store_name
    shop_header_paragraph = create_paragraph(shop_header, top_heading_style)

    shop_address_paragraph = create_paragraph(store_address, subheading_style)

    table_style = TableStyle(
        [
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]
    )

    datetime_arr = [f"Date: {date}", f"Time: {time}"]

    datetime_table = Table(
        datetime_arr,
        colWidths=[100, 100],
        rowHeights=[20, 20],
    )

    datetime_table.setStyle(table_style)

    table = [
        [shop_logo, shop_header_paragraph],
        [shop_address_paragraph, datetime_table],
    ]
    col_widths = [130, None]
    college_header_table = Table(table, colWidths=col_widths, rowHeights=[150, 50])

    college_header_table.setStyle(table_style)
    story.append(college_header_table)
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
    global time, date, store_transactions
    data = request.get_json()
    time = data.get("time")
    date = data.get("date")
    store_transactions = data.get("transactions")
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
    clear_folders("./temp")
    clear_folders("./uploads")
    app.run("0.0.0.0", port=6969)
