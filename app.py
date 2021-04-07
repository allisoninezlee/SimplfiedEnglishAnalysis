import os
from os import path
import argparse
import parsers
import csv
import traceback
import uuid
from flask import (
    Flask,
    redirect,
    request,
    jsonify,
    make_response,
    send_from_directory,
    url_for,
    render_template,
)
from flask.wrappers import Response
from werkzeug.utils import secure_filename

from document import Document


app = Flask(__name__)


DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/downloads/"
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/downloads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["DOWNLOAD_FOLDER"], filename, as_attachment=True
    )


@app.route("/", methods=["GET", "POST"])
def upload():
    print("from upload")
    if request.method == "POST":
        file = request.files["file"]
        if file:
            print(file)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # file.save(app.config["UPLOAD_FOLDER"],filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                response = parse_file(filename)
                # os.path.join(app.config["UPLOAD_FOLDER"].unlink(filename)
                os.unlink(app.config["UPLOAD_FOLDER"] + filename)
                # return jsonify(data=response)
                return render_template("form.html", data=[response], hasresult=True)
                # return jsonify(data=response)
        return {"message": "not PDF file, try again!", "success": False}
    return render_template("form.html", hasresult=False)


def parse_file(file):
    try:
        if not file:
            print("File   does not exist. Exiting...")
            exit()

        print("Processing file: " + file)

        # open file
        pdf = parsers.open_pdf(os.path.join(app.config["UPLOAD_FOLDER"] + file))
        text = parsers.extract_text(pdf)

        # create document object for this pdf
        # (hard coding some attributes until we have an algorithm to get this info directly from reading PDF)
        doc1 = Document(pdf, "Document 1", 2020, "Airplane", file)

        # get list of span objects - one for each sentence in pdf file
        total_sentences = parsers.get_sentences(text)

        # get list of token (noun) objects
        # note: we'll need to adjust so that the same noun with different capitalization isn't picked up twice
        #       (airplane vs Airplane) and the same with singular/plural nouns (airplane vs airplanes)
        total_nouns = parsers.get_nouns(total_sentences)
        # Open csv files to write to
        name = str(uuid.uuid4())
        csv_name = name + "_nouns.csv"
        path = "downloads/"
        with open(path + csv_name, "w", newline="") as csvfile:
            nounwriter = csv.writer(csvfile)
            nounwriter.writerow(
                [doc1.document_name, doc1.pub_year, doc1.product, doc1.location]
            )
            for noun in total_nouns:
                nounwriter.writerow([noun.text, noun.context_sentences, noun.num_occur])
            print("Data has been successfully saved to " + csv_name)
            print(request.host_url)
        response = request.host_url + path + csv_name
        return {"downloadlink": response, "success": True}
    except Exception as e:
        traceback.print_exc()
        return {"message": "not PDF file, try again!", "success": False}


if __name__ == "__main__":
    # manager.run()
    app.run(host="0.0.0.0", debug=False)
