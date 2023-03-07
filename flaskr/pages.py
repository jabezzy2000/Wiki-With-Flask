from flask import render_template
from flaskr.backend import Backend


def make_endpoints(app):
    backend = Backend("dijproject_wiki_content")

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        page_links = [    {"name": "Home", "url": "/"},    {"name": "Pages", "url": "/index"},    {"name": "About", "url": "/about"},    {"name": "Login", "url": "/login"},    {"name": "Sign up", "url": "/signup"}]
        greeting = "Welcome to our Wiki page! We hope you love it here."        
        return render_template("main.html", greeting= greeting, page_links = page_links)

    # TODO(Project 1): Implement additional routes according to the project requirements.
    @app.route('/index')
    def index():
        pages = ['dbz', 'tekken']
        return render_template('index.html', pages = pages)

    @app.route('/tekken')
    def tekken():
        image_data = backend.get_image("Tekken2Box.jpg")
        return render_template('tekken.html', image_data=image_data, backend= backend)

    @app.route('/dbz')
    def dbz():
        return render_template('dbz.html')

    @app.route('/login')
    def login():
        return render_template("login.html")

    @app.route('/signup')
    def signup():
        return render_template("signup.html")

    @app.route('/about')
    def about():
        jabez = "jabez.HEIC"
        jabez_link = backend.get_image(jabez)
        #add donald and ivan link when i get their pictures
        print(jabez_link)        
        return render_template("about.html",image1_link = jabez_link)
