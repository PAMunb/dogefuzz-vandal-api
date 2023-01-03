"""
Main API
"""
import subprocess
import os
import io
import tempfile
import uuid

from flask import Flask, send_file, request, json
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.route("/", methods = ['POST'])
def decompile():
    """
    Decompiles file
    """
    body = request.get_json()

    file_id = str(uuid.uuid4())
    with open(f"/tmp/{file_id}", "w", encoding="UTF-8") as file:
        file.write(body["source"])
    
    print("writing" + file.name)

    args = ["/app/vandal/bin/decompile", "-v", f"/tmp/{file_id}"]
    (std_out, std_err) = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()

    if std_err is not None:
        return std_err, 422

    return send_file(
        io.BytesIO(std_out),
        mimetype='text/plain'
    )

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
