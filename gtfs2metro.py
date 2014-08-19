#!/usr/bin/env python

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
This is a super basic script
that takes a GTFS data file
(www.gtfs-data-exchange.org)
and generates a metro style map 
for each line. The output is in
SVG format.

This could work for any GTFS data file
but has some things hardcoded around
the BJCTA (Birmingham-Jefferson Country
Transit Authority) gtfs data.
'''


import sys
import os
import random
import math

import transitfeed
import cairo

from connections import Connection
from landmarks import Landmark

def go(gtfs_zip, output_dir):
    gtfs = transitfeed.loader.Loader(gtfs_zip)
    schedule = gtfs.Load()

    routes = {}
    colors = {}

    # make sure random is the same
    random.seed(0)

    for trip in schedule.GetTripList():
        # !mwd - for now we are ignoring
        #  the possibility of variations
        #  in the same route. For now, if
        #  we have seen a route, assume this
        #  one is the same
        if trip.route_id in routes:
            continue

        #!mwd - sure wish the data used the direciton flag!!
        #  not this crappy hack
        # only look at outbound routes
        if trip.GetStopTimes()[0].stop.stop_name != 'Central Station' and \
           'ob' not in trip.shape_id and 'OB' not in trip.shape_id:
            continue

        routes[trip.route_id] = []
        colors[trip.route_id] = (random.random(), random.random(), random.random())

        for stop in trip.GetStopTimes():
            # if stop.arrival_secs != None: # only time stops
            #     routes[trip.route_id].append(stop.stop)
            routes[trip.route_id].append(stop.stop)

    # build our graph
    for route_id, stops in routes.iteritems():
        route = schedule.GetRoute(route_id)

        color = colors[route_id]

        surface = cairo.SVGSurface('%s.svg' % os.path.join(output_dir, route.route_short_name), 20000, 1000)
        c = cairo.Context(surface)

        # make a big logo
        c.save()
        c.set_source_rgb(*color)
        c.arc(125, 125, 60, 0, math.pi * 2)
        c.fill()

        c.set_source_rgb(1.0, 1.0, 1.0)
        c.set_font_size(48)
        x_bearing, y_bearing, width, height = c.text_extents(route.route_short_name)[:4]
        c.move_to(125 - width / 2 - x_bearing, 125 - height / 2 - y_bearing)
        c.show_text(route.route_short_name)
        c.restore()

        prev_stop = None
        x = 250
        y = 250
        size = 15
        dx = 150
        for j, stop in enumerate(stops):
            connections = []
            for t in stop.GetTrips():
                if t.route_id == route_id or t.route_id in connections:
                    continue

                connections.append(t.route_id)

            if j < len(stops) - 1:
                c.save()
                c.set_source_rgb(*color)
                c.move_to(x, y)
                c.line_to(x + dx, y)
                c.set_line_width(5.0)
                c.stroke()
                c.restore()

            if len(connections) == 0:
                c.save()
                c.set_source_rgb(*color)
                c.arc(x, y, size, 0, math.pi * 2)
                c.fill()
                c.restore()
            else:
                # this is a connection, do a white
                #  circle with black outline
                c.save()
                c.set_source_rgb(0.0, 0.0, 0.0)
                c.arc(x, y, size, 0, math.pi * 2)
                c.set_line_width(5.0)
                c.stroke_preserve()
                c.set_source_rgb(1.0, 1.0, 1.0)
                c.fill()
                c.restore()

            c.save()
            c.set_source_rgb(0.0, 0.0, 0.0)
            # do some text
            c.move_to(x, y - size - 5)
            c.rotate(-math.pi / 4.0)
            c.show_text('%s (%s)' % (stop.stop_name, stop.stop_id))
            #c.show_text('%s' % stop.stop_name)
            c.restore()

            # our landmarks
            if stop.stop_id in Landmark.landmarks:
                cx = x + 25
                for l in Landmark.landmarks[stop.stop_id]:
                    c.save()
                    c.set_source_rgb(74/255., 25/255., 25/255.,)
                    c.move_to(cx-8, y - size)
                    c.rotate(-math.pi / 4.0)

                    x_bearing, y_bearing, width, height = c.text_extents(l)[:4]
                    # make a brown square
                    c.rel_line_to(0, -height - 2)
                    c.rel_line_to(width+16, 0)
                    c.rel_line_to(0, height + 10)
                    c.rel_line_to(-(width+16), 0)
                    c.close_path()
                    c.fill()
                    c.restore()

                    # do the text
                    c.save()
                    c.set_source_rgb(1.0, 1.0, 1.0)
                    c.move_to(cx, y - size - 5)
                    c.rotate(-math.pi / 4.0)
                    c.show_text(l)
                    c.restore()

                    cx += 25
                    

            # our connections
            cx = x
            cy = y+50
            for i, conn in enumerate(connections):
                r = schedule.GetRoute(conn)
                try:
                    color2 = colors[r.route_id]
                except Exception, e:
                    print 'No color for', r.route_id
                    color2 = (1.0, 0.0, 0.0)
                # should be the trips color
                c.save()
                c.set_source_rgb(*color2)
                c.arc(cx, cy, size, 0, math.pi * 2)
                c.fill()
                
                c.set_source_rgb(1.0, 1.0, 1.0)

                x_bearing, y_bearing, width, height = c.text_extents(r.route_short_name)[:4]
                c.move_to(cx - width / 2 - x_bearing, cy - height / 2 - y_bearing)
                c.show_text(r.route_short_name)
                c.restore()

                cx += size * 2 + 5

                if i % 3 == 2 or i == len(connections) - 1:
                    cx = x
                    cy += size * 2 + 5

            if stop.stop_id in Connection.connections:
                for d0 in Connection.connections[stop.stop_id]:
                    c.save()
                    c.translate(x, cy)
                    c.move_to(0, 0)
                    d = d0(c)
                    d.draw(size)
                    c.restore()

                    cy += size * 2 + 5

            x += dx
            prev_stop = stop
    
        surface.finish()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >> sys.stderr, 'Usage: %s gtfs.zip output_directory' % sys.argv[0]
        sys.exit(1)

    go(sys.argv[1], sys.argv[2])
