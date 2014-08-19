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
A very VERY basic svg parser. This handles a single
path and draws it. Based on code from
Cairo's tutorials.
'''

import pyparsing

class SVGPathParser(object):
    def __init__(self):
        self.tokens = []

    def parse(self, path_string):
        dot = pyparsing.Literal(".")
        comma = pyparsing.Literal(",").suppress()
        floater = pyparsing.Combine(pyparsing.Optional("-") + pyparsing.Word(pyparsing.nums) + dot + pyparsing.Word(pyparsing.nums))
        ## Unremark to have numbers be floats rather than strings.
        #floater.setParseAction(lambda toks:float(toks[0]))
        couple = floater + comma + floater
        M_command = "M" + pyparsing.Group(couple)
        m_command = "m" + pyparsing.Group(couple)
        C_command = "C" + pyparsing.Group(couple + couple + couple)
        c_command = "c" + pyparsing.Group(couple + couple + couple)
        L_command = "L" + pyparsing.Group(couple)
        l_command = "l" + pyparsing.Group(couple)
        V_command = "V" + pyparsing.Group(floater)
        v_command = "v" + pyparsing.Group(floater)
        Z_command = "Z"
        z_command = "z"
        svgcommand = M_command | m_command | C_command | c_command | L_command | l_command | V_command | v_command | Z_command | z_command
        phrase = pyparsing.OneOrMore(pyparsing.Group(svgcommand)) 

        self.tokens = phrase.parseString(path_string)

    def render(self, context, scale):
        for l in self.tokens:
            if len(l) == 2:
                command, couples = l
                c = map(float, couples.asList())
            else:
                command = l[0]
            
            if command == 'm':
                context.rel_move_to(c[0] * scale, c[1] * scale)
            elif command == 'M':
                context.move_to(c[0] * scale, c[1] * scale)
            elif command == 'c':
                context.rel_curve_to(c[0] * scale, c[1] * scale,
                                     c[2] * scale, c[3] * scale,
                                     c[4] * scale, c[5] * scale)
            elif command == 'C':
                context.curve_to(c[0] * scale, c[1] * scale,
                                 c[2] * scale, c[3] * scale,
                                 c[4] * scale, c[5] * scale)
            elif command == 'l':
                context.rel_line_to(c[0] * scale, c[1] * scale)
            elif command == 'L':
                context.line_to(c[0] * scale, c[1] * scale)
            elif command == 'v':
                context.rel_line_to(0, c[0] * scale)
            elif command == 'V':
                x, y = context.get_current_point()
                context.line_to(x, c[0] * scale)
            elif command == 'z':
                context.close_path()
            elif command == 'Z':
                context.close_path()
            else:
                print 'unknown command', command
