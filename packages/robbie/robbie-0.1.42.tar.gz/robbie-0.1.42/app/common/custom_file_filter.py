# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from __future__ import absolute_import

import fnmatch
import os
import shutil
from typing import List, Optional, Callable, Union
from common.config import PositronJob

class CustomFileFilter:
    """Configuration that specifies how the local working directory should be packaged."""

    def __init__(self, *, ignore_name_patterns: List[str] = None):
        """Initialize a CustomFileFilter.

        Args:
            ignore_name_patterns (List[str]): ignore files or directories with names
              that match one of the glob-style patterns. Defaults to None.
        """

        if ignore_name_patterns is None:
            ignore_name_patterns = []

        self._workdir = os.getcwd()
        self._ignore_name_patterns = ignore_name_patterns

    @property
    def ignore_name_patterns(self):
        """Get the ignore name patterns."""
        return self._ignore_name_patterns

    @property
    def workdir(self):
        """Get the working directory."""
        return self._workdir



def copy_workdir(
    dst: str,
    custom_file_filter: Optional[CustomFileFilter] = None,
    print_tree: bool = True,
):
    """Copy the local working directory to the destination.

    Args:
        dst (str): destination path.
        custom_file_filter (CustomFileFilter): configuration that
            specifies how the local working directory should be packaged.
    """
    # so we can print out what is shipped over
    from common.print_banner import workspace_file_tree

    """
    def _ignore_patterns(path: str, names: List):  # pylint: disable=unused-argument
        ignored_names = set()
        if custom_file_filter.ignore_name_patterns is not None:
            for pattern in custom_file_filter.ignore_name_patterns:
                ignored_names.update(fnmatch.filter(names, pattern))
        return ignored_names
    """

    def _ignore_patterns(path: str, names: List): 
        to_ignore = []
        for name in names:
            full_path = os.path.join(path, name)

            "when `default` is set in the config file"
            if os.path.isfile(full_path):
                if (name == ".python-version" or
                    name == ".DS_Store"
                ):
                    to_ignore.append(name)
                    continue

            if os.path.isdir(full_path):
                if (name == "__pycache__" or 
                    name == "job-execution" or 
                    name == ".robbie" or 
                    name == ".ipynb_checkpoints" or
                    name == "venv" or 
                    name == ".pyenv" or 
                    name == ".git" or
                    name == ".venv"
                ):
                    to_ignore.append(name)
                    continue

            ignoring = False
            # go through each pattern if they exist
            if (custom_file_filter is not None and 
                custom_file_filter.ignore_name_patterns is not None
            ):
                for pattern in custom_file_filter.ignore_name_patterns:
                    if fnmatch.fnmatch(name, pattern):
                        to_ignore.append(name)
                        ignoring = True
                        break
            # if not ignoring:
            #     workspace_file_tree.add(f"[yellow]{full_path}, size: {os.path.getsize(full_path)} bytes[/yellow]")
            
        return to_ignore

    def fake_copytree(src, ignore=None):
        """
        Recursively prints the tree from `src` using the ignore function.
        Calls the `ignore` function for each directory visited.

        Args:
            src (str): Source directory path.
            dst (str): Destination directory path.
            ignore (callable, optional): A callable that takes the directory path and its contents 
                                         (list of names) and returns a list of names to ignore.
        """
        # Ensure the destination directory exists
        # os.makedirs(dst, exist_ok=True)

        # Get the list of items in the source directory
        entries = os.listdir(src)

        # Apply the ignore function if provided
        ignored_names = ignore(src, entries) if ignore else []

        for entry in entries:
            full_path = os.path.join(src, entry)

            if entry in ignored_names:
                continue  # Skip ignored items

            src_path = os.path.join(src, entry)

            if os.path.isdir(src_path):
                # Recursively copy subdirectory
                fake_copytree(src_path, ignore)
            else:
                # Add file to tree
                workspace_file_tree.add(f"[yellow]{os.path.relpath(full_path)}, size: {os.path.getsize(full_path)} bytes[/yellow]")

    # start of execution
    _ignore = None
    _src = os.getcwd()
    if not custom_file_filter:
        _ignore = _ignore_patterns
    elif isinstance(custom_file_filter, CustomFileFilter):
        _ignore = _ignore_patterns
        _src = custom_file_filter.workdir

    if print_tree:
        fake_copytree(_src, _ignore)
    else:
        shutil.copytree(
            _src,
            dst,
            ignore=_ignore,
            dirs_exist_ok=True,
        )





