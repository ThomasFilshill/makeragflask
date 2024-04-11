from flask import Blueprint, render_template, request, redirect, url_for, flash, session
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


load_dotenv()


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
        s3 = get_bucket()
        s3.Bucket(bucket_name).upload_fileobj(uploaded_file, new_filename)

        file = File(original_filename=uploaded_file.filename, filename=new_filename,
            bucket=bucket_name, user_id=current_user.id, region="us-east-2")
        
        db.session.add(file)
        db.session.commit()

        return(redirect(url_for('views.home')))
    
    files = File.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, files=files)

@views.route('/createdb', methods=['GET','POST'])
@login_required
def create_vector_database():
    vdb = VectorDatabase()
    vdb.createDatabase(current_user.id)

    return(redirect(url_for('views.home')))

@views.route('/querydb', methods=['GET','POST'])
@login_required
def query_vector_db():

    query_text = request.form.get('query_text')

    vdb = VectorDatabase()
    querier = Query()

    context = vdb.searchDatabase(current_user.id, query_text)
    llm_response = querier.query(query_text, context)
    print(llm_response)


    files = File.query.filter_by(user_id=current_user.id).all() ### REMOVE THIS!!

    return render_template("home.html", user=current_user, files=files, llm_response=llm_response)