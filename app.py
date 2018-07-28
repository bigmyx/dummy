import os
from flask import Flask, request, jsonify, redirect, send_from_directory
from werkzeug.utils import secure_filename
from flask_httpauth import HTTPBasicAuth


UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


users = {
    "user1": "1234",
    "user2": "5678"
}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/files/<filename>')
@auth.login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/files/', methods=['GET', 'POST'])
@auth.login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'empty file'
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return 'file not allowed'

    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
