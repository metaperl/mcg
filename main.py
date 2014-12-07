# core

import itertools
import sys
import logging

# 3rd party

import argh
import enum


logging.basicConfig(
    format='%(lineno)s %(message)s',
    level=logging.WARN
)
direction = enum.Enum('up', 'down', 'sideways')

class Command:
    """
    A Command instance consists of a start_floor and a list of
    Transition instances.
    """

    def __init__(self, start_floor, transitions):
        self.start_floor = start_floor
        self.transitions = transitions

    def __str__(self):
        return "Command, \n\tstart_floor = {0}\n\ttransitions = {1}".format(
            self.start_floor, map(str, self.transitions))

class Transition:
    """
    A Transition instance consists of an origin floor
    and destination floor.
    """

    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

    @property
    def direction(self):
        if self.origin > self.destination:
            return direction.down
        if self.origin < self.destination:
            return direction.up
        return direction.sideways

    def __str__(self):
        return "Transition {0} -> {1}".format(self.origin, self.destination)

class Path:
    """A Path instance represents the list of floors to go to and the
    distance traveled."""

    def __init__(self):
        self.floors = []
        self.distance = 0

    def __str__(self):
        return "{0} ({1})".format(
            " ".join([str(f) for f in self.floors]),
            self.distance)


def parse_command_string(s):
    """
    Given a COMMAND_STRING, return a 2-tuple of START_FLOOR and
    list of Transition instances.
    """
    start_floor, origins_and_destinations = s.split(':')
    start_floor = int(start_floor)

    command = Command(start_floor, [])

    for o_d in origins_and_destinations.split(','):
        o,d = [ int(i) for i in o_d.split('-') ]
        logging.debug("{0}:{1}->{2}".format(start_floor, o,d))
        command.transitions.append(Transition(o,d))

    return command


def commands(filename):
    """
    Given a FILENAME, open the file and yield each line as a command.
    """
    f = file(filename).read()

    for command_string in f.split('\n'):
        logging.debug(command_string)
        yield parse_command_string(command_string)


def process(command):
    """
    Given a COMMAND, return a Path instance calculatived naively (mode A).
    """

    p = Path()

    last_floor = command.start_floor
    p.floors.append(last_floor)
    for transition in command.transitions:
        p.distance += abs(last_floor - transition.origin)
        p.distance += abs(transition.origin - transition.destination)
        p.floors.append(transition.origin)
        p.floors.append(transition.destination)
        last_floor = transition.destination

    return p

def remove_consecutive_duplicates(i):
    return [x[0] for x in itertools.groupby(i)]

def pairwise_abs(i):
    diffs = [abs(a-b) for a,b in itertools.izip(i, i[1:])]
    return sum(diffs)

def get_next(i):
    try:
        return i.next()
    except StopIteration:
        return None

def sort_floors(_direction, floors):
    if _direction == direction.down:
        return sorted(floors, reverse=True)
    return sorted(floors)


def compress_transitions(command):
    """
    Given a list of Transition instances, return an optimized list of floors.
    """

    starting_floor_transition = Transition(
        command.start_floor,
        command.transitions[0].origin)

    grouped_transitions = itertools.groupby(
        [starting_floor_transition] + command.transitions,
        lambda x: x.direction)

    logging.debug(grouped_transitions)

    master_path = Path()

    for _direction, group in grouped_transitions:
        floors = set()
        for g in group:
            floors.add(g.origin)
            floors.add(g.destination)
        master_path.floors.append(sort_floors(_direction, floors))

    master_path = remove_consecutive_duplicates(
        itertools.chain.from_iterable(master_path.floors))

    return list(master_path)



def optimal_process(command):
    """
    Given a COMMAND, return a Path instance calculatived optimally (mode B).
    """

    p = Path()
    p.floors = compress_transitions(command)

    logging.debug(p.floors)

    p.distance = pairwise_abs(p.floors)

    return p

def main(input_file, mode='A'):
    """
    Given an INPUT_FILE of navigation commands and a NAVIGATION_MODE,
for each command, print to standard output a single line consisting of a space-delimited list of floors followed by the total distance in floors that the elevator travels, in parenthesis "(" and ")". The lists of floors begins with the initial floor location followed by the visited floors in the order that the elevator visits them.
    """

    for i, command in enumerate(commands(input_file)):
        logging.debug(command)

        if mode.upper() == 'A':
            print process(command)
        elif mode.upper() == 'B':
            print optimal_process(command)
        else:
            print "Mode '{0}' not recognized".format(mode)


if __name__ == '__main__':
    argh.dispatch_command(main)
