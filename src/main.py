# -*- coding: utf-8 -*-

import sys
from pathlib import Path

from seewo_editor.runtime import current_runtime_info, write_runtime_diagnostic


def _value_after(argv: list[str], option: str) -> str | None:
    if option not in argv:
        return None
    index = argv.index(option)
    if index + 1 >= len(argv):
        return None
    return argv[index + 1]


def _main() -> int:
    entry_file = Path(__file__)
    argv = sys.argv[1:]
    diagnose_path = _value_after(argv, "--diagnose-runtime")
    if diagnose_path:
        write_runtime_diagnostic(
            diagnose_path,
            current_runtime_info(entry_file),
            _value_after(argv, "--music"),
        )
        return 0

    from seewo_editor.app import main

    return main(entry_file, argv)


if __name__ == "__main__":
    raise SystemExit(_main())
