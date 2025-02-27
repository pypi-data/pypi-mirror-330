#!/usr/bin/env python3
# coding=utf-8


import sys
import re
import argparse
import functools
import inspect
from typing import Callable, get_args, Optional, TypeVar
import importlib
import textwrap

import argcomplete
import rich

from .libargparse import RichArgParser


F = TypeVar("F", bound=Callable[..., any])


# class _MyArgParser(argparse.ArgumentParser):
#     def error(self, message):
#         print(message)
#         print("----------------------------------")
#         print()
#         self.print_help()
#         sys.exit(1)

#     def is_subparser(self):
#         """
#         Specific for this program because the main parser always have subparsers

#         ---------------------------------
#         Last Update: @2025-02-20 10:08:51
#         """
#         return self._subparsers is None

#     def remove_subparser(self, name):
#         del self._subparsers._actions[-1].choices[name]

#     def print_help(self, file=None):
#         """
#         Customized help display for the main parser and specific command help

#         ---------------------------------
#         Last Update: @2025-02-24 13:56:48
#         """
#         from rich.panel import Panel
#         from rich.table import Table
#         from rich.text import Text
#         from rich.console import Console

#         console = Console()
#         width = console.width

#         # @ Main
#         if self.is_subparser():  # @ note | For specific command help
#             assert hasattr(self, "doc")

#             # @ .Show-usage-box
#             usage = f" {self.prog} \[-h, --help] <Arguments>"
#             panel_usage = Panel(
#                 usage,
#                 title="Usage",
#                 title_align="left",
#                 border_style="#aaaaaa",
#                 padding=(0, 0)
#             )
#             rich.print(panel_usage)

#             # @ .Show-doc-box
#             if self.doc:
#                 panel_doc = Panel(
#                     self.doc,
#                     title="Docstring",
#                     title_align="left",
#                     border_style="#aaaaaa",
#                     padding=(0, 0)
#                 )
#                 rich.print(panel_doc)

#             # @ .Show-argument-box
#             hmsg = ""
#             i_action = 0
#             for action in self._actions:
#                 if action.dest == "help":
#                     continue
#                 i_action += 1
#                 options = sorted(action.option_strings, key=lambda x: len(x))
#                 if action.type is None:
#                     if action.default is not None:
#                         argType = type(action.default).__name__
#                     elif action.const is not None:
#                         argType = type(action.const).__name__
#                     else:
#                         argType = "str"
#                 else:
#                     argType = action.type.__name__

#                 if action.nargs == 0:
#                     assert argType == "bool", f"{argType=}"
#                 elif action.nargs:
#                     argType += action.nargs

#                 if options[0].startswith("--no-"):
#                     hmsg += " ↳ "
#                     hmsg += f"[cyan]{', '.join(options):27}[/cyan]   [gold3]{'':10}[/gold3]"
#                 else:
#                     if i_action > 1:
#                         hmsg += "[#eeeeee]" + '─' * (width - 2) + "[/#eeeeee]\n"
#                     hmsg += f"[cyan]{', '.join(options):30}[/cyan]   [gold3]{argType:10}[/gold3]"

#                     if not action.required:
#                         if action.default == "":
#                             _default = '""'
#                         else:
#                             _default = str(action.default)
#                         hmsg += f"   [bright_black]\[default: { _default + ']':10}[/bright_black]"

#                     if action.required or action.dest in self.required_bool_pair:
#                         hmsg += f"   [red]\[required][/red]"

#                 # @ ..handle-choices
#                 if action.choices:
#                     hmsg += f"\n   ■ [bright_black]Choices: {action.choices}[/bright_black]"

#                 # @ ..handle-help-msg
#                 if action.help:
#                     if action.nargs != 0:
#                         hmsg += f"\n   ■ {action.help}"
#                     elif options[0].startswith("--no-"):
#                         hmsg += f"\n   ■ {action.help}"

#                 hmsg += "\n"
#             panel_args = Panel(
#                 hmsg.rstrip(),
#                 title="Argument",
#                 title_align="left",
#                 border_style="#aaaaaa",
#                 padding=(0, 0)
#             )

