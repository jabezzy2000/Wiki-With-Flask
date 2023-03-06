from flask import render_template


def make_endpoints(app):

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
