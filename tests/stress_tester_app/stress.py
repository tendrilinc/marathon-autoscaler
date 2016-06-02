#!/usr/bin/env python
import json
import logging
import os
import random
from subprocess import call
import sys


def single_play(command_statements):
    """
    Executes the command_statements once, in order.
    :param command_statements: list of statement lists
    :return: None
    """
    for statement in command_statements:
        execute_statement(statement)


def repeat_play(command_statements):
    """
    Infinitely repeat the single_play.
    :param command_statements: list of statement lists
    :return: None
    """
    while True:
        single_play(command_statements)


def shuffle_play(command_statements):
    """
    Randomly pop statements from the list and execute.
    :param command_statements: list of statement lists
    :return: None
    """
    statements = list(command_statements)
    while len(statements) > 0:
        total_cmds = len(statements) - 1
        if total_cmds > 0:
            next_statement = statements.pop(random.randint(1, total_cmds))
        else:
            next_statement = statements.pop(0)
        execute_statement(next_statement)


def repeat_shuffle_play(command_statements):
    """
    Infinitely repeat the shuffle_play.
    :param command_statements: list of statement lists
    :return: None
    """
    statements = tuple(command_statements)
    while len(statements) > 0:
        shuffle_play(statements)
        print(statements)


def execute_statement(statement):
    """
    Pass the statement list to subprocess.call()
    :param statement:
    :return:
    """
    print("Calling {0}".format(statement))
    call(statement)


def generate_command_statement(instruction):
    """
    Converts json fragment to list (cmd, [args] [switches] [flags])
    :param instruction: json fragment
    :return: statement list
    """
    cmd_statement = [instruction.get("cmd")]
    for arg in instruction.get("args", []):
        cmd_statement.append(arg)
    for switch, value in instruction.get("switches", {}).items():
        cmd_statement.append(switch)
        cmd_statement.append(value)
    for flag in instruction.get("flags", []):
        cmd_statement.append(flag)
    return cmd_statement


def load_instruction_set():
    """
    Converts the INSTRUCTIONS environment variable to json object.
    :return: json object
    """
    raw_data = os.getenv("INSTRUCTIONS")
    try:
        return json.loads(raw_data)
    except ValueError as err:
        logger.info(raw_data)
        logger.exception(err)


def get_play_mode(instruction_set):
    """
    Get the play_mode, type of execution arrangement.
    :param instruction_set: json object
    :return: play_mode value
    """
    result = instruction_set.get("play_mode")
    if result is None:
        raise ValueError("Play mode not found in instruction_set data.")
    return result


def get_command_statements(instruction_set):
    """
    Get the instructions out of the json document.
    :param instruction_set: json document containing instructions
    :return: list of statement lists
    """
    raw_instructions = instruction_set.get("instructions")
    if raw_instructions is None:
        raise ValueError("Instructions not found in instruction_set data.")
    instructions = []
    for instruction in raw_instructions:
        instructions.append(generate_command_statement(instruction))

    return instructions


def establish_logger():
    """
    Enable logging
    :return: None
    """
    logging.getLogger('').handlers = []

    log_formatter = logging.Formatter("%(asctime)s %(process)d %(funcName)s:%(lineno)d %(name)s %(message)s")
    log_system = logging.getLogger(__name__)
    log_system.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_formatter)

    log_system.addHandler(console_handler)

    return log_system


def start():
    """
    Begin play / execution of instructions.
    :return: None
    """
    instruction_set = load_instruction_set()
    play_mode = get_play_mode(instruction_set)
    command_statements = get_command_statements(instruction_set)
    play_modes[play_mode](command_statements)


if __name__ == "__main__":
    play_modes = {
        "single": single_play,
        "repeat": repeat_play,
        "shuffle": shuffle_play,
        "repeat_shuffle": repeat_shuffle_play
    }
    logger = establish_logger()
    start()
