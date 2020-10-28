import datetime, _io, os, signal, subprocess, time

_CORRECT = u"\u2714"
_WRONG = u"\u2718"

def slot(a, b, x, n=10):
    dx = (b - a) / n
    i = 1
    c = a + dx
    while c <= x:
        i += 1
        c += dx
    return i

def run(cmd, args=[], stdin=None, timeout=30):
    start = datetime.datetime.now()
    process = subprocess.Popen([cmd] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    if stdin:
        process.stdin.write(bytes(stdin, "utf-8"))
    process.stdin.close()
    while process.poll() is None:
        time.sleep(0.1)
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            os.kill(process.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            return (False, "__TIMEOUT__")
    stdout = process.stdout.read().decode("utf-8")
    process.stdout.close()
    return (process.returncode == 0, stdout)

def python3(name, args=[], stdin=None, timeout=30, outfile=None, f=None):
    cmd = "python3 %s" %(name)
    if len(args) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in args])
    stdintext = None
    if stdin:
        if isinstance(stdin, _io.TextIOWrapper):
            cmd = "%s < %s" %(cmd, stdin.name)
            stdintext = stdin.read()
        else:
            cmd = "echo '%s' | %s" %(stdin, cmd)
            stdintext = stdin
    print(cmd, end=" ")
    success, stdout = run("python3", [name] + args, stdintext, timeout)
    if outfile:
        print("> %s" %(outfile), end=" ")
        fh = open(outfile, "w")
        fh.write(stdout)
        fh.close()
    try:
        if f:
            f(stdout)
    except AssertionError as e:
        print(_WRONG)
        raise e
    print(_CORRECT)
    return success, stdout

def function(name, f=None):
    print(name, end=" ")
    try:
        if f:
            f()
    except AssertionError as e:
        print(_WRONG)
        raise e
    print(_CORRECT)

def pycodestyle(filename):
    print("pycodestyle %s " %(filename), end="")
    success, stdout = run("pycodestyle", [filename])
    if not success:
        print(_WRONG)
        raise AssertionError("\n" + stdout)
    print(_CORRECT)
    return success, stdout

def ant(opts=[]):
    cmd = "ant"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    print("%s " %(cmd), end="")
    success, stdout = run("ant", opts)
    if not success:
        print(_WRONG)
        raise AssertionError("\n" + stdout)
    print(_CORRECT)
    return success, stdout

def javac(name, opts=[]):
    cmd = "javac"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + name
    print("%s " %(cmd), end="")
    success, stdout = run("javac", opts + [name])
    if not success:
        print(_WRONG)
        raise AssertionError("\n" + stdout)
    print(_CORRECT)
    return success, stdout

def jmm(name, opts=[], f=None):
    cmd = "./bin/j--"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + name
    print("%s " %(cmd), end="")
    success, stdout = run("./bin/j--", opts + [name])
    try:
        if f:
            f(stdout)
    except AssertionError as e:
        print(_WRONG)
        raise e
    print(_CORRECT)
    return success, stdout

def javaccjmm(name, opts=[], f=None):
    cmd = "./bin/javaccj--"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + name
    print("%s " %(cmd), end="")
    success, stdout = run("./bin/javaccj--", opts + [name])
    try:
        if f:
            f(stdout)
    except AssertionError as e:
        print(_WRONG)
        raise e
    print(_CORRECT)
    return success, stdout

def java(name, opts=[], args=[], f=None):
    cmd = "java"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + name
    if len(args) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in args])
    print("%s " %(cmd), end="")
    success, stdout = run("java", opts + [name] + args)
    try:
        if f:
            f(stdout)
    except AssertionError as e:
        print(_WRONG)
        raise e
    print(_CORRECT)
    return success, stdout

def spim(name):
    cmd = "spim -f " + name
    print("%s " %(cmd), end="")
    success, stdout = run("spim", ["-f", name])
    try:
        if f:
            f(stdout)
    except AssertionError as e:
        print(_WRONG)
        raise e
    print(_CORRECT)
    return success, stdout
