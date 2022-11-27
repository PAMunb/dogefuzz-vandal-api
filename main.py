import subprocess
import os
import io

from flask import Flask, send_file

app = Flask(__name__)

@app.route("/")
def decompile():
    output = subprocess.Popen(["/app/vandal/bin/decompile", "-v", "/app/vandal/examples/dao_hack.hex"], stdout=subprocess.PIPE).communicate()[0]
    return send_file(
        io.BytesIO(output),
        mimetype='text/plain'
    )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
