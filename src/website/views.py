from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_required, current_user
from .models import User, File
import boto3
import uuid
import os
from . import db
from . import get_bucket
from dotenv import load_dotenv
from qdrant.vectorDatabase import VectorDatabase
from qdrant.llm import Query
import json


load_dotenv()


ALLOWED_EXTENSIONS = {'application/pdf', 'md'}

def allowed_file(file):
    return file.content_type in ALLOWED_EXTENSIONS


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        uploaded_file = request.files['file-to-save']
        if not allowed_file(uploaded_file):
            flash('File type not allowed', category='error')
            return(redirect(url_for('views.home')))
        
        new_filename = uuid.uuid4().hex + '.' + uploaded_file.filename.lower()
        
        bucket_name = 'makerag'
        s3 = get_bucket()
        s3.Bucket(bucket_name).upload_fileobj(uploaded_file, new_filename)

        file = File(original_filename=uploaded_file.filename, filename=new_filename,
            bucket=bucket_name, user_id=current_user.id, region="us-east-2")
        
        db.session.add(file)
        db.session.commit()

        return(redirect(url_for('views.home')))
    
    
    files = File.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, files=files, llm_response=session.get('llm_response'))

    


@views.route('/createdb', methods=['GET','POST'])
@login_required
def create_vector_database():
    files = File.query.filter_by(user_id=current_user.id).all()
    file_ids = [file.filename for file in files]
    vdb = VectorDatabase()
    vdb.createDatabase(current_user.id, file_ids)

    return(redirect(url_for('views.home')))

@views.route('/querydb', methods=['GET','POST'])
@login_required
def query_vector_db():

    query_text = request.form.get('query_text')

    vdb = VectorDatabase()
    querier = Query()

    context = vdb.searchDatabase(current_user.id, query_text)
    llm_response = querier.query(query_text, context)
    session['llm_response'] = llm_response
    
    return(redirect(url_for('views.home')))

@views.route('/delete-file', methods=['POST'])
def delete_file():  
    file_json = json.loads(request.data)
    file_id = file_json.get('id')
    file = File.query.get(file_id)
    if file:
        if file.user_id == current_user.id:
            db.session.delete(file)
            db.session.commit()
            bucket_name = 'makerag'
            s3 = get_bucket()
            s3.Object(bucket_name, file.filename).delete()

    return jsonify({})

@views.errorhandler(413)
def request_entity_too_large(error):
    flash('File too large', category='error')
    return(redirect(url_for('views.home')))
   