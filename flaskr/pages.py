from flask import render_template, request, abort
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
            return render_template("signup.html")


    @app.route("/login", methods=["GET", "POST"])
    def login():
            return render_template("login.html")



    @app.route('/upload',methods =['GET','POST'])
    def upload():
        if request.method == 'POST':
        # Get the uploaded file from the HTML form
            uploaded_file = request.files['html_file']
            print(request.files.keys())
            # Save the uploaded file to a temporary location
            filepath = '/tmp/' + uploaded_file.filename
            uploaded_file.save(filepath)

            # Call the "upload()" method to save the file to Google Cloud Storage
            backend.upload(filepath, uploaded_file.filename)

            # Render a success message
            message = f'{uploaded_file.filename} has been uploaded successfully!'
            return render_template('upload.html', message=message)
        else:
            # Render the upload form
            return render_template('upload.html')

    @app.route('/about')
    def about():
        # jabez = "jabez.HEIC"
        jabez_link = backend.get_image('jabez.HEIC')
        #add donald and ivan link when i get their pictures
        print(jabez_link)        
        return render_template("about.html",image1_link = jabez_link)
