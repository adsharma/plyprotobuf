#!/usr/bin/env python3
"""
Unnest nested messages. Need to run multiple times if multiply nested
"""

import sys
import re
import plyproto.parser
import plyproto.model as m
import argparse
import traceback
import os.path

from collections import OrderedDict

class UnnestVisitor(m.Visitor):
    content=""
    replacement=""
    moved = []
    # We need OrderedSet here really
    parents = OrderedDict()
    prepend = {}

    def __init__(self):
        super().__init__()

    def visit_MessageDefinition(self, obj):
        '''New message, refactor name, w.r.t. path'''
        if self.verbose > 3:
            print("Message, [%s] lex=%s body=|%s|\n" % (obj.name, obj.lexspan, obj.body))

        if obj.parent != self.outer_most:
            start, end = obj.lexspan
            # Do not unnest doubly nested objects.
            # Just run this tool twice
            if obj.parent not in self.moved:
                pstart = obj.parent.lexspan[0]
                if pstart not in self.prepend:
                    self.prepend[pstart] = ""
                self.prepend[pstart] += self.content[start-1:end+1] + "\n"
                self.parents[pstart] = obj.parent
            self.moved.append(obj)
        
        return True

    def visit_Proto(self, obj):
        self.outer_most = obj
        self.outer_lexspan = obj.lexspan
        return True
       
# Main executable code
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Log statements formating string converter.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i','--in-place',  help='Overwrites provided file with the new content', required=False, default=False, dest='inplace')
    parser.add_argument('-o','--outdir',    help='Output directory', required=False, default="", dest='outdir')
    parser.add_argument('-e','--echo',      help='Writes output to the standard output', required=False, default=False)
    parser.add_argument('-v','--verbose',   help='Writes output to the standard output', required=False, default=0, type=int)
    parser.add_argument('file')
    args = parser.parse_args()
    
    # Load the file and instantiate the visitor object.
    p = plyproto.parser.ProtobufAnalyzer()
    if args.verbose>0:
        print(" [-] Processing file: %s" % (args.file))
    
    # Start the parsing.
    try:
        v = UnnestVisitor()
        v.offset = 0
        v.verbose = args.verbose
        with open(args.file, 'r') as content_file:
            v.content = content_file.read()
        
        tree = p.parse_file(args.file)
        tree.accept(v)
      
        out = ""
        last = 0

        parents = list(v.parents.values())
        if not parents:
            sys.exit(0)
        # Consume everything up to the first object being unnested
        pstart = parents[0].lexspan[0] - 1
        out += v.content[last:pstart]
        last = pstart
        for obj in v.moved:
            start, end = obj.lexspan
            if len(parents):
                pstart, pend = parents[0].lexspan
                if pstart < start:
                    out += v.prepend[parents[0].lexspan[0]]
                    parents = parents[1:]
            if start < last:
                continue
            out += v.content[last:start-1]
            last = end
        out += v.content[end:]
        v.content = out 
        # If here, probably no exception occurred.
        if args.echo:
            print(v.content)
        if args.outdir != None and len(args.outdir)>0 and v.statementsChanged>0:
            outfile = args.outdir + '/' + os.path.basename(args.file).capitalize()
            with open(outfile, 'w') as f:
                f.write(v.content)
        if args.inplace and v.statementsChanged>0:
            with open(args.file, 'w') as f:
                f.write(v.content)
                
        if args.verbose>0:
            print(" [-] Processing finished, changed=%d" % v.statementsChanged)
    except Exception as e:
        print("    Error occurred! file[%s]" % (args.file), e)
        if args.verbose>1:
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
        sys.exit(1)
        
