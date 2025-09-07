"""Service for smali code patching."""

import re
from pathlib import Path
from typing import List, Optional

from ..exceptions import FridaPatchError


class SmaliPatcher:
    """Service for patching smali code."""

    @staticmethod
    def inject_load_library(smali_file: Path, library_name: str = "frida-gadget") -> bool:
        """Inject System.loadLibrary call into smali file.

        Returns:
            bool: True if injection was successful, False otherwise.
        """
        if not smali_file.exists():
            return False

        try:
            lines = smali_file.read_text().splitlines()
            new_lines = []
            injected = False
            i = 0

            while i < len(lines):
                line = lines[i]
                new_lines.append(line)

                # Look for existing static constructor
                if line.strip().startswith(".method static constructor"):
                    injected = SmaliPatcher._inject_into_constructor(
                        lines, new_lines, i, library_name
                    )
                    # Skip processed lines
                    i = len([l for l in new_lines if l]) - 1
                i += 1

            if not injected:
                # Create new static constructor
                injected = SmaliPatcher._create_constructor(
                    new_lines, library_name
                )

            if injected:
                smali_file.write_text("\n".join(new_lines))
                return True

        except Exception as e:
            raise FridaPatchError(f"Failed to patch smali file {smali_file}: {e}")

        return False

    @staticmethod
    def _inject_into_constructor(lines: List[str], new_lines: List[str], 
                               start_index: int, library_name: str) -> bool:
        """Inject into existing static constructor."""
        i = start_index + 1

        # Find .locals line
        while i < len(lines) and not lines[i].strip().startswith(".locals"):
            new_lines.append(lines[i])
            i += 1

        if i >= len(lines):
            return False

        # Process .locals line
        locals_line = lines[i]
        new_lines.append(locals_line)

        # Update locals count
        match = re.search(r"\.locals (\d+)", locals_line)
        if match:
            locals_count = int(match.group(1)) + 1
            new_lines[-1] = f"    .locals {locals_count}"

        # Inject loadLibrary call
        new_lines.extend([
            "",
            f'    const-string v0, "{library_name}"',
            "    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V",
            ""
        ])

        # Add remaining lines
        i += 1
        while i < len(lines):
            new_lines.append(lines[i])
            i += 1

        return True

    @staticmethod
    def _create_constructor(lines: List[str], library_name: str) -> bool:
        """Create new static constructor."""
        # Find insertion point (before first method or before .end class)
        insert_index = -1

        for i, line in enumerate(lines):
            if (line.strip().startswith(".method") and 
                not line.strip().startswith(".method static constructor")):
                insert_index = i
                break

        if insert_index == -1:
            # Insert before .end class
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].strip() == ".end class":
                    insert_index = i
                    break

        if insert_index != -1:
            constructor_lines = [
                "",
                ".method static constructor <clinit>()V",
                "    .locals 1",
                "",
                f'    const-string v0, "{library_name}"',
                "    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V",
                "",
                "    return-void",
                ".end method",
                ""
            ]

            lines[insert_index:insert_index] = constructor_lines
            return True

        return False

    @staticmethod
    def is_already_patched(smali_file: Path, library_name: str = "frida-gadget") -> bool:
        """Check if smali file is already patched."""
        if not smali_file.exists():
            return False

        try:
            content = smali_file.read_text()
            return f'"{library_name}"' in content and "loadLibrary" in content
        except Exception:
            return False
