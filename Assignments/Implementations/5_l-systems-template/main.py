#! /usr/bin/env python

from lindenmayer import LSystem, Rule, StochasticRule
from draw import TurtleDrawer

import math

def main():
    drawer = TurtleDrawer(5, 1, 25)

    lsystem = LSystem('[++++++X][------F][+++X][---F][+X][-F][+++++X][-----F][------T]F',
        {
            'X': 'X[+X]X[+X]',
            'F': 'F[-F]F[-F]',
            'T': 'T'
        })
    description = lsystem.evaluate(6)

    # uncomment if you want to see the string you're drawing
    #print(description)

    drawer.draw(description, offset=(0, -400))
    drawer.done()

if __name__ == '__main__':
    main()
