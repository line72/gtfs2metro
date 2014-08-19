gtfs2metro
==========

== About

gtfs2metro is very basic software to read GTFS (General Transit Feed
Specification) data and generate Metro Line maps.

This software was writen by Marcus Dillavou <line72@line72.net> as
part of the Code For Birmingham (http://www.codeforbirmingham.org)
which is the Birmingham, AL brigade of Code For America. This software
is tailored specifically towards BJCTA (Birmingham-Jefferson County
Transit Authority) GTFS data, but could be modified to work with any
GTFS data.

GTFS data is used by transit agencies as a common storage platform for
route and stop data. This is typically used by trip planning
applications such as Google Transit or Open Trip Planner. More
information about GTFS can be found at
http://www.gtfs-data-exchange.org or
https://developers.google.com/transit/gtfs/

== Running

=== Prerequsites

Before running, you will need to install two dependencies
 * python-gtfs
 * python-cairo

On Mac OSX, if you are using mac ports, you can install the following:

 $ port install py-gtfs py-cairo

On Linux, cairo should be part of your base install. To install gtfs
library, run
 $ pip install transitfeed

This hasn't been test under Windows, but would likely work by
installing python and the two dependencies

== Running

You will first need to download GTFS data. This has only been tested
with BJCTA's GTFS data:
http://www.gtfs-data-exchange.com/agency/birmingham-jefferson-county-transit-authority/

Make a new directory to store the output

 $ mkdir output

Now run the script

 $ python gtfs2metro.py /path/to/GTFS.zip output/

Under Mac OSX, if you installed the gtfs and cairo through ports, make
sure you are running the correct version of python, NOT the system
version:

 $ /opt/local/bin/python2.7 gtfs2metro.py /path/to/GTFS.zip output/

You will now have a bunch of separate .svg files in the output
directory, one for each line.

== Copyright

gtfs2metro is Copyright 2014 Marcus Dillavou <line72@line72.net> and
is released under the MIT license. Please see LICENSE for more information.