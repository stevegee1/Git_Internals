#Hash-object command
"""
It reads a file, compute its hash as an object
either storing it in the repository(if -w flag is passed) or just printing its hash
"""


import argparse, sys, os, configparser,hashlib


argpaser= argparse.ArgumentParser(description="content tracker")
argsubparser= argpaser.add_subparsers(title="Commands", dest="command")
argsubparser.required=True
parser_name = argsubparser.add_parser("hash-object", help="Computer object ID and optionally creates a blob from a file")
parser_name.add_argument("-t",metavar="type", dest="type", choices=["blob"],default="blob", help="Specify the type")
parser_name.add_argument("path",help="Read object from <file>")



def main(argv=sys.argv[1:]):
    args= argpaser.parse_args(argv)
    match args.command:
       case "hash-object": cmd_hash_objects(args)
       
def cmd_hash_objects(args):
    print(args.path)
    print(args.type.encode())
    with open(args.path, "rb") as fd:
       sha=object_hash(fd, args.type.encode(), None)
       print(sha)

class GitObject (object):

    def __init__(self, data=None):
        if data != None:
            self.deserialize(data)
        else:
            self.init()

    def serialize(self, repo):
        """This function MUST be implemented by subclasses.

It must read the object's contents from self.data, a byte string, and do
whatever it takes to convert it into a meaningful representation.  What exactly that means depend on each subclass."""
        raise Exception("Unimplemented!")

    def deserialize(self, data):
        raise Exception("Unimplemented!")

    def init(self):
        pass # Just do nothing. This is a reasonable default!

class GitBlob(GitObject):
    fmt=b'blob'
    def serialize(self):
        return self.blobdata
    def deserialize(self, data):
        self.blobdata=data
     
def object_write(obj, repo=None):
    if type(obj)==None:
        raise Exception("This implementation is fucking hilarious!")
    #serialize object data
    data= obj.serialize()
    # Add header
    result= obj.fmt + b' ' + str(len(data)).encode() + b'\x00' + data
    #compute hash
    sha = hashlib.sha1(result).hexdigest()
    return sha


def object_hash(fd, fmt,repo):
   
    data= fd.read()
    print(data)

    match fmt:
        case b'blob' : obj=GitBlob(data)
        case _: raise Exception("Unknown type %s!" %fmt)
    print(obj)
    return(object_write(obj, repo))

