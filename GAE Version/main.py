import webapp2, jinja2, os
import RPi.GPIO as pi

from google.appengine.ext import db

# os.path.dirname(__file__) is the current location of the file
# os.path.join joins the current location with templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

GPIO.setmode(GPI.BOARD)

# [right motor one pin, left motor two pin]
motorsINT = [21, 22]

motors = {
    "right":motorsINT[0],
    "left":motorsINT[1]
}

GPIO.setup(motorsINT, GPIO.OUT)

# possible directions, left right forward backwards
class Move:
    def __init__(self):
        directions = {
            "left": self.left,
            "right": self.right,
            "forward": self.forward,
            "backward": self.backward,
            "stop": self.stop,
        }
    @classmethod
    def towards(self, direction):
        GPIO.output(motorsINT, GPIO.LOW)
        for key, value in self.directions.items():
            if direction == key:
                self.directions[key]()

    def setHigh(self, motor):
        GPIO.output(motor, GPIO.HIGH)
    def stop:
        GPIO.output(motorsINT, GPIO.LOW)
    def left:
        self.setHigh(motors.get("right"))
    def right:
        self.setHigh(motors.get("left"))
    def forward:
        self.setHigh(motorsINT)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

# MainPage is a child of Handler, therefore it has all the functions and variables of Handler
class MainPage(Handler):
    def renderFront(self):
        self.render("index.html")

    def get(self):
        self.renderFront()

    def post(self):
        direction = self.request.get('direction')
        Move.towards(direction)

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

GPIO.cleanup()
