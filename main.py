from flask import Flask, request, jsonify, json
from config import app, db
from models import Blog, Staff
from werkzeug.utils import secure_filename
import os
import cloudinary.uploader
import cloudinary.api
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


# Create blog
@app.route("/create-blog", methods=["POST"])
def create_blog():

    fe_title = request.form.get('title')
    fe_date = request.form.get('date')
    fe_img_url = request.form.get('imgUrl')
    fe_blog_url = request.form.get('blogUrl')
    fe_about_text = request.form.get('aboutText')

    try:
        blog = Blog(title=fe_title,
                    date=fe_date,
                    about_text=fe_about_text,
                    img=fe_img_url,
                    blog_url=fe_blog_url
                    )
        try:
            db.session.add(blog)
            db.session.commit()
            return jsonify({
                "Status": 200,
                "Message": "Blog Was Created Successfully"
            }), 200
        except Exception as e:
            return jsonify({
                "Status": 400 or 401,
                "Message": f" Couldn't Create Blog Something Went Wrong {str(e)} "
            }), 400

    except Exception as e:
        print("Not Able to Create Blog", e)
        return jsonify({
            "Status": 400 or 401,
            "Message": f" Couldn't Create Blog Something Went Wrong: {str(e)} "
        }), 400 or 401


# Getting blog
@app.route("/blogs", methods=["GET"])
def get_blogs():
    blogs = Blog.query.all()
    blogs_list = [b.to_json() for b in blogs]
    return jsonify({
        "Status": 200,
        "blogs": blogs_list
    })

# Delete Blog


@app.route("/delete-blog/<int:id>", methods=["DELETE"])
def delete_blog(id):
    blog = Blog.query.get(id)

    if not blog:
        print("No Blog Found")
        return jsonify({
            "Status": 404,
            "Message": "No Blog Was Founded, Couldn't Delete"
        }), 404

    try:
        db.session.delete(blog)
        db.session.commit()
        return jsonify({
            "Status": 200,
            "Message": "Blog Was Deleted Successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "Status": 500,
            "Message": f"An Error Occurred Couldn't Delete",
            "Code Message": f"Error Happened: {str(e)}"
        }), 500
# Staff
# Add Staff


@app.route("/add-staff", methods=["POST"])
def add_staff():
    fe_name = request.form.get("name")
    fe_job_title = request.form.get("jobTitle")
    img_file = request.files.get('imgFile')
    fe_about_me = request.form.get("aboutMe")
    # print(data)
    # print(img_file)

    try:
        img_as_file = secure_filename(img_file.filename)
        upload_result = cloudinary.uploader.upload(img_file)
        public_id_cloud = upload_result['public_id']
        new_img_url = upload_result['secure_url']

        staff = Staff(
            name=fe_name,
            job_title=fe_job_title,
            bio=fe_about_me,
            img=new_img_url,
            public_id=public_id_cloud
        )

        try:
            db.session.add(staff)
            db.session.commit()
            return jsonify({
                "Status": 200,
                "Message": "Staff Has Been Added Successfully"
            }), 200
        except Exception as e:
            return jsonify({
                "Status": 400,
                "Message": "Couldn't Add Staff Something Went Wrong Try Again ",
                "Code Error": f"Error: {str(e)}"
            }), 401
    except Exception as e:
        print(str(e))
        return jsonify({
            "Status": 400,
            "Message": "Something Went Wrong Couldn't Add Staff"
        }), 400

# Getting staff


@app.route("/staff", methods=["GET"])
def get_staff():
    staff = Staff.query.all()
    staff_list = [s.to_json() for s in staff]
    return jsonify({
        "Status": 200,
        "Message": "Getting Staff Went Successfully ",
        "Staff": staff_list
    }), 200
# Update Staff


@app.route("/update-staff/<int:id>", methods=["PATCH"])
def update_staff(id):
    staff = Staff.query.get(id)
    name = request.form.get('name')
    job_title = request.form.get('jobTitle')
    about = request.form.get('about')
    public_id = request.form.get('publicId')
    file = request.files.get("img")

    update_img = False
    if file:
        delete_old_img = cloudinary.api.delete_resources(
            public_id, resources_type="image", type="upload")

        new_img_uploader = cloudinary.uploader.upload(file)
        new_public_id = new_img_uploader['public_id']
        new_img_url = new_img_uploader['secure_url']
        update_img = True

    try:
        # updating
        staff.name = name
        staff.job_title = job_title
        staff.bio = about
        if update_img:
            staff.img = new_img_url
            staff.public_id = new_public_id
        try:
            db.session.commit()
            print('Updating Staff Worked')
            return jsonify({
                "Status": 200,
                "Message": "Staff Has Been Updated Successfully"
            }), 200
        except Exception as e:
            print(f"Error Happened During Updating: {e}")
            return jsonify({
                "Status": 400,
                "Message": "Couldn't Update Something Went Wrong"
            }), 400

    except Exception as e:
        print(f"Couldn't Retrieve Data Make Sure You Entered Valid Info {e}")
        return jsonify({
            "Status": 401,
            "Message": "Couldn't Update Make Sure You Entered Valid Info Or Try Again Later "
        }), 401
    # staff.name = data['name']
    # db.session.commit()


# Delete Staff


@ app.route("/delete-staff/<int:id>", methods=["DELETE"])
def delete_staff(id):
    staff = Staff.query.get(id)
    public_id = staff.public_id

    if not staff:
        print("No Staff Was Found")
        return jsonify({
            "Status": 403,
            "Message": "Couldn't Find Staff"
        }), 403
    try:
        delete_img_from_cloud = cloudinary.api.delete_resources(
            public_id, resources_type="image", type="upload")
        print(f"Deleting img from cloud {delete_img_from_cloud}")
        db.session.delete(staff)
        db.session.commit()
        return jsonify({
            "Status": 200,
            "Message": "Deleting Staff Went Successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "Status": 500,
            "Message": "Couldn't Deleted Something Went Wrong Try Again",
            "Code Message": f"Error Happened: {str(e)}"
        }), 500


username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')


@app.route('/login', methods=["POST"])
def log_in():

    data = request.form
    print(data)

    if request.method == "POST":
        fe_username = request.form['name']
        fe_password = request.form['password']
        if username == fe_username and password == fe_password:
            access_token = create_access_token(identity=username)

            print(access_token)
            return jsonify({
                "Status": 200,
                "Message": "Log-In Went Successfully",
                "Token": access_token
            }), 200
    else:
        print("wrong user")
        return jsonify({
            "Status": 401,
            "Message": "User Not Found"
        }), 401

    return jsonify({"Message": "Should go back to log-in "})


@app.route("/authenticated", methods=["GET"])
@jwt_required()
def authenticated():
    current_user = get_jwt_identity()
    if current_user:
        print(f"Current User is: {current_user}")
        return jsonify({
            "Status": 200,
            "Message": f"User is Authenticated: {current_user}"
        }), 200
    # logging the use out or returning bad request
    print('No user founded')
    return jsonify({
        "Status": 401,
        "Message": "No User Was Found "
    }), 401


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
