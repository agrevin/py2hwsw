# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os


def setup(py_params_dict):
    # Py2hwsw dictionary describing current core
    core_dict = {
        "parent": {
            # Tester is a child core of iob_system: https://github.com/IObundle/py2hwsw/tree/main/py2hwsw/lib/hardware/iob_system
            # Tester will inherit all attributes/files from the iob_system core.
            "core_name": "iob_system",
            "include_tester": False,
            # Every parameter in the lines below will be passed to the iob_system parent core.
            **py_params_dict,
            "system_attributes": {
                # Set "is_tester" attribute to generate Makefile and flows allowing to run this core as top module
                "is_tester": True,
                # Every attribute in this dictionary will override/append to the ones of the iob_system parent core.
                "board_list": [
                    "iob_aes_ku040_db_g",
                    "iob_cyclonev_gt_dk",
                ],
                "subblocks": [
                    # Since Tester already contains one iob_uart peripheral by default
                    # to communicate with the testbench/console, we will use it as the
                    # UUT and verify it by checking that the Tester messages are
                    # printed correctly. So there is no need for other verification
                    # instruments.
                ],
            },
        },
    }

    # Create symlinks to the UUT's (iob_uart) software sources inside the Tester's software folder
    # Destination folder is Tester's software/src
    DEST_DIR = os.path.join(
        py_params_dict.get("build_dir"), py_params_dict.get("dest_dir"), "software/src"
    )
    # Source folder is relative path to core's software/src
    SRC_DIR = os.path.relpath(
        os.path.join(
            py_params_dict.get("build_dir"),
            "software/src",
        ),
        DEST_DIR,
    )
    os.makedirs(DEST_DIR, exist_ok=True)
    os.symlink(
        os.path.join(SRC_DIR, "iob_uart_csrs.c"),
        os.path.join(DEST_DIR, "iob_uart_csrs.c"),
    )
    os.symlink(
        os.path.join(SRC_DIR, "iob_uart_csrs.h"),
        os.path.join(DEST_DIR, "iob_uart_csrs.h"),
    )

    return core_dict
