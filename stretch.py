#!/usr/bin/env python3

import time
from pprint import pprint
from collections import namedtuple

# each second is multiplied by seconds_scale. If you're debugging and
# seconds are too slow (or fast), set this to < 1 for faster second
# ticks, or > 1 for slower ones.
seconds_scale = 1.0

Movement = namedtuple('Movement', ('description', 'time_in_seconds'))

def status(fmt, count):
    return fmt.format('#' * count)

def run_movement(current_description, longest_description_length, next_description, seconds, max_seconds):
    """\
    Run a single movement.

    longest_description_length and max_seconds are for aligning the
    output, which makes the output nicer when you have multiple
    different movements in a single set. Specify None if you don't
    care.
    """

    if longest_description_length is None:
        longest_description_length = len(current_description)
    if max_seconds is None:
        max_seconds = seconds
    
    fmt = "{seconds_spacer}[{{:{seconds}s}}] {current_description}{description_spacer}   next: {next_description} ".format(current_description=current_description,
                                                                                                                           seconds=seconds,
                                                                                                                           next_description=next_description,
                                                                                                                           seconds_spacer=' ' * (max_seconds - seconds),
                                                                                                                           description_spacer=' ' * (longest_description_length - len(current_description)))
    
    for count in range(seconds):
        print(status('\r' + fmt, count), end='')
        time.sleep(1 * seconds_scale)

    print(status('\r' + fmt, count + 1))


def run_set(set_description,
            movements,
            next_set_description):
    """\
    Run the supplied movements in sequence.
    """
    
    print("Next: {}".format(set_description))
    print("Press enter when ready; start: {}".format(movements[0].description))
    input()

    max_seconds = max(m.time_in_seconds for m in movements)
    longest_description_length = max(len(m.description) for m in movements)
    
    for (i, movement) in enumerate(movements):
        (movement_description, movement_time) = movement
        
        next_movement = ([m.description for m in movements[i+1:][:1]] or [next_set_description])[0]
        run_movement(movement_description, longest_description_length, next_movement, movement_time, max_seconds)

def movements_with_breaks_between_sets(sets, time_between_sets):
    """\
    Add a break movement between the movements of each input set.
    Return a flattened list of movements.
    
    sets: A list of lists, each containing Movement objects, eg.

    [[Movement("Set 1 movement 1", 5),
      Movement("Set 1 movement 2", 5)],
     [Movement("Set 2 movement 1", 5),
      Movement("Set 2 movement 2", 5)]]

    Example result:
    
    [Movement("Set 1 movement 1", 5),
     Movement("Set 1 movement 2", 5),
     Movement("Break", time_between_sets),
     Movement("Set 2 movement 1", 5),
     Movement("Set 2 movement 2", 5)]
    """
    
    movements = []

    for i, set_ in enumerate(sets):
        if i > 0:
            movements.append(Movement('Relax', time_between_sets))
        movements.extend(set_)
        
    return movements

def sets_with_progress(sets):
    """\
    Add a "(i/n)" indicator to each movement in each set of sets, that
    increments with each set.

    sets: A list of lists, each containing Movement objects, eg.

    [[Movement("Set 1 movement 1", 5),
      Movement("Set 1 movement 2", 5)],
     [Movement("Set 2 movement 1", 5),
      Movement("Set 2 movement 2", 5)]]

    Example result:
    
    [[Movement("Set 1 movement 1 (1/2)", 5),
      Movement("Set 1 movement 2 (1/2)", 5)],
     [Movement("Set 2 movement 1 (2/2)", 5),
      Movement("Set 2 movement 2 (2/2)", 5)]]
    """
    
    count = len(sets)
    updated_sets = []
    for i, set_ in enumerate(sets):
        updated_set = []
        for movement in set_:
            updated_set.append(Movement(movement.description + " ({}/{})".format(i + 1, count), movement.time_in_seconds))
        updated_sets.append(updated_set)
    return updated_sets
        
