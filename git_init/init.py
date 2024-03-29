
import argparse, sys, os, configparser


argpaser= argparse.ArgumentParser(description="content tracker")
argsubparser= argpaser.add_subparsers(title="Commands", dest="command")
argsubparser.required=True
parser_name = argsubparser.add_parser("init", help="initialize a new,empty repository")
parser_name.add_argument("path",metavar="directory", nargs="?", default=".", help="Where to create the repository")



def main(argv=sys.argv[1:]):
    args= argpaser.parse_args(argv)
    match args.command:
       case "init": cmd_init(args)

def cmd_init(args):
    repo_create(args.path)

class GitRepository(object):
    worktree= None
    gitdir= None
    conf=None

    def __init__(self,path, force=False):
        self.worktree= path
        self.gitdir= os.path.join(path,".git")

        if not(force or os.path.isdir(self.gitdir)):
            raise Exception("Not a git repository %s" % path)

        #read configuration file in .git/config
        self.conf= configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")
        if not force:
            vers= int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception("Unsupported repositoryformatversion %s" % vers)

def repo_path(repo, *path):
        return os.path.join(repo.gitdir, *path)

def repo_file(repo, *path,mkdir=False):
        if repo_dir(repo, *path[:-1], mkdir=mkdir):
            return repo_path(repo,*path)
def repo_dir(repo, *path, mkdir=False):
    path = repo_path(repo, *path)

    if os.path.exists(path):
        if(os.path.isdir(path)):
            return path
        else:
            raise Exception("Not a directory %s" % path)
    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None

def repo_create(path):
    repo = GitRepository(path,True)
    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception("%s is not a directory" % path)
        if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
          raise Exception("%s is not empty" % path)

    else:
        os.makedirs(repo.worktree)
    
    assert repo_dir(repo, "branches", mkdir= True)
    assert repo_dir(repo, "refs","heads", mkdir= True)
    assert repo_dir(repo, "objects", mkdir= True)
    assert repo_dir(repo, "refs","tags", mkdir= True)

    #.git/description
    with open(repo_file(repo, "description"), "w") as f:
        f.write("Unnamed repository:edit this file 'description' to name the repository. \n")

    #.git/HEAD
    with open(repo_file(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")
    with open(repo_file(repo, "config"), "w") as f:
        config= repo_default_config()
        config.write(f)
    return repo

def repo_default_config():
    ret= configparser.ConfigParser()
    ret.add_section("core")
    ret.set("core", "repositoryformatversion", "0")
    ret.set("core", "filemode", "false")
    ret.set("core","bare","false")
    return ret

#check for the presence of .git directory
def repo_find(path=".", required = True):
    path= os.path.realpath(path)
    if os.path.isdir(os.path.join(path,".git")):
        return GitRepository(path)

    parent = os.path.realpath(os.path.join(path,".."))
    if parent ==path:
        if required:
            raise Exception("No git directory")
        else:
            return None
    return repo_find(parent, required)
    


