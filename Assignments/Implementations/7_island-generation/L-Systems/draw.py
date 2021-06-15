import turtle

class TurtleDrawer:
    def __init__(self, length, width, angle):
        self.length = length
        self.width = width
        self.angle = angle
        self.actions = {}

        self.add_action('F', self.forward)
        self.add_action('f', self.forward_no_draw)
        self.add_action('+', self.turn_ccw)
        self.add_action('-', self.turn_cw)
        self.add_action('[', self.push_state)
        self.add_action(']', self.pop_state)

    def add_action(self, symbol, action):
        self.actions[symbol] = action

    def init_turtle(self, offset, animate, clear):
        if clear:
            turtle.reset()

        if not animate:
            turtle.tracer(0, 0)
        else:
            turtle.delay(0)

        turtle.penup()
        turtle.setpos(offset)
        turtle.setheading(90)
        turtle.pendown()
        turtle.hideturtle()

    def draw(self, description, offset = (0, 0), animate = False, clear = True):
        self.init_turtle(offset, animate, clear)

        self.states = []

        for symbol in description:
            if not symbol in self.actions:
                continue
            self.actions[symbol]()

        if not animate:
            turtle.update()

    def done(self):
        turtle.done()

    def forward(self):
        turtle.width(self.width)
        turtle.forward(self.length)

    def forward_no_draw(self):
        turtle.penup()
        self.forward()
        turtle.pendown()

    def turn_ccw(self):
        turtle.left(self.angle)

    def turn_cw(self):
        turtle.right(self.angle)

    def push_state(self):
        self.states.append((turtle.position(), turtle.heading()))

    def pop_state(self):
        pos, heading = self.states.pop()
        turtle.penup()
        turtle.setposition(pos)
        turtle.setheading(heading)
        turtle.pendown()
