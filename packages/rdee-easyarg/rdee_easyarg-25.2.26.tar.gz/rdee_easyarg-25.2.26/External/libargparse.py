# coding=utf-8

"""
Customized argparse.ArgumentParser, including:
    - prettified help information
    - handle opposite of no-arg boolean option automatically
    
Demo test is embedded into section:__main__
"""

import sys
import argparse
import re

import rich


class CustomSubParsersAction(argparse._SubParsersAction):
    def add_parser(self, name, **kwargs):
        # print(f"Adding parser: {name}")
        parser = super().add_parser(name, **kwargs)
        if "help" in kwargs:
            parser.help = kwargs["help"]
        return parser


class RichArgParser(argparse.ArgumentParser):
    def _get_sub_parsers(self, *args, **kwargs):
        # 返回自定义的 SubParsersAction
        return CustomSubParsersAction(*args, **kwargs)

    def add_subparsers(self, **kwargs):
        # 调用父类的 add_subparsers 方法，并传入自定义的 SubParsersAction
        if 'action' not in kwargs:
            kwargs['action'] = self._get_sub_parsers
        return super().add_subparsers(**kwargs)

    def error(self, message):
        rich.print(message)
        print("----------------------------------")
        print()
        self.print_help()
        sys.exit(1)

    def is_subparser(self):
        """
        Specific for this program because the main parser always have subparsers

        ---------------------------------
        Last Update: @2025-02-20 10:08:51
        """
        return self._subparsers is None

    def get_help_action(self):
        # print(self._actions)
        for act in self._actions:
            if isinstance(act, argparse._HelpAction):
                return act

    def remove_subparser(self, name):
        del self._subparsers._actions[-1].choices[name]

    def print_help(self, file=None):
        """
        Customized help display for the main parser and specific command help

        ---------------------------------
        Last Update: @2025-02-26 19:48:04
        """
        from rich.panel import Panel
        from rich.table import Table
        from rich.text import Text
        from rich.console import Console

        console = Console()
        width = console.width

        # @ Main
        if self.is_subparser():  # @ note | For specific command help

            # @ .Show-usage-box
            usage = f" {self.prog} \[-h, --help] <Arguments>"
            panel_usage = Panel(
                usage,
                title="Usage",
                title_align="left",
                border_style="#aaaaaa",
                padding=(0, 0)
            )
            rich.print(panel_usage)

            # @ .Show-doc-box
            doc = self.description
            doc = doc if doc else self.help
            if doc:  # @ note | desc is used to display in main help, doc is used to display in sub-help if possible
                panel_doc = Panel(
                    doc,
                    title="Docstring",
                    title_align="left",
                    border_style="#aaaaaa",
                    padding=(0, 0)
                )
                rich.print(panel_doc)

            # @ .Show-argument-box
            hmsg = ""
            i_action = 0
            for action in self._actions:
                if action.dest == "help":
                    continue
                i_action += 1
                options = sorted(action.option_strings, key=lambda x: len(x))
                if action.type is None:
                    if action.default is not None:
                        argType = type(action.default).__name__
                    elif action.const is not None:
                        argType = type(action.const).__name__
                    elif action.choices is not None:
                        argType = type(action.choices[0]).__name__
                    else:
                        argType = "str"
                else:
                    argType = action.type.__name__

                if action.nargs == 0:
                    assert argType == "bool", f"{argType=}"
                elif action.nargs:
                    argType += action.nargs

                if options[0].startswith("--no-"):  # @ note | may be optimized after, can be more flexible
                    hmsg += " ↳ "
                    hmsg += f"[cyan]{', '.join(options):27}[/cyan]   [gold3]{'':10}[/gold3]"
                else:
                    if i_action > 1:
                        hmsg += "[#eeeeee]" + '─' * (width - 2) + "[/#eeeeee]\n"
                    hmsg += f"[cyan]{', '.join(options):30}[/cyan]   [gold3]{argType:10}[/gold3]"

                    if action.required or (action.type is bool and action.default is None):  # @ note | for paired boolean option, one of them may be required
                        hmsg += f"   [red]\[required][/red]"
                    else:  # not action.required:
                        if action.default == "":
                            _default = '""'
                        else:
                            _default = str(action.default)
                        hmsg += f"   [bright_black]\[default: { _default + ']':10}[/bright_black]"

                # @ ..handle-choices
                if action.choices:
                    hmsg += f"\n   ■ [bright_black]Choices: {action.choices}[/bright_black]"

                # @ ..handle-help-msg
                if action.help:
                    if action.nargs != 0:
                        hmsg += f"\n   ■ {action.help}"
                    elif options[0].startswith("--no-"):
                        hmsg += f"\n   ■ {action.help}"

                hmsg += "\n"
            panel_args = Panel(
                hmsg.rstrip(),
                title="Argument",
                title_align="left",
                border_style="#aaaaaa",
                padding=(0, 0)
            )

            rich.print(panel_args)
        else:  # @ note | For main help
            usage = f"{self.prog} \[-h, --help] <command> \[-h, --help] \[arguments]"
            panel_usage = Panel(
                usage,
                title="Usage",
                title_align="left",
                border_style="#aaaaaa",
                padding=(0, 0)
            )
            rich.print(panel_usage)

            commands = self._subparsers._actions[-1].choices

            table = Table(
                show_header=False,
                show_edge=False,
                show_lines=False,
                box=None,
                padding=(0, 2))

            table.add_column("Command", style="bold cyan")
            table.add_column("Description", style="bold green")

            rows = []
            rowMap = {}
            i_row = 0
            for k, v in commands.items():
                if v.prog in rowMap:
                    rows[rowMap[v.prog]][0].append(k)
                    continue
                rows.append([[k], v.help])
                rowMap[v.prog] = i_row
                i_row += 1
            for ks, v in rows:
                table.add_row(",".join(sorted(ks, key=lambda x: len(x))), v)

            panel = Panel(
                table,
                title="Commands",
                title_align="left",
                border_style="#aaaaaa",
                padding=(0, 0)
            )

            rich.print(panel)

        return

    @property
    def subparser_dest(self):
        if self._subparsers is None:
            return ""
        return self._subparsers._group_actions[0].dest

    def get_subparser(self, name: str):
        return self._subparsers._group_actions[0].choices[name]

    def get_actions(self, name: str = "", dest: str = "", args=None):
        """
        Find target actions by name or dest

        ---------------------------------
        Last Update: @2025-02-25 17:49:35
        """
        rst: list = []
        for act in self._actions:
            if isinstance(act, argparse._HelpAction):
                continue
            elif isinstance(act, argparse._SubParsersAction):
                continue
            else:
                _name = name if name.startswith("-") else (("-" if len(name) == 1 else "--") + name)
                if act.dest == dest or _name in act.option_strings:
                    rst.append(act)
        if not rst and args is not None and self._subparsers is not None:
            subparser = self.get_subparser(getattr(args, self.subparser_dest))
            return subparser.get_actions(name)

        return rst

    def parse_args(self, args=None):
        """
        Add check for required no-arg options pair

        e.g., for "def func1(do_it: bool)", the parser will add --do-it and --no-do-it, and you have to use one of them, this wrapper will do the check

        ---------------------------------
        Last Update: @2025-02-21 18:54:02
        """
        args = super().parse_args(args)
        subparser = self.get_subparser(args.command)

        for name, val in vars(args).items():
            if val is None:
                acts = self.get_actions(dest=name, args=args)
                if acts[0].type == bool:
                    self.error(f"[red]Error![/red] dest:{name} is required!")

        return args

    def add_argument(self, *name_or_flags, action=..., nargs=None, const=..., default=..., type=..., choices=..., required=..., help=..., metavar=..., dest=..., version=..., **kwargs):
        # print(name_or_flags, action)
        paramdict = {}
        if action is not ...:
            paramdict["action"] = action
        if nargs is not None:
            paramdict["nargs"] = nargs
        if const is not ...:
            paramdict["const"] = const
        if default is not ...:
            paramdict["default"] = default
        if type is not ...:
            paramdict["type"] = type
        if choices is not ...:
            paramdict["choices"] = choices
        if required is not ...:
            paramdict["required"] = required
        if dest is not ...:
            paramdict["dest"] = dest

        if isinstance(action, str) and action.startswith("store_"):
            group = self.add_mutually_exclusive_group()

            if required is True:
                paramdict["default"] = None
            paramdict["required"] = False
            added = group.add_argument(*name_or_flags, **paramdict)
            assert added.nargs == 0
            added.type = bool
            opposite = kwargs.get("opposite", f"--no-" + added.dest.replace("_", "-"))
            oppo_action = "store_true" if action == "store_false" else "store_false"

            paramdict["default"] = None
            paramdict["action"] = oppo_action

            oppo = group.add_argument(opposite, **paramdict)
            oppo.type = bool
        else:
            return super().add_argument(*name_or_flags, **paramdict)


if __name__ == "__main__":
    print("Demo Test")
    parser = RichArgParser(description="test")
    subparsers = parser.add_subparsers(dest="command", description="this is subparsers")
    p1 = subparsers.add_parser("sub1", description="sub1-description", help="sub1-help")
    p2 = subparsers.add_parser("sub2", help="sub2-help")

    a11 = p1.add_argument("--p1-a1", help="p1, arg1")
    a12 = p1.add_argument("--p1-flag1", action="store_true", help="p1, flag1")
    a13 = p1.add_argument("--p1-flag2", action="store_true", required=True, help="p1, flag2")
    p2.add_argument("--p2-a1", choices=["a", "b"], help="p2, arg1")
    p2.add_argument("--p2-a2", choices=[2, 3], help="p2, arg2")

    args = parser.parse_args()
