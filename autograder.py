import datetime, _io, os, signal, subprocess, time

_CORRECT = u"\u2714"
_WRONG = u"\u2718"

# Runs the specified command using the specified command-line arguments, standard input,
# and timeout, and returns the tuple (<success flag>, <output>).
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


def python3(name, args=[], stdin=None, timeout=30, f=None):
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
    try:
        if f:
            f(stdout)
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

# Compiles the specified Java program, and returns the tuple (<success flag>, <stdout>).
def javac(name, args=[]):
    success, stdout = run("javac", [name] + args)
    return (success, stdout)

# Runs the specified Java program using the specified command-line arguments, standard input,
# and timeout, and returns the tuple (<success flag>, <stdout>).
def java(name, args=[], stdin=None, timeout=30):
    success, stdout = run("java", [name] + args, stdin, timeout)
    return (success, stdout)

# Runs the specified spim program using the specified command-line arguments, standard input,
# and timeout, and returns the tuple (<success flag>, <stdout>).
def spim(name, args=[], stdin=None, timeout=30):
    success, stdout = run("spim", ["-f", name] + args, stdin, timeout)
    return (success, stdout)

# Runs the specified bash program using the specified command-line arguments and timeout, 
# and returns the tuple (<success flag>, <stdout>).
def bash(name, args=[], timeout=30):
    success, stdout = run("bash", [name] + args)
    return (success, stdout)

# Breaks the interval [a, b) into n slots and returns the slot number [1, n] that x belongs to.
def slot(a, b, x, n=10):
    dx = (b - a) / n
    i = 1
    c = a + dx
    while c <= x:
        i += 1
        c += dx
    return i
