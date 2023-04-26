from flask import render_template, request, abort, redirect, session, url_for
from bs4 import BeautifulSoup
from flaskr.backend import Backend
import requests
import os
import logging


def make_endpoints(app):
    backend = Backend("dijproject_wiki_content")

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    def slice_string(value, length):
        return value[:length]

    app.jinja_env.filters['slice_string'] = slice_string

    @app.route("/")
    def home(message=""):
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        page_links = [{
            "name": "Home",
            "url": "/"
        }, {
            "name": "Pages",
            "url": "/pages"
        }, {
            "name": "About",
            "url": "/about"
        }, {
            "name": "Upload",
            "url": "/upload"
        }, {
            "name": "Login",
            "url": "/login"
        }, {
            "name": "Sign up",
            "url": "/signup"
        }, {
            "name": "Logout",
            "url": "/logout"
        }]
        greeting = "Welcome to our Wiki page! We hope you love it here."
        # backend.upload("hi dbz","dbz.html")
        # backend.upload("hi tekken","tekken.html")
        # backend.upload("hi mario","mario.html")
        username = session.get("username")  # Get the username from the session if the user is logged in
        return render_template("main.html",
                               messsage = message,
                               greeting=greeting,
                               page_links=page_links,
                               username = username)

    # TODO(Project 1): Implement additional routes according to the project requirements.
    @app.route('/pages')
    def index():
        pages = backend.get_all_page_names()
        return render_template('pages.html', pages=pages)

    @app.route('/pages/<pagename>', methods = ['GET', 'POST'])
    def pages(pagename):
        file_name = f"{pagename}"
        contents = backend.get_wiki_page(file_name)
        if contents is None:
            abort(404)

        css_styles = '''
        <style>
    #comments-section {
        font-family: Arial, sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 10px;
        background-color: #f8f8f8;
    }

    #comments-section h3,
    #comments-section h4 {
        margin-bottom: 10px;
    }

    #comments-section ul {
        list-style-type: none;
        padding: 0;
    }

    #comments-section li {
        border-bottom: 1px solid #eee;
        padding: 8px 0;
    }

    #comments-section li:last-child {
        border-bottom: none;
    }

    #comments-section textarea {
        width: 100%;
        padding: 5px;
        resize: none;
        font-family: inherit;
        font-size: 14px;
        border: 1px solid #ccc;
    }

    #comments-section input[type="submit"] {
        font-family: inherit;
        font-size: 14px;
        padding: 5px 10px;
        background-color: #007bff;
        color: #fff;
        border: none;
        border-radius: 3px;
        cursor: pointer;
    }

    #comments-section input[type="submit"]:hover {
        background-color: #0056b3;
    }
</style>
        '''
        head_close_pos = contents.find('</head>')

        contents = contents[:head_close_pos] + css_styles + contents[head_close_pos:]
        # create a new template file in the templates directory
        template_path = os.path.join(app.root_path, 'templates',
                                     f"{pagename}.html")
        with open(template_path, 'w') as f:
            comments_section = '''
                <div id="comments-section">
                    <h3>Comments</h3>
                    {% if comments %}
                        <ul>
                            {% for comment in comments %}
                                <li><b>{{ comment.username }}:</b> {{ comment.comment }}</li>
                            {% endfor %}
                        </ul>
                    {% else %}
                        <p>No comments yet.</p>
                    {% endif %}

                    {% if 'username' in session %}
                        <h4>Add a comment</h4>
                        <form method="POST">
                            <textarea name="comment" rows="4" cols="50" required></textarea><br>
                            <input type="submit" value="Submit">
                        </form>
                    {% else %}
                        <p>You must <a href="{{ url_for('login') }}">log in</a> to post a comment.</p>
                    {% endif %}
                </div>
            '''
            f.write(contents + comments_section)
        
        if request.method == 'POST':
            if 'username' in session:
                comment = request.form['comment']
                backend.add_comment(pagename, session['username'], comment)
                return redirect(url_for('pages', pagename=pagename))
            else:
                return redirect(url_for('login'))

        comments = backend.get_comments(pagename)
        return render_template(f"{pagename}.html", comments=comments)
       

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            confirm_password = request.form["confirm_password"]
            if password != confirm_password:
                return "Passwords do not match"
            if backend.sign_up(username, password):
                return login(username,password)
            else:
                return "Username already exists"
        else:
            return render_template("signup.html")

    @app.route("/login", methods=["GET", "POST"])
    def login(user = None, passw = None):
        if request.method == "POST":
            if user and passw:
                username = user
                password = passw
            else:
                username = request.form["username"]
                password = request.form["password"]
            if backend.sign_in(username, password):
                page_links = [{ "name": "Home", "url": "/"  }, {    "name": "Pages",    "url": "/pages" }, {  "name": "About",   "url": "/about" }, 
                {"name": "Upload", "url": "/upload" }, { "name": "Logout","url": "/logout"}]
                session['logged_in'] = True
                session['username'] = username
                return render_template("main.html", message="Logged in successfully!", page_links = page_links, username = username)
            else:
                return render_template("login.html", error="Incorrect username or password")
        else:
            return render_template("login.html")


    # If GET request, render login page

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     'uploads')
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        if request.method == 'POST':
            # Check if a file was uploaded
            if 'html_file' not in request.files:
                return redirect(request.url)
            file = request.files['html_file']
            filename = request.form['file_name']
            category = request.form['category']
            author = request.form['author']

            # Save the file to a temporary directory on the server
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Rename the file and update the file variable
            new_filename = f"{filename}_{category}_{author}.html"
            os.rename(filepath, os.path.join(UPLOAD_FOLDER, new_filename))
            filepath = os.path.join(UPLOAD_FOLDER, new_filename)

            # Upload the file to GCS
            success, message = backend.upload(filepath=filepath,
                                              filename=new_filename)
            if success:
                return render_template('upload.html', message=message)
            else:
                return render_template('upload.html', message=message)

        return render_template('upload.html')

    @app.route('/about')
    def about():
        # jabez = "jabez.HEIC"
        jabez_link = backend.get_image('jabez.HEIC')
        #add donald and ivan link when i get their pictures
        print(jabez_link)
        return render_template("about.html", image1_link=jabez_link)

    @app.route('/search')
    def search():
        query = request.args.get('q')
        category = request.args.get('category')
        author = request.args.get('author')
        rating = request.args.get('rating')
        matches = {}
        contents = {}
        all_pages = backend.get_all_page_names()

        if not query:
            if not category and not author:
                return redirect(url_for('index'))
            else:
                for page in all_pages:
                    split_page = page.lower().split("_")
                    if category.lower() in split_page or author.lower() in split_page:
                        matches[page.split("_")[0]] = page
                        contents[page.split("_")[0]] = backend.get_wiki_page(page).split()[0:4]
            
                
        for page in all_pages:
        # Retrieve the content of the page
            page_content = backend.get_wiki_page(page)
            print(f"page content for {page_content}")

        # Check if the query is in the page title or content
            if query in page or query.lower() in page or query.upper() in page \
           or query in page_content or query.lower() in page_content or query.upper() in page_content:
                matches[page.split("_")[0]] = page
                contents[page.split("_")[0]] = backend.get_wiki_page(page)

        
        # logging.debug("matches: %s", matches)

        if category:
            copy_match = matches.copy()
            for key in copy_match:
                logging.debug("key: %s", key)
                logging.debug("split match: %s", copy_match[key].split("_"))
                if category not in copy_match[key].split("_"):
                    del matches[key]
                    del contents[key]
        if author:
            copy_match = matches.copy()
            logging.debug("author matches: %s", matches)
            for key in copy_match:
                if author.lower() not in copy_match[key].lower().split("_")[-1].split("."):
                    logging.debug(f"Author: {author}, key: {key} not in {copy_match[key]}: {key in copy_match[key].lower().split('_')}")

                    del matches[key]
                    del contents[key]

        # logging.debug("filtered matches: %s", matches)
        logging.debug("contents: %s", contents)

        return render_template('search_results.html', query=query, matches=matches,category = category, author = author, contents = contents)
        
    @app.route('/logout')
    def logout():
        # Clear the user session
        session.clear()
        # Redirect to the home page
        return redirect(url_for('login'))
    