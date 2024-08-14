from flask import Flask, session, url_for, render_template, redirect, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename
import uuid as uuid
import numpy as np
import os
import pickle
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications import ResNet50, imagenet_utils
from tensorflow.keras.models import load_model
import joblib
from PIL import Image
from google.cloud import storage
import logging
import datetime
from io import BytesIO
import subprocess
from google.cloud.sql.connector import Connector, IPTypes
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pymysql

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "1234567890")
os.environ['INSTANCE_CONNECTION_NAME'] = 'solid-scope-415202:asia-southeast2:servcdet'
os.environ['CLOUDSQL_PROXY_SOCK'] = f'/tmp/cloudsql/{os.environ["INSTANCE_CONNECTION_NAME"]}'
os.environ['MYSQL_USER'] = 'albarmaula@gmail.com'
os.environ['MYSQL_PASSWORD'] = '123456'

# # app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_HOST'] = '34.101.254.77'
# app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
# app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
# app.config['MYSQL_DB'] = 'servcdet' 
# app.config['MYSQL_UNIX_SOCKET'] = '/cloudsql/solid-scope-415202:asia-southeast2:servcdet'

# mysql = MySQL(app)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "service-account-key.json"
# Initialize SQLAlchemy
db = SQLAlchemy()

# Function to create a database connection
def get_connection():
    connector = Connector()
    connection = connector.connect(
        os.environ['INSTANCE_CONNECTION_NAME'],
        "pymysql",
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        db="servcdet",
        ip_type=IPTypes.PUBLIC,  # or IPTypes.PRIVATE depending on your configuration
    )
    return connection

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'creator': get_connection
}

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

client = storage.Client()
bucket_name = 'servcdet'
bucket = client.get_bucket(bucket_name)
    
def get_signed_url(filename):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)
    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=15),
        method="GET"
    )
    return url

def delete_blob(bucket_name, blob_name):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()
    print(f"Blob {blob_name} deleted.")

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif', 'svg', 'webp', 'heic', 'ico', 'raw', 'dng', 'ai', 'eps', 'psd', 'pdf'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
          
# app.config['UPLOAD_FOLDER'] = 'static/uploads' 

###########################################(MACHINE LEARNING)#############################################################
print("[INFO] Loading The Machine Learning...")
resnet_model = ResNet50(weights="imagenet", include_top=False)
scaler = joblib.load("ml/.2scaler.pkl")
pca = joblib.load("ml/.2pca.pkl")
svm_classifier = joblib.load("ml/.2svm_classifier.pkl")
with open("ml/2le.cpickle", "rb") as f:
    le = pickle.load(f)

def preprocess_image(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)
    features = resnet_model.predict(image)
    features = features.reshape((features.shape[0], -1))
    features = scaler.transform(features)
    features = pca.transform(features)
    return features

###########################################(FUNCTIONS)#############################################################
#Done
@app.route('/change_status_detection', methods=['POST'])
def change_status_detection():
    if "user_id" in session:
        data = request.get_json()
        detection_id = data.get('id')
        if detection_id:
            current_status = db.session.execute(text("SELECT status FROM detection WHERE detection_id = :detection_id"),{'detection_id': detection_id}).fetchone()
            if current_status:
                new_status = 'non-aktif' if current_status[0] == 'aktif' else 'aktif'
                db.session.execute(text("UPDATE detection SET status = :status WHERE detection_id = :detection_id"),
                    {'status': new_status, 'detection_id': detection_id})
                db.session.commit()
                flash('Status berhasil diperbarui!', 'success')
                return jsonify(success=True)
            else:
                flash('ID tidak valid!', 'danger')
                return jsonify(success=False, message="Invalid ID"), 400
        else:
            flash('ID tidak valid!', 'danger')
            return jsonify(success=False, message="Invalid ID"), 400
    else:
        flash('Anda tidak diizinkan untuk melakukan aksi ini!', 'danger')
        return jsonify(success=False, message="Unauthorized"), 403

