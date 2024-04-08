from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, File
import boto3
import uuid
import os
from . import db
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')

ALLOWED_EXTENSIONS = {'application/pdf', 'md'}

def allowed_file(file):
    return file.content_type in ALLOWED_EXTENSIONS


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        uploaded_file = request.files['file-to-save']
        if not allowed_file(uploaded_file):
            flash('File type not allowed', category='error')
            return(redirect(url_for('views.home')))
        
        new_filename = uuid.uuid4().hex + '.' + uploaded_file.filename.lower()
        
        bucket_name = 'makerag'
        s3 = boto3.resource('s3', 
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        s3.Bucket(bucket_name).upload_fileobj(uploaded_file, new_filename)

        file = File(original_filename=uploaded_file.filename, filename=new_filename,
            bucket=bucket_name, user_id=current_user.id, region="us-east-2")
        
        db.session.add(file)
        db.session.commit()

        return(redirect(url_for('views.home')))
    
    files = File.query.filter_by(user_id=current_user.id)
    return render_template("home.html", user=current_user, files=files)