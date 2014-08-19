# Copyright (c) 2014 Marcus Dillavou <line72@line72.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
Some special types of external connections,
such as rail stations, airports, bus stations, etc
These show up as connections similar to the connections
with other Metro lines.
'''

from SVGPathParser import SVGPathParser

class Drawable(object):
    def __init__(self, context):
        self.context = context

    def draw(self, size):
        pass

class Airport(Drawable):
    def draw(self, size):
        self.context.set_source_rgb(0.0, 0.0, 0.0)
        
        svg = SVGPathParser()
        svg.parse('m -4.6183,-33.468802 c 0.0184,-5.8 8.7688,-5.8 8.7688,0.1624 v 24.3687986 l 34.1,20.5064024 v 9.0064 L 4.3065,9.4007985 V 27.607199 l 7.8496,6.1504 v 7.1064 l -12.1064,-3.756 l -12.1128,3.756 v -7.1064 l 7.7752,-6.1504 V 9.4007985 L -38.2495,20.573599 v -9.0064 L -4.6183,-8.9384034 V -33.468802 z')
        svg.render(self.context, (size * 2) / 100.0)
        self.context.fill()

        # put a rectangle around it
        self.context.move_to(-size, size)
        self.context.line_to(size, size)
        self.context.line_to(size, -size)
        self.context.line_to(-size, -size)
        self.context.close_path()
        self.context.stroke()

class TrainStation(Drawable):
    def draw(self, size):
        print 'Drawing Train Station'

        # self.context.set_source_rgb(0.0, 0.0, 0.0)
        # svg = SVGPathParser()
        # svg.parse('M -0.31899362,47.989002 H 18.568786 l 13.79253,18.90124 h 11.12047 l -19.28,-27.05167 c 6.43128,-0.96855 12.83599,-7.22991 12.83599,-14.86623 v -55.889809 c 0,-7.87209 -7.09929,-15.115462 -16.73965,-15.115462 l -20.53779962,-0.0262 l -20.69572038,0.0262 c -9.64036,0 -16.72655,7.243372 -16.72655,15.115462 v 55.889809 c 0,7.63632 6.39162,13.89768 12.82326,14.86623 l -19.26545,27.05167 h 11.10701 l 13.79253,-18.90124 h 18.88814038 z')
        # svg.render(self.context, (size * 2) / 100.0)
        # self.context.fill()

        # self.context.set_source_rgb(1.0, 1.0, 1.0)
        # svg = SVGPathParser()
        # svg.parse('M 20.481866,31.692502 c 4.04774,0 7.33506,-3.06501 7.33506,-6.86388 c 0,-3.78469 -3.28732,-6.85042 -7.33506,-6.85042 c -4.04702,0 -7.33506,3.06573 -7.33506,6.85042 c -3e-4,3.79887 3.28804,6.86388 7.33506,6.86388 z')
        # svg.render(self.context, (size * 2) / 100.0)
        # self.context.fill()

        # # put a rectangle around it
        # self.context.move_to(-size, size)
        # self.context.line_to(size, size)
        # self.context.line_to(size, -size)
        # self.context.line_to(-size, -size)
        # self.context.close_path()
        # self.context.stroke()

class BusStation(Drawable):
    def draw(self, size):
        pass


class Connection(object):
    connections = {'SBO1': (TrainStation,), # central station
                   '20OU24': (Airport,), # airport
                   }