#Done
@app.route('/uploadpp', methods=['POST'])
def uploadpp():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            pic_name = "pp_" + str(uuid.uuid1()) + "_" + filename

            # Upload the file to Google Cloud Storage
            blob = bucket.blob(pic_name)
            blob.upload_from_file(uploaded_file)

            # Check image dimensions
            image = Image.open(uploaded_file)
            if image.width < 100 or image.height < 100:
                flash('Gambar anda terlalu kecil! Tolong unggah gambar berkualitas baik!', 'danger')
                return redirect(url_for("doctor"))

            user_id = session.get('user_id')
            db.session.execute(text("UPDATE user SET profile_picture = :pic_name WHERE user_id = :user_id"),
                    {'pic_name': pic_name, 'user_id': user_id})
            db.session.commit()
            
            flash("Foto profil anda telah diubah!", 'success')
            return redirect(url_for('doctor'))
        else:
            flash('Tolong unggah file gambar dengan ekstensi yang benar!', 'danger')
            return redirect(url_for('doctor'))
        
###########################################(THE PAGE)#############################################################
print("[INFO] Loading The Page...")
#Done
@app.route('/')
def index():
    return render_template("index.html")

#Done
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))

#Done
@app.route('/login', methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            email = request.form["emailForm"]
            password = request.form["passForm"]
            user = db.session.execute(text("SELECT * FROM user WHERE email = :email"),{'email': email}).fetchone() 
            if user:
                username = user[1]
                hashed_password = user[4]
                if check_password_hash(hashed_password, password):
                    session['status'] = user[7] 
                    status = session.get('status')
                    if status == "aktif":
                        session['user_id'] = user[0]
                        session['username'] = user[1]
                        session['role'] = user[6]
                        flash('Login berhasil!', 'success')
                        return redirect(url_for('index'))
                    else:
                        flash('Akun anda tidak dapat digunakan, Silahkan hubungi admin!', 'danger')
                        return redirect(url_for('logout'))
                else:
                    flash('Password salah! Silakan coba lagi!', 'danger')
                    return redirect(url_for('login'))
            else:
                flash('Email tidak ditemukan! Silakan coba lagi!', 'danger')
                return redirect(url_for('login'))
        else:
            if "user_id" in session:
                return redirect(url_for("user"))
            else:
                return render_template("login.html")
    except Exception as e:
        logging.error(f"Error in login: {e}")
        return jsonify(success=False, message="An error occurred"), 500
    
        
###########################################(DOCTOR)#############################################################
#Done
@app.route('/doctor')
def doctor():
    if "user_id" in session:
        role = session.get('role')
        if role == "dokter":
            user_id = session.get('user_id')      
            user_data = db.session.execute(text("SELECT * FROM user WHERE user_id = :user_id"),{'user_id': user_id}).fetchone()
            
            file_name = user_data[8]
            image_url = get_signed_url(file_name)
            
            page = request.args.get('page', 1, type=int)
            per_page = 10
            offset = (page - 1) * per_page
            
            total = db.session.execute(text("SELECT COUNT(*) FROM detection WHERE user_id = :user_id AND status = :status"),{'user_id': user_id, 'status':'aktif'}).fetchone()[0]
            
            detection_data = db.session.execute(text("""SELECT d.detection_id, d.image, d.label, d.time, p.username AS patient_username, d.note, u.username AS doctor_username, d.confidence, p.nik
                FROM detection d
                JOIN patient p ON d.patient_id = p.id
                JOIN user u ON d.user_id = u.user_id
                WHERE d.user_id = :user_id AND d.status = 'aktif' LIMIt :per_page OFFSET :offset"""),
            {'user_id': user_id, 'per_page':per_page, 'offset':offset}).fetchall()
            
            detection_data_with_images = []
            for detection in detection_data:
                filename = detection[1] 
                this_image_url = get_signed_url(filename)
                data_with_image = list(detection) + [this_image_url]
                detection_data_with_images.append(data_with_image)
            
            return render_template("doctor.html", user_data=user_data, image_url=image_url,
                                   detection_data=detection_data_with_images, 
                                   page=page, per_page=per_page, total=total)
        if role == "admin":
            return redirect(url_for("admin"))
        if role == "superadmin":
            return redirect(url_for("superadmin"))
        else:
            flash('Anda tidak dapat mengakses halaman ini! Silahkan login kembali!', 'danger')
            return redirect(url_for('logout'))
    else:
        flash("Anda belum Login!", 'danger')
        return redirect(url_for("login"))
    
#done
@app.route('/doctor/detection', methods=["GET", "POST"])
def doctor_detect():
    if "user_id" in session:
        role = session.get('role')
        if role == "dokter":
            patients = db.session.execute(text("SELECT id, username FROM patient")).fetchall()

            if request.method == "POST":
                patient_id = request.form['patientDetForm']
                file = request.files['imgDetForm']
                doct_id = session.get('user_id')
                
                if file.filename == '':
                    flash('Tolong masukkan data formulir secara lengkap!', 'danger')
                    return redirect(url_for("doctor_detect"))

                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_name = "det_" + str(uuid.uuid1()) + "_" + filename
                    blob = bucket.blob(file_name)
                    blob.upload_from_file(file)

                    # Save file to buffer
                    buffer = BytesIO()
                    file.seek(0)  # Ensure file pointer is at the start
                    file.save(buffer)
                    buffer.seek(0)  # Reset buffer pointer to the start

                    # Debug information
                    file_size = buffer.getbuffer().nbytes
                    print(f"Uploaded file size: {file_size} bytes")
                    print(f"File content type: {file.content_type}")

                    try:
                        image = Image.open(buffer)
                        image.verify()  # Verify that the image is valid
                        buffer.seek(0)  # Reset buffer to start for full image loading
                        image = Image.open(buffer)  # Reopen image for processing
                        image.load()  # Load image data
                        
                        # Proceed with image processing
                        features = preprocess_image(buffer)
                        confidence = svm_classifier.predict_proba(features)
                        max_confidence = np.max(confidence)
                        
                        if max_confidence < 0.5 or image.width < 100 or image.height < 100:
                            flash('Tolong unggah gambar yang relevan dan/atau berkualitas baik!', 'danger')
                            image.close()
                            delete_blob(bucket_name, file_name)
                            return redirect(url_for("doctor_detect"))
                        else:
                            prediction = svm_classifier.predict(features)
                            label = le.inverse_transform(prediction)[0]
                            confidence_score = confidence[0][prediction[0]] * 100
                            
                            db.session.execute(
                                text(
                                    "INSERT INTO detection (image, label, patient_id, note, user_id, confidence, status) "
                                    "VALUES (:image, :label, :patient_id, :note, :user_id, :confidence, :status)"
                                ),
                                {
                                    'image': file_name,
                                    'label': label,
                                    'patient_id': patient_id,
                                    'note': '',
                                    'user_id': doct_id,
                                    'confidence': confidence_score,
                                    'status': 'aktif'
                                }
                            )
                            db.session.commit()
                            detection_id = db.session.execute(text("SELECT LAST_INSERT_ID()")).scalar()
                            
                            flash('Data deteksi telah disimpan!', 'success')
                            return redirect(url_for('doctor_detection_result', detection_id=detection_id))
                    except Exception as e:
                        logging.error(f"Error processing image from buffer: {e}")
                        flash('Tolong unggah gambar yang relevan dan/atau berkualitas baik!', 'danger')
                        delete_blob(bucket_name, file_name)
                        return redirect(url_for("doctor_detect"))
                else:
                    flash('Tolong unggah file gambar dengan ekstensi yang benar!', 'danger')
                    return redirect(url_for("doctor_detect"))
            else:
                return render_template("doctor-detection.html", patients=patients)
        else:
            flash('Anda tidak dapat mengakses halaman ini! Silahkan login kembali!', 'danger')
            return redirect(url_for('logout'))
    else:
        flash("Anda belum Login!", 'danger')
        return redirect(url_for("login"))


#done
@app.route('/doctor/detection-result', methods=["GET", "POST"])
def doctor_detection_result():
    if "user_id" in session:
        role = session.get('role')
        if role == "dokter":
            user_id = session.get('user_id')
            detection_id = request.args.get('detection_id')
            if request.method == "POST":
                detection_id = request.form['detection_id']
                note = request.form['note']
                
                db.session.execute(
                    text("UPDATE detection SET note = :note WHERE detection_id = :detection_id"),
                    {'note': note, 'detection_id': detection_id}
                )
                db.session.commit()
                
                flash('Catatan berhasil diperbarui!', 'success')
                return redirect(url_for('doctor'))
            if detection_id:
                
                detection_data = db.session.execute(
                text("""
                    SELECT d.detection_id, d.image, d.label, d.time, p.username AS patient_username, d.note, d.user_id, d.confidence, p.nik
                    FROM detection d
                    JOIN patient p ON d.patient_id = p.id
                    WHERE d.detection_id = :detection_id AND d.user_id = :user_id AND d.status = 'aktif'
                """),
                    {'detection_id': detection_id, 'user_id': user_id}
                ).fetchone()
                
                file_name = detection_data[1]
                image_url = get_signed_url(file_name)
                if detection_data:
                    return render_template("doctor-detection-result.html", detection_data=detection_data, image_url=image_url)
                else:
                    flash('Data deteksi tidak ditemukan!', 'danger')
                    return redirect(url_for('doctor'))
            else:
                flash('ID deteksi tidak ditemukan!', 'danger')
                return redirect(url_for('doctor'))
        else:
            flash('Anda tidak dapat mengakses halaman ini! Silahkan login kembali!', 'danger')
            return redirect(url_for('logout'))
    else:
        flash("Anda belum Login!", 'danger')
        return redirect(url_for("login"))

###########################################(ADMIN)#############################################################
#Done
@app.route('/admin', methods=["GET", "POST"])
def admin():
    if "user_id" in session:
        role = session.get('role')
        if role == "admin":
            if request.method == "POST":
                name = request.form["namePatientForm"]
                nik = request.form["nikPatientForm"]
                phone = request.form["phonePatientForm"]
                birthday = request.form["birthdayPatientForm"]
                status = request.form["statusPatientForm"]
                
                existing_nik = db.session.execute(text("SELECT * FROM patient WHERE nik = :nik"),{'nik': nik}).fetchone()
                
                if existing_nik:
                    flash('Pasien dengan NIK ini sudah digunakan!', 'danger')
                    return redirect(url_for('admin'))
                else:
                    db.session.execute(
                    text(
                            "INSERT INTO patient (nik, username, phone, birthday, status) "
                            "VALUES (:nik, :username, :phone, :birthday, :status)"
                        ),
                        {
                            'nik': nik,
                            'username': name,
                            'phone': phone,
                            'birthday': birthday,
                            'status': status
                        }
                    )
                    db.session.commit()
                    
                    flash("Pasien telah ditambahkan!", 'success')
                    return redirect(url_for("admin"))
            else:
                user_id = session.get('user_id')
                user_data = db.session.execute(text("SELECT * FROM user WHERE user_id = :user_id"),{'user_id': user_id}).fetchone()
                file_name = user_data[8]
                image_url = get_signed_url(file_name)

                page = request.args.get('page', 1, type=int)
                per_page = 10
                offset = (page - 1) * per_page
                
                total = db.session.execute(text("SELECT COUNT(*) FROM patient")).fetchone()[0]
                
                patient_data = db.session.execute(text("SELECT * FROM patient LIMIT :per_page OFFSET :offset"), {'per_page':per_page,'offset':offset}).fetchall()
                return render_template("admin.html", user_data=user_data, image_url=image_url, 
                                       patient_data=patient_data, 
                                       page=page, per_page=per_page, 
                                       total=total)
        if role == "dokter":
            return redirect(url_for("doctor"))
        if role == "superadmin":
            return redirect(url_for("superadmin"))
        else:
            flash('Anda tidak dapat mengakses halaman ini! Silahkan login kembali!', 'danger')
            return redirect(url_for('logout'))
    else:
        flash("Anda belum Login!", 'danger')
        return redirect(url_for("login"))
    
@app.route('/admin/patient/<int:taken_patient_id>', methods=["GET", "POST"])
def admin_patient(taken_patient_id):
    if "user_id" in session:
        role = session.get('role')
        if role == "admin":
            if request.method == 'POST':
                new_name = request.form['new_name']
                new_nik = request.form['new_nik']
                new_phone = request.form['new_phone']
                new_birthday = request.form['new_birthday']
                new_status = request.form['new_status']
                
                db.session.execute(
                    text(
                        "UPDATE patient SET username = :username, phone = :phone, nik = :nik, birthday = :birthday, status = :status WHERE id = :id"
                    ),
                    {
                        'username': new_name,
                        'phone': new_phone,
                        'nik': new_nik,
                        'birthday': new_birthday,
                        'status': new_status,
                        'id': taken_patient_id
                    }
                )
                db.session.commit()
                flash("Data pasien telah diubah!", 'success')
                return redirect(url_for('admin_patient', taken_patient_id=taken_patient_id))
            else:
                patient_data = db.session.execute(text("SELECT * FROM patient WHERE id = :taken_patient_id"),{'taken_patient_id': taken_patient_id}).fetchone()
                
                page = request.args.get('page', 1, type=int)
                per_page = 10
                offset = (page - 1) * per_page
                
                total =  db.session.execute(text("SELECT COUNT(*) FROM detection WHERE patient_id = :taken_patient_id"),{'taken_patient_id': taken_patient_id}).fetchone()[0]

                detection_data = db.session.execute(
                    text("""
                        SELECT d.detection_id, d.image, d.label, d.time, p.username AS patient_username, d.note, u.username AS doctor_username, d.confidence, p.nik
                        FROM detection d
                        JOIN patient p ON d.patient_id = p.id
                        JOIN user u ON d.user_id = u.user_id
                        WHERE d.patient_id = :patient_id AND d.status = 'aktif'
                        LIMIT :per_page OFFSET :offset
                    """),
                    {
                        'patient_id': taken_patient_id,
                        'per_page': per_page,
                        'offset': offset
                    }
                ).fetchall()
                
                detection_data_with_images = []
                for detection in detection_data:
                    filename = detection[1] 
                    this_image_url = get_signed_url(filename)
                    data_with_image = list(detection) + [this_image_url]
                    detection_data_with_images.append(data_with_image)
 
                return render_template("admin-patient.html", taken_patient_id=taken_patient_id, patient_data=patient_data, detection_data=detection_data_with_images, page=page, per_page=per_page, total=total)
        else:
            flash('Anda tidak dapat mengakses halaman ini! Silahkan login kembali!', 'danger')
            return redirect(url_for('logout'))
    else:
        flash("Anda belum Login!", 'danger')
        return redirect(url_for("login"))

###########################################(SUPERADMIN)#############################################################
#Done   
@app.route('/superadmin/add', methods=["GET", "POST"])
def register():
    if "user_id" in session:
        role = session.get('role')
        if role == "superadmin":
            if request.method == "POST":
                username = request.form["usernameRegForm"]
                phone = request.form["phoneRegForm"]
                email = request.form["emailRegForm"]
                role = request.form["roleRegForm"]
                password = request.form["passRegForm"]
                hashed_password = generate_password_hash(password)
                
                user = db.session.execute(text("SELECT * FROM user WHERE email = :email"),{'email': email}).fetchone()     
                if user:
                    flash('Email sudah digunakan! Silakan gunakan email lain!', 'danger')
                    return redirect(url_for('register'))
                else:
                    db.session.execute(
                        text(
                            "INSERT INTO user (username, phone, email, password, role, status, profile_picture) "
                            "VALUES (:username, :phone, :email, :password, :role, :status, :profile_picture)"
                        ),
                        {
                            'username': username,
                            'phone': phone,
                            'email': email,
                            'password': hashed_password,
                            'role': role,
                            'status': 'aktif',
                            'profile_picture': 'user-black.png'
                        }
                    )
                    db.session.commit()
                    
                    flash("Akun pengguna telah ditambahkan!", 'success')
                    return redirect(url_for("superadmin"))
            else:
                return render_template("superadmin-add.html")
        else:
            flash('Anda tidak dapat mengakses halaman ini! Silahkan login kembali!', 'danger')
            return redirect(url_for('logout'))
    else:
        flash("Anda belum Login!", 'danger')
        return redirect(url_for("login"))
    
#Done
@app.route('/superadmin')
def superadmin():
    if "user_id" in session:
        role = session.get('role')
        if role == "superadmin":
            user_id = session.get('user_id')
            user_data = db.session.execute(text("SELECT * FROM user WHERE user_id = :user_id"),{'user_id': user_id}).fetchone()
            file_name = user_data[8]
            image_url = get_signed_url(file_name)

            active_page = request.args.get('active_page', 1, type=int)
            inactive_page = request.args.get('inactive_page', 1, type=int)
            per_page = 10
            active_offset = (active_page - 1) * per_page
            inactive_offset = (inactive_page - 1) * per_page
            
            active_count_query = "SELECT COUNT(*) FROM user WHERE status = :status"
            active_users_query = """
                SELECT * FROM user
                WHERE status = :status
                LIMIT :limit OFFSET :offset
            """

            active_total = db.session.execute(
                text(active_count_query),
                {'status': 'aktif'}
            ).scalar()

            active_users = db.session.execute(
                text(active_users_query),
                {
                    'status': 'aktif',
                    'limit': per_page,
                    'offset': active_offset
                }
            ).fetchall()

            inactive_count_query = "SELECT COUNT(*) FROM user WHERE status = :status"
            inactive_users_query = """
                SELECT * FROM user
                WHERE status = :status
                LIMIT :limit OFFSET :offset
            """
            inactive_total = db.session.execute(
                text(inactive_count_query),
                {'status': 'non-aktif'}
            ).scalar()

            inactive_users = db.session.execute(
                text(inactive_users_query),
                {
                    'status': 'non-aktif',
                    'limit': per_page,
                    'offset': inactive_offset
                }
            ).fetchall()
            
            active_users_with_images = []
            for user in active_users:
                filename = user[8] 
                this_image_url = get_signed_url(filename)
                data_with_image = list(user) + [this_image_url]
                active_users_with_images.append(data_with_image)

            inactive_users_with_images = []
            for user in inactive_users:
                filename = user[8] 
                this_image_url = get_signed_url(filename)
                data_with_image = list(user) + [this_image_url]
                inactive_users_with_images.append(data_with_image)
                
            return render_template("superadmin.html", user_data=user_data, image_url=image_url,
                                   active_users=active_users_with_images, 
                                   inactive_users=inactive_users_with_images, 
                                   active_page=active_page, 
                                   inactive_page=inactive_page, 
                                   per_page=per_page, 
                                   active_total=active_total, 
                                   inactive_total=inactive_total)
        else:
            flash('Anda tidak dapat mengakses halaman ini! Silahkan login kembali!', 'danger')
            return redirect(url_for('logout'))
    else:
        flash("Anda belum Login!", 'danger')
        return redirect(url_for("login"))
    
#Done
@app.route('/superadmin/user/<int:taken_user_id>', methods=['GET', 'POST'])
def superadmin_user(taken_user_id):
    if "user_id" in session:
        role = session.get('role')
        if role == "superadmin":
            if request.method == 'POST':
                if 'new_password' in request.form:
                    password = request.form['new_password']
                    new_password = generate_password_hash(password)
                    
                    db.session.execute(text("UPDATE user SET password = :new_password WHERE user_id = :taken_user_id"),
                        {'new_password': new_password, 'taken_user_id': taken_user_id})
                    db.session.commit()
                    flash("Password telah diperbarui!", 'success')
                    return redirect(url_for('superadmin_user', taken_user_id=taken_user_id))
                else:
                    new_name = request.form['new_name']
                    new_phone = request.form['new_phone']
                    new_email = request.form['new_email']
                    new_status = request.form['new_status']
                    
                    db.session.execute(
                        text(
                            "UPDATE user SET username = :username, phone = :phone, email = :email, status = :status WHERE user_id = :user_id"
                        ),
                        {
                            'username': new_name,
                            'phone': new_phone,
                            'email': new_email,
                            'status': new_status,
                            'user_id': taken_user_id
                        }
                    )
                    db.session.commit()
                    
                    flash("Data pengguna telah diubah!", 'success')
                    return redirect(url_for('superadmin_user', taken_user_id=taken_user_id))
            else:
                user_data = db.session.execute(text("SELECT * FROM user WHERE user_id = :user_id"),{'user_id': taken_user_id}).fetchone()
                file_name = user_data[8]
                image_url = get_signed_url(file_name)

                active_page = request.args.get('active_page', 1, type=int)
                inactive_page = request.args.get('inactive_page', 1, type=int)
                per_page = 10
                active_offset = (active_page - 1) * per_page
                inactive_offset = (inactive_page - 1) * per_page
                
                active_count_query = "SELECT COUNT(*) FROM detection WHERE user_id = :user_id AND status = 'aktif'"
                active_detections_query = """
                    SELECT d.detection_id, d.image, d.label, d.time, p.username AS patient_username, d.note, u.username AS doctor_username, d.confidence, p.nik, d.status
                    FROM detection d
                    JOIN patient p ON d.patient_id = p.id
                    JOIN user u ON d.user_id = u.user_id
                    WHERE d.user_id = :user_id AND d.status = 'aktif'
                    LIMIT :limit OFFSET :offset
                """
                active_total = db.session.execute(
                    text(active_count_query),
                    {'user_id': taken_user_id}
                ).scalar()

                active_detections = db.session.execute(
                    text(active_detections_query),
                    {
                        'user_id': taken_user_id,
                        'limit': per_page,
                        'offset': active_offset
                    }
                ).fetchall()

                inactive_count_query = "SELECT COUNT(*) FROM detection WHERE user_id = :user_id AND status = 'non-aktif'"
                inactive_detections_query = """
                    SELECT d.detection_id, d.image, d.label, d.time, p.username AS patient_username, d.note, u.username AS doctor_username, d.confidence, p.nik, d.status
                    FROM detection d
                    JOIN patient p ON d.patient_id = p.id
                    JOIN user u ON d.user_id = u.user_id
                    WHERE d.user_id = :user_id AND d.status = 'non-aktif'
                    LIMIT :limit OFFSET :offset
                """
                inactive_total = db.session.execute(
                    text(inactive_count_query),
                    {'user_id': taken_user_id}
                ).scalar()

                inactive_detections = db.session.execute(
                    text(inactive_detections_query),
                    {
                        'user_id': taken_user_id,
                        'limit': per_page,
                        'offset': inactive_offset
                    }
                ).fetchall()

                active_detections_with_images = []
                for detection in active_detections:
                    filename = detection[1] 
                    this_image_url = get_signed_url(filename)
                    data_with_image = list(detection) + [this_image_url]
                    active_detections_with_images.append(data_with_image)

                inactive_detections_with_images = []
                for detection in inactive_detections:
                    filename = detection[1]
                    this_image_url = get_signed_url(filename)
                    data_with_image = list(detection) + [this_image_url]
                    inactive_detections_with_images.append(data_with_image)
                
                return render_template("superadmin-user.html", user_data=user_data, image_url=image_url,
                                       active_detections=active_detections_with_images, 
                                       inactive_detections=inactive_detections_with_images, 
                                       active_page=active_page, 
                                       inactive_page=inactive_page, 
                                       per_page=per_page, 
                                       active_total=active_total, 
                                       inactive_total=inactive_total, 
                                       taken_user_id=taken_user_id)
        else:
            flash('Anda tidak dapat mengakses halaman ini! Silahkan login kembali!', 'danger')
            return redirect(url_for('logout'))
    else:
        flash("Anda belum Login!", 'danger')
        return redirect(url_for("login"))
    
print("[INFO] Done :)")

def create_wsgi_app():
    return app

if __name__ == '__main__':
    # subprocess.Popen(['cloud_sql_proxy', f'-instances={os.environ["INSTANCE_CONNECTION_NAME"]}=tcp:3306', '-dir=/tmp/cloudsql'])
    # os.system(f'cloud_sql_proxy -instances={os.environ["INSTANCE_CONNECTION_NAME"]}=tcp:3306 -dir=/tmp/cloudsql')
    # app.run(debug=True, host='0.0.0.0')
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
