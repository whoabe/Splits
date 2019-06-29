import os
import config
from flask import Flask, render_template, request
from models.base_model import db

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'splits_web')

app = Flask('SPLITS', root_path=web_dir)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

'''shows the form to upload receipt image'''
@app.route('/upload', methods=["GET"])
def upload_form():
    return render_template('users/user_edit.html')
    # render some html page

'''uploads receipt image to amazon? s3? google?'''
@app.route("/", methods=["POST"])
def upload_file():

	# A 
    #  We check the request.files object for a user_file key. (user_file is the name of the file input on our form). If it’s not there, we return an error message.

    if "user_file" not in request.files:
        flash("No file in request.files")
        return render_template('users/user_edit.html')

	# B
    # If the key is in the object, we save it in a variable called file.
    file    = request.files["user_file"]

    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

	# C.
    # We check the filename attribute on the object and if it’s empty, it means the user sumbmitted an empty form, so we return an error message.
    if file.filename == "":
        flash("Please select a file")
        return render_template('users/user_edit.html', user = current_user)

	# D.
    # Finally we check that there is a file and that it has an allowed filetype (this is what the allowed_file function does, you can check it out in the flask docs).

    if file and 'image' in file.content_type:
        file.filename = secure_filename(file.filename)
        # secure_filename = Pass it a filename and it will return a secure version of it. This filename can then safely be stored on a regular file system and passed to os.path.join(). The filename returned is an ASCII only string for maximum portability.
        # output = upload_file_to_s3(file, Config.S3_BUCKET)
        upload_file_to_s3(file, Config.S3_BUCKET)
        user = current_user
        user.profile_image = str(current_user.id) + "-" + file.filename
        if user.save():
            flash("profile image updated")
            return render_template('users/user_edit.html', user = current_user)
        # return str(output)


    else:
        flash('wrong content type')
        return render_template('users/user_edit.html', user = current_user)

'''need another view function that sends the image to google vision AI has method=POST'''