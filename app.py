from flask import Flask, render_template, request, jsonify, send_from_directory, abort
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# ----------------------------
#   KONFIGURATION
# ----------------------------
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'geocache')
}

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
TILE_FOLDER = os.path.join(BASE_DIR, 'static', 'tiles')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TILE_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# ----------------------------
#   DB FUNKTIONEN
# ----------------------------
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def insert_cache(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO caches (name, lat, lon, found_date, hint, remark, location, image)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, tuple(data.values()))
    conn.commit()
    cid = cursor.lastrowid
    cursor.close()
    conn.close()
    return cid

def get_all_caches():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM caches ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# ----------------------------
#   HILFSFUNKTIONEN
# ----------------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ----------------------------
#   ROUTEN
# ----------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/caches', methods=['GET'])
def api_get_caches():
    data = get_all_caches()
    for c in data:
        if c.get("image"):
            c["image"] = f"/uploads/{c['image']}"
    return jsonify(data)

@app.route('/api/caches', methods=['POST'])
def api_create_cache():
    form = request.form
    if not form.get('lat') or not form.get('lon') or not form.get('name'):
        return jsonify({'error': 'lat, lon, name required'}), 400

    image_name = ""
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            fname = secure_filename(file.filename)
            fname = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{fname}"
            path = os.path.join(UPLOAD_FOLDER, fname)
            file.save(path)
            try:
                Image.open(path).verify()
                image_name = fname
            except:
                os.remove(path)
                return jsonify({'error': 'invalid image'}), 400

    cid = insert_cache({
        "name": form.get('name'),
        "lat": form.get('lat'),
        "lon": form.get('lon'),
        "found_date": form.get('found_date'),
        "hint": form.get('hint'),
        "remark": form.get('remark'),
        "location": form.get('location'),
        "image": image_name
    })

    return jsonify({'id': cid}), 201

@app.route('/uploads/<filename>')
def uploads(filename):
    path = os.path.normpath(os.path.join(UPLOAD_FOLDER, filename))
    if not path.startswith(UPLOAD_FOLDER):
        abort(403)
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/tiles/<int:z>/<int:x>/<int:y>.png')
def offline_tiles(z, x, y):
    path = os.path.normpath(os.path.join(TILE_FOLDER, str(z), str(x), f"{y}.png"))
    if not path.startswith(TILE_FOLDER) or not os.path.isfile(path):
        abort(404)
    return send_from_directory(os.path.dirname(path), os.path.basename(path))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5012, debug=True)
