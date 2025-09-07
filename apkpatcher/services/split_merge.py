"""Service for handling split APK merging."""

from pathlib import Path
from typing import List

from ..exceptions import BuildError, ValidationError
from .apktool import ApktoolService
from .signing import SigningService


class SplitMergeService:
    """Service for merging split APKs into single APK."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.apktool_service = ApktoolService(verbose=verbose)
        self.signing_service = SigningService(verbose=verbose)

    def merge_split_apks(self, apk_paths: List[Path], net: bool = False) -> Path:
        """Merge multiple split APKs into a single APK."""
        if not apk_paths:
            raise ValidationError("No APK paths provided")

        if len(apk_paths) == 1:
            # Single APK, just sign and return
            return self.signing_service.sign_apk(apk_paths[0])

        # Find base APK
        base_apk = None
        split_apks = []

        for apk_path in apk_paths:
            if apk_path.name == "base.apk":
                base_apk = apk_path
            else:
                split_apks.append(apk_path)

        if base_apk is None:
            base_apk = apk_paths[0]  # Use first as base
            split_apks = apk_paths[1:]

        if self.verbose:
            print(f"Merging {len(apk_paths)} split APKs...")

        # Decode all APKs
        base_dir = self.apktool_service.decode(base_apk, no_resources=False, no_sources=True)

        split_dirs = []
        for split_apk in split_apks:
            split_dir = self.apktool_service.decode(
                split_apk, 
                no_resources=False, 
                no_sources=True,
                extra_args="--resource-mode dummy"
            )
            split_dirs.append(split_dir)

        # Merge content from split APKs into base
        self._merge_split_content(base_dir, split_dirs)

        # Fix dummy resource identifiers
        self._fix_dummy_resources(base_dir, split_dirs)

        # Update manifest to disable APK splitting
        self._disable_apk_splitting(base_dir)

        # Build merged APK
        output_path = base_apk.parent / "merged.apk"
        built_path = self.apktool_service.build(base_dir, output_path, add_network_config=net)

        # Sign merged APK
        signed_path = self.signing_service.sign_apk(built_path)

        if self.verbose:
            print(f"Merged APK created: {signed_path}")

        return signed_path

    def _merge_split_content(self, base_dir: Path, split_dirs: List[Path]) -> None:
        """Merge content from split directories into base directory."""
        import shutil

        for split_dir in split_dirs:
            # Copy all directories except AndroidManifest.xml, apktool.yml, and original/
            for item in split_dir.iterdir():
                if item.name in ["AndroidManifest.xml", "apktool.yml", "original"]:
                    continue

                target = base_dir / item.name

                if item.is_dir():
                    if item.name == "res":
                        # Special handling for res directory - only copy non-XML files
                        self._merge_res_directory(item, target)
                    else:
                        # Copy entire directory
                        if target.exists():
                            shutil.rmtree(target)
                        shutil.copytree(item, target)
                else:
                    # Copy file
                    shutil.copy2(item, target)

    def _merge_res_directory(self, source_res: Path, target_res: Path) -> None:
        """Merge res directories, excluding XML files to avoid conflicts."""
        import shutil

        for item in source_res.rglob("*"):
            if item.is_file() and not item.suffix == ".xml":
                relative_path = item.relative_to(source_res)
                target_file = target_res / relative_path

                target_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target_file)

    def _fix_dummy_resources(self, base_dir: Path, split_dirs: List[Path]) -> None:
        """Fix APKTOOL_DUMMY resource identifiers."""
        # This is a simplified implementation
        # In a full implementation, you would:
        # 1. Find all DUMMY resource IDs in base/res/values/public.xml
        # 2. Find the real names in split APK public.xml files
        # 3. Replace all references to DUMMY names with real names

        if self.verbose:
            print("Fixing dummy resource identifiers...")

        public_xml = base_dir / "res" / "values" / "public.xml"
        if not public_xml.exists():
            return

        # Simple approach: remove DUMMY entries (they'll be regenerated)
        try:
            content = public_xml.read_text()
            lines = content.splitlines()
            filtered_lines = [line for line in lines if "APKTOOL_DUMMY_" not in line]
            public_xml.write_text("\n".join(filtered_lines))
        except Exception:
            pass  # Continue without fixing if there's an issue

    def _disable_apk_splitting(self, base_dir: Path) -> None:
        """Disable APK splitting in AndroidManifest.xml."""
        from ..utils.manifest import ManifestUtils

        manifest_path = base_dir / "AndroidManifest.xml"
        if manifest_path.exists():
            ManifestUtils.disable_apk_splitting(manifest_path)
