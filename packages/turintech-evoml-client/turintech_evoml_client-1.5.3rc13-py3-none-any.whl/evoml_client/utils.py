# ────────────────────────────────── Imports ───────────────────────────────── #
import importlib
import re
from pathlib import Path
from importlib import util
import sys
from typing import List


# ──────────────────────────────────────────────────────────────────────────── #


def import_module(module_location: Path, module_name: str) -> Path:
    spec = util.spec_from_file_location(name=module_name, location=module_location)
    module = util.module_from_spec(spec)
    if spec.name in sys.modules:
        for key in list(sys.modules.keys()):
            if key.startswith(spec.name):
                del sys.modules[key]
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module_location.parent.parent


def import_pipeline_module(pipeline_root: Path) -> Path:
    pipeline_code_path = pipeline_root.joinpath(*["src", "pipeline"])
    return import_module(
        module_location=pipeline_code_path.joinpath("__init__.py"),
        module_name=pipeline_code_path.name,
    )


def import_pipeline_conf_mgr(pipeline_root: Path):
    import_pipeline_module(pipeline_root=pipeline_root)
    from pipeline.conf.conf_manager import conf_mgr

    return conf_mgr


def import_preprocessor_module(preprocessor_package_path: Path):
    return import_module(
        module_location=preprocessor_package_path.joinpath("__init__.py"), module_name=preprocessor_package_path.name
    )


def sanitise_headers(headers: List[str]):
    """Clears up headers"""
    clean_headers = []
    for index, header in enumerate(headers):
        if header:
            clean = re.sub(
                "(<[^>]*>)|([(].*[)]|[<>]|[^ a-zA-Z0-9_])",
                "",
                str(header).strip().replace(" ", "_"),
            )
            # In case of duplicates
            clean_headers += [clean]
        else:
            clean_headers += [f"col_{index}"]
    for ch in range(len(clean_headers)):
        count = clean_headers.count(clean_headers[ch])
        if count > 1:
            clean_headers[ch] = f"{clean_headers[ch]}_{count}"
    return clean_headers
