"""
utils_library
Eine Sammlung von persönlichen Helferfunktionen:
- io_utils: Dateihandling
- viz_utils: Plotting und Pretty-Print
- parallel_utils: Multicore-Helpers
"""

from .io_utils import (
    load_file,
    save_file,
    file_exists,
    folder_exists,
    move_file,
    copy_file,
    create_folderpath,
)

from .viz_utils import (
    auto_plot,
    pretty_print,
)

from .parallel_utils import (
    run_parallel_list,
    run_parallel_stream,
)

__all__ = [
    # io_utils
    "load_file", "save_file", "file_exists", "folder_exists",
    "move_file", "copy_file", "create_folderpath",

    # viz_utils
    "auto_plot", "pretty_print",

    # parallel_utils
    "run_parallel_list", "run_parallel_stream",
]
