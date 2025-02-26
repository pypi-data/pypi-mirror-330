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
from .rfc_editor import BCP


@add_command("bcp-download", help="Downlaod BCPs")
def add_cmd_bcp_download(_arg: argp):
    _arg.add_argument("--text", action="store_true", help="Download text BCP")
    _arg.add_pos("bcp_number", type=int, nargs="+", metavar="BCP", help="number")  # noqa:E501


@run_command(add_cmd_bcp_download)
def run_cmd_bcp_download(cmds: commands) -> int:
    bcp_nums: List[int] = cmds.args.bcp_number
    all_bcps: bool = not (cmds.args.text)
    with ThreadPoolExecutor(max_workers=64) as executor:
        for number in bcp_nums:
            site: BCP = BCP(number)
            if all_bcps or cmds.args.text:
                executor.submit(site.text.save)
        executor.shutdown(wait=True)
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = __version__
    return cmds.run(root=add_cmd_bcp_download,
                    argv=argv,
                    description=__description__,
                    epilog=f"For more, please visit {__urlhome__}.")