#             rich.print(panel_args)
#         else:  # @ note | For main help
#             usage = f"{self.prog} \[-h, --help] <command> \[-h, --help] \[arguments]"
#             panel_usage = Panel(
#                 usage,
#                 title="Usage",
#                 title_align="left",
#                 border_style="#aaaaaa",
#                 padding=(0, 0)
#             )
#             rich.print(panel_usage)

#             commands = self._subparsers._actions[-1].choices

#             table = Table(
#                 show_header=False,
#                 show_edge=False,
#                 show_lines=False,
#                 box=None,
#                 padding=(0, 2))

#             table.add_column("Command", style="bold cyan")
#             table.add_column("Description", style="bold green")

#             rows = []
#             rowMap = {}
#             i_row = 0
#             for k, v in commands.items():
#                 if v.prog in rowMap:
#                     rows[rowMap[v.prog]][0].append(k)
#                     continue
#                 rows.append([[k], v.description])
#                 rowMap[v.prog] = i_row
#                 i_row += 1
#             for ks, v in rows:
#                 table.add_row(",".join(sorted(ks, key=lambda x: len(x))), v)

#             panel = Panel(
#                 table,
#                 title="Commands",
#                 title_align="left",
#                 border_style="#aaaaaa",
#                 padding=(0, 0)              # 调整面板内边距
#             )

#             rich.print(panel)

#         return

#     def get_subparser(self, name: str):
#         return self._subparsers._group_actions[0].choices[name]

#     def parse_args(self, args=None):
#         """
#         Add check for required no-arg options pair

#         e.g., for "def func1(do_it: bool)", the parser will add --do-it and --no-do-it, and you have to use one of them, this wrapper will do the check

#         ---------------------------------
#         Last Update: @2025-02-21 18:54:02
#         """
#         # print("--> parse_args")
#         args = super().parse_args(args)
#         subparser = self.get_subparser(args.command)
#         for pn in subparser.required_bool_pair:
#             if getattr(args, pn) is None:
#                 rich.print(f"[red]Error![/red] --{pn} or --no-{pn} is required!")
#                 sys.exit(101)
#         return args


