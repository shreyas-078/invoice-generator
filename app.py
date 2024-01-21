from flask import Flask, render_template, request, jsonify  # Backend Server
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

# Creating Flask App
app = Flask(__name__, static_folder="static", static_url_path="/static")


# Reportlab Function to create paragraph
def create_paragraph(text, style):
    return Paragraph(text, style)


# Homepage
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate-pdf-template-1", methods=["POST"])
def template_1():
    data = json.loads(request.data.decode("utf-8"))
    story = []

    # Creating a PDF Document Template
    doc = SimpleDocTemplate(
        "template-1-invoice",
        pagesize=letter,
        topMargin=0,
        leftMargin=50,
        bottomMargin=0,
    )

    # Style for Top Heading for Store Name
    top_heading_style = ParagraphStyle(
        name="Heading",
        fontWeight="bold",
        fontName="Helvetica",
        fontSize=20,
        textColor=colors.black,
        spaceAfter=20,
        alignment=1,
        leading=25,
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

    shop_logo_path = "shop_logo_path"  # Store Logo Path
    shop_logo = Image(
        shop_logo_path, width=60, height=60
    )  # Creating an image and Adjusting width and height as needed

    shop_header = ""
    shop_header_paragraph = create_paragraph(shop_header, top_heading_style)

    table_style = TableStyle(
        [
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]
    )

    table = [[shop_logo, shop_header_paragraph]]
    col_widths = [60, None]
    college_header_table = Table(table, colWidths=col_widths, rowHeights=[100])

    college_header_table.setStyle(table_style)
    story.append(college_header_table)


@app.route("/default", methods=["GET", "POST"])
def default_():
    return render_template("default.html")


@app.route("/upload-file", methods=["POST"])
def upload_file_handler():
    data = request.files["file"]
    upload_path = os.path.join(os.getcwd(), f"temp")
    data.save(os.path.join(upload_path, data.filename))
    return jsonify({"message": "File Uploaded Successfully"})


if __name__ == "__main__":
    app.run(port=6969)
