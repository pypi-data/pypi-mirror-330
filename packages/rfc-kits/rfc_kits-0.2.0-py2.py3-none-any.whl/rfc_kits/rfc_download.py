# coding:utf-8

from concurrent.futures import ThreadPoolExecutor
from typing import List
from typing import Optional
from typing import Sequence

from xkits import add_command
from xkits import argp
from xkits import commands
from xkits import run_command

from .attribute import __description__
from .attribute import __urlhome__
from .attribute import __version__
from .rfc_editor import RFC


@add_command("rfc-download", help="Downlaod RFCs")
def add_cmd_rfc_download(_arg: argp):
    _arg.add_argument("--text", action="store_true", help="Download text RFC")
    _arg.add_argument("--html", action="store_true", help="Download html RFC")
    _arg.add_argument("--pdf", action="store_true", help="Download pdf RFC")
    _arg.add_pos("rfc_number", type=int, nargs="+", metavar="RFC", help="number")  # noqa:E501


@run_command(add_cmd_rfc_download)
def run_cmd_rfc_download(cmds: commands) -> int:
    rfc_nums: List[int] = cmds.args.rfc_number
    all_rfcs: bool = not (cmds.args.text or cmds.args.html or cmds.args.pdf)
    with ThreadPoolExecutor(max_workers=64) as executor:
        for number in rfc_nums:
            site: RFC = RFC(number)
            if all_rfcs or cmds.args.text:
                executor.submit(site.text.save)
            if all_rfcs or cmds.args.html:
                executor.submit(site.html.save)
            if all_rfcs or cmds.args.pdf:
                executor.submit(site.pdfrfc.save)
        executor.shutdown(wait=True)
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = __version__
    return cmds.run(root=add_cmd_rfc_download,
                    argv=argv,
                    description=__description__,
                    epilog=f"For more, please visit {__urlhome__}.")
