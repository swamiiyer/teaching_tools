import _io, os, subprocess

_CORRECT = u"\u2714"
_WRONG = u"\u2718"

def run(cmd, args=[], stdin=None, timeout=30):
    try:
        cp = subprocess.run([cmd] + args,
                            stdin= bytes(stdin, "utf-8") if stdin else None,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    except subprocess.TimeoutExpired as e:
        return (False, "Error: %ss timeout expired" %(timeout), "")
    except:
        return (False, "Error: unable to run command '%s'" %(cmd), "")
    return (cp.returncode == 0, cp.stdout.decode("utf-8"), cp.stderr.decode("utf-8"))

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
    success, stdout, stderr = run("python3", [name] + args, stdintext, timeout)
    if not success:
        print(_WRONG)
        raise AssertionError("\n" + stderr + "\n" + stdout)
    if outfile:
        print("> %s" %(outfile), end=" ")
        fh = open(outfile, "w")
        fh.write(stdout)
        fh.close()
    try:
        if f:
            f(stdout, stderr)
    except AssertionError as e:
        print(_WRONG)
        raise e
    print(_CORRECT)
    return success, stdout, stderr

def pycodestyle(filename, timeout=30):
    print("pycodestyle %s " %(filename), end="")
    success, stdout, stderr = run("pycodestyle", [filename], None, timeout)
    if not success:
        print(_WRONG)
        raise AssertionError("\n" + stderr + "\n" + stdout)
    print(_CORRECT)
    return success, stdout, stderr

def javac(name, opts=[], timeout=30):
    cmd = "javac"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + name
    print("%s " %(cmd), end="")
    success, stdout, stderr = run("javac", opts + [name], None, timeout)
    if not success:
        print(_WRONG)
        raise AssertionError("\n" + stderr + "\n" + stdout)
    print(_CORRECT)
    return success, stdout, stderr

def java(name, opts=[], args=[], f=None, timeout=30):
    cmd = "java"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + name
    if len(args) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in args])
    print("%s " %(cmd), end="")
    success, stdout, stderr = run("java", opts + [name] + args, None, timeout)
    try:
        if f:
            f(stdout, stderr)
    except AssertionError as e:
        print(_WRONG)
        raise e
    print(_CORRECT)
    return success, stdout, stderr

def ant(opts=[], timeout=30):
    cmd = "ant"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    print("%s " %(cmd), end="")
    success, stdout, stderr = run("ant", opts, None, timeout)
    if not success:
        print(_WRONG)
        raise AssertionError("\n" + stderr + "\n" + stdout)
    print(_CORRECT)
    return success, stdout, stderr

def jmm(name, opts=[], f=None, timeout=30):
    cmd = "j--"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + name
    print("%s " %(cmd), end="")
    success, stdout, stderr = run("./bin/j--", opts + [name], None, timeout)
    try:
        if f:
            f(stdout, stderr)
    except AssertionError as e:
        print(_WRONG)
        raise e
    print(_CORRECT)
    return success, stdout, stderr

def javaccjmm(name, opts=[], f=None, timeout=30):
    cmd = "javaccj--"
    if len(opts) > 0:
        cmd += " " + " ".join(["'%s'" %(v) if " " in v else v for v in opts])
    cmd += " " + name
    print("%s " %(cmd), end="")
    success, stdout, stderr = run("./bin/javaccj--", opts + [name], None, timeout)
    try:
        if f:
            f(stdout, stderr)
    except AssertionError as e:
        print(_WRONG)
        raise e
    print(_CORRECT)
    return success, stdout, stderr

def spim(name, timeout=30, f=None):
    cmd = "spim -f " + name
    print("%s " %(cmd), end="")
    if not os.path.isfile(name):
        print(_WRONG)
        raise AssertionError("\nError: cannot find file '%s'" %(name))
    success, stdout, stderr = run("spim", ["-f", name], None, timeout)
    try:
        if f:
            f(stdout, stderr)
    except AssertionError as e:
        print(_WRONG)
        raise e
    print(_CORRECT)
    return success, stdout, stderr

def function(name, f=None):
    print(name, end=" ")
    try:
        if f:
            f()
    except AssertionError as e:
        print(_WRONG)
        raise e
    print(_CORRECT)

def slot(a, b, x, n=10):
    dx = (b - a) / n
    i = 1
    c = a + dx
    while c <= x:
        i += 1
        c += dx
    return i
    
