import argparse
import multiprocessing
import sys

from twisted.internet import defer, protocol, reactor
from twisted.internet.task import coiterate


class VergeProcess(protocol.ProcessProtocol):
    def __init__(self, stdout, stderr=sys.stderr, reactor=reactor):
        self.done = defer.Deferred()
        self.reactor = reactor
        self.stdout = stdout
        self.stderr = stderr

    @classmethod
    def spawn(cls, command, *args, **kwargs):
        protocol = cls(*args, **kwargs)
        protocol.reactor.spawnProcess(
            processProtocol=protocol,
            executable=command[0],
            args=command,
        )
        return protocol.done

    def errReceived(self, data):
        self.stderr.write(data)

    def outReceived(self, data):
        self.stdout.write(data)

    def processEnded(self, reason):
        self.done.callback(None)


def main(command, arguments=None, max_processes=None, stdout=sys.stdout):
    if max_processes is None:
        max_processes = multiprocessing.cpu_count()

    processes = (
        VergeProcess.spawn(command + [argument], stdout=stdout)
        for argument in arguments
    )

    return defer.gatherResults(
        coiterate(processes) for _ in xrange(max_processes)
    )


def parse(argv=None, stdin=sys.stdin):
    arguments = (line[:-1] for line in stdin)
    return dict(vars(parser.parse_args(argv)), arguments=arguments)


parser = argparse.ArgumentParser()
parser.add_argument("command", nargs=argparse.REMAINDER)
