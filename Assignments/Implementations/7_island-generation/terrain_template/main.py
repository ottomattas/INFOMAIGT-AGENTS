#! /usr/bin/env python

from rendering import Renderer

if __name__ == '__main__':
    app = Renderer()

    # call your generation function here!

    app.render_heightmap(heights, 1)
    app.run()
