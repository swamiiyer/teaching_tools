import datetime, os, signal, subprocess, time


def run(cmd, args=[], stdin=None, timeout=30):
    """
    Runs the specified command using the specified command-line arguments, standard input,
    and timeout, and returns the tuple (<success flag>, <output>).
    """

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


def python3(name, args=[], stdin=None, timeout=30):
    """
    Runs the specified Python program using the specified command-line arguments, standard input,
    and timeout, and returns the tuple (<success flag>, <stdout>).
    """

    success, stdout = run("python3", [name] + args, stdin, timeout)
    return (success, stdout)


def pycodestyle(filename):
    """
    Runs the pycodestyle program on the specified Python program, and returns the tuple (<success
    flag>, <stdout>).
    """

    success, stdout = run("pycodestyle", [filename])
    return (stdout == "", "\n" + stdout)


def javac(name, args=[]):
    """
    Compiles the specified Java program, and returns the tuple (<success flag>, <stdout>).
    """

    success, stdout = run("javac", [name] + args)
    return (success, stdout)


def java(name, args=[], stdin=None, timeout=30):
    """
    Runs the specified Java program using the specified command-line arguments, standard input,
    and timeout, and returns the tuple (<success flag>, <stdout>).
    """

    success, stdout = run("java", [name] + args, stdin, timeout)
    return (success, stdout)

def spim(name, args=[], stdin=None, timeout=30):
    """
    Runs the specified spim program using the specified command-line arguments, standard input,
    and timeout, and returns the tuple (<success flag>, <stdout>).
    """

    success, stdout = run("spim", ["-f", name] + args, stdin, timeout)
    return (success, stdout)

def check_style(filename):
    """
    Runs the check_style program on the specified Java program, and returns the tuple (<success
    flag>, <stdout>).
    """

    success, stdout = run("check_style", [filename])
    return (len(stdout.splitlines()[1:-1]) == 0, "\n" + stdout)


def bash(name, args=[], timeout=30):
    """
    Runs the specified bash program using the specified command-line arguments and timeout, 
    and returns the tuple (<success flag>, <stdout>).
    """

    success, stdout = run("bash", [name] + args)
    return (success, stdout)

def slot(a, b, x, n=10):
    """
    Breaks the interval [a, b) into n slots and returns the slot number [1, n] that x belongs to.
    """

    dx = (b - a) / n
    i = 1
    c = a + dx
    while c <= x:
        i += 1
        c += dx
    return i
