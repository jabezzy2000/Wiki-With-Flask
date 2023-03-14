from flask import Flask, render_template, request, abort, redirect, url_for, session, flash
from flaskr.backend import Backend


def make_endpoints(app):
    backend = Backend("dijproject_wiki_content")

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        page_links = [    {"name": "Home", "url": "/"},    {"name": "Pages", "url": "/pages"},    {"name": "About", "url": "/about"}, {"name": "Upload", "url": "/upload"},    {"name": "Login", "url": "/login"},    {"name": "Sign up", "url": "/signup"}]
        greeting = "Welcome to our Wiki page! We hope you love it here."    
        # backend.upload("hi dbz","dbz.html")   
        # backend.upload("hi tekken","tekken.html")  
        # backend.upload("hi mario","mario.html") 
        return render_template("main.html", greeting= greeting, page_links = page_links)

    # TODO(Project 1): Implement additional routes according to the project requirements.
    @app.route('/pages')
    def index():
        pages = backend.get_all_page_names()
        print(pages)
        return render_template('pages.html', pages = pages)

    @app.route('/pages/<pagename>')
    def pages(pagename):
        file_name = f"uploads/{pagename}"
        contents = backend.get_wiki_page(file_name)
        if contents is None:
            abort(404)
        return render_template(pagename+".html", contents=contents)

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if backend.sign_up(username, password):
                return 'Sign up successful!'
            else:
                return 'Username already taken!'
        else:
            return render_template('signup.html')
            


    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == 'POST':
            # Get username and password from form data
            username = request.form['username']
            password = request.form['password']

            # Check if user exists and if password matches
            if backend.sign_in(username, password):
                # Set session variable to store username
                session['username'] = username

                # Redirect to upload page
                return redirect(url_for('upload'))
            else:
                # Show error message on login page
                return render_template('login.html', error='Invalid username or password')

        # If GET request, render login page
        return render_template('login.html')

    @app.route("/logout", methods=['POST'])
    def logout():
        session.pop('username', None)
        return redirect('/login')


    @app.route('/upload',methods =['GET','POST'])
    def upload_file():
        if request.method == 'POST':
        # Check if a file was uploaded
            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files['file']
            # Check if the file is empty
            if file.filename == '':
                return redirect(request.url)
            # Upload the file to GCS
            backend.upload(filepath=file, filename=file.filename)
            return redirect('/')
    return render_template('upload.html')
        
    @app.route('/about')
    def about():
        # jabez = "jabez.HEIC"
        jabez_link = backend.get_image('jabez.HEIC')
        #add donald and ivan link when i get their pictures
        print(jabez_link)        
        return render_template("about.html",image1_link = jabez_link)
