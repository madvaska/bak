#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import argparse

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-n', '--name', type=open)
    return parser


if __name__ == '__main__':
    print ("Версия 0.04")
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    print (namespace)


    outf = open('out.csv','w')
    for line in namespace.name:
        print(';;;;;;'+line.rstrip()+';0000000000000000;;;')
        outf.write(';;;;;;'+line.rstrip()+";0000000000000000;;;\n")
    namespace.name.close()
    outf.close()
