#! /usr/bin/env python

from lindenmayer import LSystem, Rule, StochasticRule
from draw import TurtleDrawer

import math, sys

def flower():
    drawer = TurtleDrawer(4,1,16)

    lsystem = LSystem('X[B]C',
                      {
                          'X': 'DDDDDDDD',
                          'D': 'DFF',
                          'B': '[F+B--F+B]-B',
                          'C': 'L--L--L--L',
                          'L': 'S-S-S-S',
                          'S': '[A]-[A]-[A]-[A]-[A]-[A]',
                          'A': StochasticRule(((0.7, 'DDD[+D][-D]D'), (0.2, 'DDD[+D][--F]F'), (0.1, 'DDD[--D]F')))
                      })
    description = lsystem.evaluate(9)
    description2 = lsystem.evaluate(9)

    # uncomment if you want to see the string you're drawing
    # print(description)

    drawer.draw(description, offset=(200, -400))
    drawer.draw(description2, offset=(-200, -400), clear=False)
    drawer.done()

def tumbleweed():
    '''
    Draws a tumbleweed
    :return: A single image of a randomly generated tumbleweed
    '''
    drawer = TurtleDrawer(5, 1, 10)
    lsystem = LSystem('FFFX',
        {
            'F': StochasticRule(((0.65,'F-F[+F]F[-F]'),(0.3, 'F[+FF]F[--F]'), (0.05,'FF[++F]FF[-F]'))),
            'X': 'F-F[++F]F[-F]'
        })
    description = lsystem.evaluate(5)

    # uncomment if you want to see the string you're drawing
    #print(description)

    drawer.draw(description, offset=(-100, 0))
    drawer.done()

def rye():
    drawer = TurtleDrawer(10,1,20)
    lsystem = LSystem('XSK',
                      {
                          'X' : StochasticRule(((0.97, 'XF'), (0.01, 'X[-S]F'), (0.01, 'X[+S]F'), (0.01, 'X[+S][-S]F'))),
                          'S' : 'SF[-SF]SF',
                          'K' : 'F[+K][-K]FK'
                      })
    description = lsystem.evaluate(4)

    drawer.draw(description, offset=(0, -400))
    drawer.done()

if __name__ == '__main__':
    try:
        if sys.argv[1] == '1':
            flower()
        elif sys.argv[1] == '2':
            tumbleweed()
        elif sys.argv[1] == '3':
            rye()
    except IndexError:
        print('Use any of the following numerical arguments to see one of the following plants:\n'
              '1: Dandelion\n'
              '2: Tumbleweed\n'
              '3: Rye')
