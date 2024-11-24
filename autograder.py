import _io, os, psutil, subprocess

CORRECT = u"\u2714"
WRONG = u"\u2718"

def run(cmd, args=[], input=None, timeout=30):
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

def python3(name, args=[], input=None, timeout=30, outfile=None, tester=None):
    cmd = "python3 %s" %(name)
    if len(args) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in args])
    inputtext = None
    if input:
        if isinstance(input, _io.TextIOWrapper):
            cmd = "%s < %s" %(cmd, input.name)
            inputtext = input.read()
        else:
            cmd = "echo '%s' | %s" %(input, cmd)
            inputtext = input
    print(cmd, end=" ")
    success, stdout, stderr = run("python3", [name] + args, inputtext, timeout)
    if not success:
        print(WRONG)
        raise AssertionError("\n" + stderr)
    if outfile:
        print("> %s" %(outfile), end=" ")
        fh = open(outfile, "w")
        fh.write(stdout)
        fh.close()
    try:
        if tester:
            tester(stdout, stderr)
    except AssertionError as e:
        print(WRONG)
        raise e
    print(CORRECT)

def javac(filename, opts=[], timeout=30):
    cmd = "javac"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + filename
    print("%s " %(cmd), end="")
    if not os.path.isfile(filename):
        print(WRONG)
        raise AssertionError("\nError: cannot find file '%s'" %(filename))
    success, stdout, stderr = run("javac", opts + [filename], None, timeout)
    if not success or stderr != "":
        print(WRONG)
        raise AssertionError("\n" + stderr)
    print(CORRECT)

def java(filename, opts=[], args=[], tester=None, timeout=30):
    cmd = "java"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + filename
    if len(args) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in args])
    print("%s " %(cmd), end="")
    if not os.path.isfile("%s.class" %(filename)):
        print(WRONG)
        raise AssertionError("\nError: cannot find file '%s.class'" %(filename))
    success, stdout, stderr = run("java", opts + [filename] + args, None, timeout)
    if not success:
        print(WRONG)
        raise AssertionError("\n" + stderr)
    try:
        if tester:
            tester(stdout, stderr)
    except AssertionError as e:
        print(WRONG)
        raise e
    print(CORRECT)

def ant(opts=[], timeout=30):
    cmd = "ant"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    print("%s " %(cmd), end="")
    if not os.path.isfile("build.xml"):
        print(WRONG)
        raise AssertionError("\nError: cannot find file 'build.xml'")
    success, stdout, stderr = run("ant", opts, None, timeout)
    if not success:
        print(WRONG)
        raise AssertionError("\n" + stderr)
    if "SUCCESSFUL" not in stdout:
        print(WRONG)
        raise AssertionError("\n" + stdout)
    print(CORRECT)

def iota(filename, opts=[], tester=None, timeout=30):
    cmd = "iota"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + filename
    print("%s " %(cmd), end="")
    if not os.path.isfile(filename):
        print(WRONG)
        raise AssertionError("\nError: cannot find file '%s'" %(filename))
    success, stdout, stderr = run("./bin/iota", opts + [filename], None, timeout)
    if not success:
        print(WRONG)
        raise AssertionError("\n" + stderr)
    try:
        if tester:
            tester(stdout, stderr)
    except AssertionError as e:
        print(WRONG)
        raise e
    print(CORRECT)

def jmm(filename, opts=[], tester=None, timeout=30):
    cmd = "j--"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + filename
    print("%s " %(cmd), end="")
    if not os.path.isfile(filename):
        print(WRONG)
        raise AssertionError("\nError: cannot find file '%s'" %(filename))
    success, stdout, stderr = run("./bin/j--", opts + [filename], None, timeout)
    if not success:
        print(WRONG)
        raise AssertionError("\n" + stderr)
    try:
        if tester:
            tester(stdout, stderr)
    except AssertionError as e:
        print(WRONG)
        raise e
    print(CORRECT)

def javaccjmm(filename, opts=[], tester=None, timeout=30):
    cmd = "javaccj--"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + filename
    print("%s " %(cmd), end="")
    if not os.path.isfile(filename):
        print(WRONG)
        raise AssertionError("\nError: cannot find file '%s'" %(filename))
    success, stdout, stderr = run("./bin/javaccj--", opts + [filename], None, timeout)
    if not success:
        print(WRONG)
        raise AssertionError("\n" + stderr)
    try:
        if tester:
            tester(stdout, stderr)
    except AssertionError as e:
        print(WRONG)
        raise e
    print(CORRECT)

def function(name, tester=None):
    print(name, end=" ")
    try:
        if tester:
            tester()
    except AssertionError as e:
        print(WRONG)
        raise e
    print(CORRECT)

def slot(a, b, x, n=10):
    dx = (b - a) / n
    i = 1
    c = a + dx
    while c <= x:
        i += 1
        c += dx
    return i
    
