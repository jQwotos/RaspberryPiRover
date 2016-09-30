from flask import Flask
import RPi.GPIO as GPIO
import jinja2
app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)

templateLocation = 'templates'

template_dir = os.path.join(os.path.dirname(__file__), templateLocation)
jinja_env = jina2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

pins = [1, 2]

class MainPage(View):
    def render(self, template, **kw):
        return render_template(template, **kw)

@app.route("/")
def mainPage():
    pass

class Controls:
    @staticmethod
    def stop(self):

    @staticmethod
    def turnLeft(self):

    @staticmethod
    def turnRight(self):

    @staticmethod
    def moveForward(self):

    @staticmethod
    def moveBackward(self):

if __name == "__main__":
    app.run()
    app.add_url_rule('/', view_func=MainPage)