class EasyArg:
    """
    Used to generate subparsers for target functions by decorating `@instance.command()`
    Then, call `instance.parse` to run corresponding function based on CLI command
    """

    def __init__(self, description: str = ""):
        """
        Initialize:
            - argparse.ArgumentParser & its subparsers
            - functions holder

        Last Update: @2024-11-23 14:35:26
        """
        self.parser = RichArgParser(description=description)
        self.subparsers = self.parser.add_subparsers(dest='command', help='Execute functions from CLI commands directly')
        self.functions = {}

    def command(self, name="", desc="", alias="", defaults: None | dict = None, choicess: None | dict = dict()) -> Callable[[F], F]:
        """
        A function decorator, used to generate a subparser and arguments based on the function signature

        :param defaults: Set specific default values for arguments under cmd invocation
        :param choicess: Set specific choices for arguments under cmd invocation

        ---------------------------------
        Last Update: @2025-02-24 13:45:24
        """
        if choicess is None:
            choicess = {}
        if defaults is None:
            defaults = {}

        def decorator(func: F) -> F:
            # @ Prepare
            # @ .handle-names
            cmd_name = name if name else func.__name__
            cmd_name = cmd_name.replace("_", "-")
            if alias:
                aliases = [alias]
            else:
                aliases = []
            # @ .get-short-description
            if not desc and func.__doc__ is not None:
                desc2 = re.split(r'\n *\n', func.__doc__)[0].strip()  # Use the first paragraph
            else:
                desc2 = desc

            # @ .refine-long-doc | and save argument information
            argInfos = {}
            choicess_implicit = {}
            if func.__doc__ is not None:
                doc = textwrap.dedent(func.__doc__).strip()
                argLines = re.findall(r":param ([0-9a-zA-Z_]+): +(.*)", doc)
                for an, ai in argLines:  # @ exp | arg-name, arg-info
                    if an not in choicess:
                        rerst = re.match(r"(\{.*?\}) .*", ai)
                        if rerst:
                            elements = re.findall(r"\w+", rerst.group(1))
                            choicess_implicit[an] = elements
                            ai = re.sub(r"\{.*?\}", "", ai)
                    argInfos[an] = ai.strip()

                doc = re.sub(r':param [0-9a-zA-Z_]+: .*', '', doc)
                doc = re.sub(r':return ?: .*', '', doc)
                doc = re.sub(r'\n+', '\n', doc, flags=re.M)
                doc = doc.strip()
            else:
                doc = desc2

            # @ .create-subparser
            parser = self.subparsers.add_parser(cmd_name, aliases=aliases, help=desc2, description=doc)  # @ exp | Add a subparser with command the same as function name
            # parser._main_parser = self.parser

            # @ Main | Add arguments with proper attributes
            shortname_recorded = set()
            sig = inspect.signature(func)
            for param_name, param in sig.parameters.items():
                # @ .retrieve-type | From annotations, take the first type for the compound types, e.g. get `str`` for `typing.Union[str, float]`
                param_name_opt = param_name.replace("_", "-")
                annotation = param.annotation
                annotations = get_args(annotation)
                if annotations:  # @ note | search priority:  float > int > str, and bool
                    if float in annotations:
                        cmdType = float
                    elif int in annotations:
                        cmdType = int
                    elif str in annotations:
                        cmdType = str
                    elif bool in annotations:
                        cmdType = bool
                    else:
                        raise TypeError(f"No intrinsic type annotation for parameter: {param_name}")
                else:
                    cmdType = annotation
                    assert cmdType in (float, int, str, bool), f"No intrinsic type annotation for parameter: {param_name}"

                if param_name in choicess_implicit:  # @ exp | apply implicit choices according to param type
                    choicess[param_name] = [cmdType(e) for e in choicess_implicit[param_name]]

                # @ .get-attribute
                required = param.default == inspect._empty
                if param_name in defaults:
                    default = defaults[param_name]
                    required = False
                else:
                    default = None if required else param.default

                # @ .add-argument | Only support intrinsic types: int, float, str & bool
                # @ - Use the first letter as short-name if no conflict
                if cmdType == inspect.Parameter.empty:
                    raise TypeError(f"Parameter '{param_name}' in function '{func.__name__}' missing type hint")

                elif cmdType in (int, float, str, bool):
                    short_name = param_name[0]
                    assert short_name.isalpha()
                    option_strings = ["--" + param_name_opt]
                    if short_name not in shortname_recorded:
                        option_strings.append("-" + short_name)
                        shortname_recorded.add(short_name)
                    if cmdType is bool:
                        parser.add_argument(*option_strings, dest=param_name, action="store_true", required=required, help=argInfos.get(param_name, ""))
                    else:
                        parser.add_argument(*option_strings, type=cmdType, required=required, default=default, choices=choicess.get(param_name), help=argInfos.get(param_name, ""))
                # elif cmdType == bool:
                #     # @ ..handle-bool-specifically
                #     short_name = param_name[0]
                #     assert short_name.isalpha()
                #     if required:
                #         parser.required_bool_pair.append(param_name)
                #     if short_name not in shortname_recorded:
                #         parser.add_argument(f"--{param_name_opt}", f"-{short_name}", dest=param_name, action="store_true", default=default, help=argInfos.get(param_name, ""))
                #         shortname_recorded.add(short_name)
                #     else:
                #         parser.add_argument(f"--{param_name_opt}", dest=param_name, action="store_true", default=default, help=argInfos.get(param_name, ""))
                #     parser.add_argument(f"--no-{param_name_opt}", dest=param_name, action="store_false", default=None if default is None else not default, help=argInfos.get(param_name, ""))
                else:
                    raise TypeError(f"easyarg only supports types: int, float, str & bool, now is {cmdType}")

            # @ Post
            self.functions[cmd_name] = func

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper  # type: ignore
        return decorator

    def parse(self, args: Optional[list[str]] = None):
        """
        Last Update: @2024-11-23 14:40:31
        ---------------------------------
        Parse arguments and call corresponding function
        """
        argcomplete.autocomplete(self.parser)
        args = self.parser.parse_args(args)
        kwargs = {key: value for key, value in vars(args).items() if key != 'command' and value is not None}

        if args.command is None:
            self.parser.print_help()
            return
        # print(self.functions)
        func = self.functions[args.command]
        func(**kwargs)
