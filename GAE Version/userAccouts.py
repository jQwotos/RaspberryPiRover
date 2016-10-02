import webapp2, jinja2, os, hashlib, hmac, string, random

from google.appengine.ext import db

# os.path.dirname(__file__) is the current location of the file
# os.path.join joins the current location with templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

'''
SQL     -   GQL
Tables  -   Entities
'''

secret = "potatoesareawesome!"

def hash_str(s):
    return hmac.new(secret, s).hexdigest()

def make_secure_val(password, salt, username):
    return "%s|%s" % (username, hash_str("%s%s%s" % (password, salt, username)))

def check_secure_val(x):
    username = x.split("|")[0]
    enteredPasswordHash = x.split("|")[1]
    actualPasswordHash = db.GqlQuery("SELECT passwordHash FROM User WHERE username=%s" % username)
    if enteredPasswordHash == actualPasswordHash:
        return True


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class User(db.Model):
    username = db.StringProperty(required = True)
    passwordHash = db.StringProperty(required = True)
    salt = db.StringProperty(required = True)
    dateCreated = db.DateTimeProperty(auto_now_add = True)

class Post(db.Model):
    text = db.StringProperty(required = True)
    date = db.DateTimeProperty(auto_now_add = True)

# MainPage is a child of Handler, therefore it has all the functions and variables of Handler
class MainPage(Handler):
    def renderFront(self):


        strVisits = make_secure_val(str(visits))

        self.response.headers.add_header('Set-Cookie', 'visits=%s' % strVisits)
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY date DESC")
        self.render("index.html", posts = posts, visits = visits)

    def get(self):
        self.renderFront()

    def post(self):
        text = self.request.get('text')
        post = Post(text = text)
        post.put()

        self.redirect('/')

class Login(Handler):
    def get(self):

    def post(self):

class Register(Handler):
    def get(self):

    def post(self):
        secret = Secret.secret
        username = self.request.get('username')
        password = self.request.get('password')
        currentUsers = db.GqlQuery("SELECT username FROM User")
        if usename not in currentUsers:
            salt = "".join(random.choice(string.ascii_uppercase + string.digits) for x in len(20))
            passwordHash = make_secure_val(password, salt, username)
            user = User(username = username, passwordHash = passwordHash)
            user.put()

class SecretGeny:
    def __init__(self):
        self.secret = "potatoeslovetobecomehashedbyhmac!*^!"

Secret = SecretGeny()

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/user', UserAccounts),
], debug=True)
