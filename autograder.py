import _io, os, psutil, subprocess

_CORRECT = u"\u2714"
_WRONG = u"\u2718"

# Runs ant with the given options (opts), and returns 1 on success and 0 on failure.
def ant(opts=[]):
    cmd = "ant"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    print("%s " %(cmd), end="")
    if not os.path.isfile("build.xml"):
        print(_WRONG)
        print("build.xml not found")
        return 0
    success, stdout, stderr = _run("ant", opts)
    if not success or stderr != "":
        print(_WRONG)
        print(stderr)
        return 0
    if "SUCCESSFUL" not in stdout:
        print(_WRONG)
        print(stdout)
        return 0
    print(_CORRECT)
    return 1

# Returns 1 if the file with the given name exists and 0 otherwise.
def fileCheck(name):
    print("%s exists?" %(name), end=" ")
    if os.path.exists(name):
        print(_CORRECT)
        return 1
    print(_WRONG)
    return 0

# Used to test a function. The doc argument is a string describing the function that is being 
# tested. The testing function (tester) calls the function and compares its output with the 
# expected value. If they don't match, tester raises an AssertionError, in which case this function 
# returns 0. Otherwise, this function returns 1. 
def function(doc, tester):
    print(doc, end=" ")
    try:
        tester()
    except AssertionError as e:
        print(_WRONG)
        print(e)
        return 0
    print(_CORRECT)
    return 1

# Compiles the iota program with the given name (name), options (opts), and testing function 
# (tester). If not successful, returns 0. Otherwise, does the following: if tester is specified, 
# calls it with the stdout and stderr strings from the iota compiler; and returns 1 if tester does 
# not result in an assertion error, and 0 if it does. 
def iota(name, opts=[], tester=None):
    cmd = "./bin/iota"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + name
    print("%s " %(cmd), end="")
    if not os.path.isfile(name):
        print(_WRONG)
        print("%s not found" %(name))
        return 0
    success, stdout, stderr = _run("./bin/iota", opts + [name])
    if not success or stderr != "":
        print(_WRONG)
        print(stderr)
        return 0
    try:
        if tester:
            tester(stdout.strip(), stderr.strip())
    except AssertionError as e:
        print(_WRONG)
        print(e)
        return 0
    print(_CORRECT)
    return 1

# Runs the java program with the given name (name), command-line inputs (args), testing function 
# (tester), and timeout value (timeout) in seconds. If not successful, returns 0. Otherwise, does 
# the following: if outfile is specified, if tester is specified, calls it with the stdout and 
# stderr strings from the java program; and returns 1 if tester does not result in an assertion 
# error, and 0 if it does.
def java(name, opts=[], args=[], tester=None, timeout=30):
    cmd = "java"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + name
    if len(args) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in args])
    print("%s " %(cmd), end="")
    success, stdout, stderr = _run("java", opts + [name] + args, None, timeout)
    if not success or stderr != "":
        print(_WRONG)
        print(stderr)
        return 0
    try:
        if tester:
            tester(stdout.strip(), stderr.strip())
    except AssertionError as e:
        print(_WRONG)
        print(e)
        return 0
    print(_CORRECT)
    return 1

# Compiles the java program with the given name (name) and options (opts), and returns 1 on 
# success and 0 otherwise.
def javac(name, opts=[]):
    cmd = "javac"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + name
    print("%s " %(cmd), end="")
    success, stdout, stderr = _run("javac", opts + [name])
    if not success or stderr != "":
        print(_WRONG)
        print(stderr)
        return 0
    print(_CORRECT)
    return 1

# Compiles the j-- program with the given name (name), options (opts), and testing function 
# (tester). Calls the tester, if one is specified, with the stdout and stderr strings from the
# j-- compiler; and returns 0 if the tester results in an assertion error. Otherwise, returns 1.
def jmm(name, opts=[], tester=None):
    cmd = "./bin/j--"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + name
    print("%s " %(cmd), end="")
    if not os.path.isfile(name):
        print(_WRONG)
        print("%s not found" %(name))
        return 0
    success, stdout, stderr = _run("./bin/j--", opts + [name])
    try:
        if tester:
            tester(stdout.strip(), stderr.strip())
    except AssertionError as e:
        print(_WRONG)
        print(e)
        return 0
    print(_CORRECT)
    return 1

# Compiles the j-- program with the given name (name), options (opts), and testing function 
# (tester). If not successful, returns 0. Otherwise, does the following: if tester is specified, 
# calls it with the stdout and stderr strings from the j-- compiler with javacc frontend; and 
# returns 1 if tester does not result in an assertion error, and 0 if it does. 
def javaccjmm(name, opts=[], tester=None):
    cmd = "./bin/javaccj--"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + name
    print("%s " %(cmd), end="")
    if not os.path.isfile(name):
        print(_WRONG)
        print("%s not found" %(name))
        return 0
    success, stdout, stderr = _run("./bin/javaccj--", opts + [name])
    if not success or stderr != "":
        print(_WRONG)
        print(stderr)
        return 0
    try:
        if tester:
            tester(stdout.strip(), stderr.strip())
    except AssertionError as e:
        print(_WRONG)
        print(e)
        return 0
    print(_CORRECT)
    return 1

# Runs the python program with the given name (name), command-line inputs (args), standard input 
# (input), output file name (outfile), testing function (tester), and timeout value (timeout) in 
# seconds. If not successful, returns 0. Otherwise, does the following: if outfile is specified,  
# writes the stdout string to that file; if tester is specified, calls it with the stdout and 
# stderr strings from the python program; and returns 1 if tester does not result in an assertion 
# error, and 0 if it does.
def python3(name, args=[], input=None, outfile=None, tester=None, timeout=30):
    cmd = "python3 %s" %(name)
    if len(args) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in args])
    inputtext = None
    if input:
        if isinstance(input, _io.TextIOWrapper):
            cmd = "%s < %s" %(cmd, input.name)
            inputtext = input.read()
        else:
            cmd = "echo -e '%s' | %s" %(input, cmd)
            inputtext = input
    print(cmd, end=" ")
    success, stdout, stderr = _run("python3", [name] + args, inputtext, timeout)
    if not success or stderr != "":
        print(_WRONG)
        print(stderr)
        return 0
    if outfile:
        print("> %s" %(outfile), end=" ")
        fh = open(outfile, "w")
        fh.write(stdout)
        fh.close()
    try:
        if tester:
            tester(stdout.strip(), stderr.strip())
    except AssertionError as e:
        print(_WRONG)
        print(e)
        return 0
    print(_CORRECT)
    return 1

# Runs the command with the given name (cmd), command-line inputs (args), standard input (input), 
# and timeout value (timeout) in seconds. If successful, returns the tuple (True, stdout string, 
# stderr string). If the command times out, returns the tuple (False, "", timeout string). If the 
# command fails, returns the tuple (False, "", error string).
def _run(cmd, args=[], input=None, timeout=30):
    try:
        proc = subprocess.Popen([cmd] + args,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    except:
        return (False, "", "Error: unable to run command '%s'" %(cmd))
    try:
        stdout, stderr = proc.communicate(bytes(input, "utf-8") if input else None, timeout)
    except subprocess.TimeoutExpired as e:
        for child in psutil.Process(proc.pid).children(recursive=True):
            child.kill()
        proc.kill()           
        return (False, "", "Error: %ss timeout expired" %(timeout))
    return (True, stdout.decode("utf-8"), stderr.decode("utf-8"))
