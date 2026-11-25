"""Build the OpenAI Plugins Directory upload from the shared Weave plugin."""

import argparse
import io
import json
import math
import os
from pathlib import Path
import re
import stat
import tempfile
from xml.etree import ElementTree
from zipfile import ZIP_STORED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist/weave-analytics-openai.zip"
SCHEMA_ROOT = "https://agent-plugins.org/schemas/1.0.0"
MCP_URL = "https://app.workweave.ai/public/mcp"
SKILL = "skills/engineering-analytics/SKILL.md"
LOGO = "assets/logo.svg"
PACKAGE_FILES = ("LICENSE", LOGO, "mcp.json", "plugin.json", SKILL)
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def read_source(name: str) -> bytes:
    path = ROOT
    for component in Path(name).parts:
        path = path / component
        if path.is_symlink():
            raise ValueError(f"{name} must not use symbolic links")
    mode = path.stat().st_mode
    if not stat.S_ISREG(mode) or mode & 0o111:
        raise ValueError(f"{name} must be a regular, nonexecutable file")
    return path.read_bytes()


def unique_object(items: list[tuple]) -> dict:
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError("JSON objects must not contain duplicate keys")
        result[key] = value
    return result


def load_json(contents: bytes) -> dict:
    value = json.loads(contents, object_pairs_hook=unique_object)
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object")
    return value


def check_logo(logo: bytes) -> None:
    if len(logo) > 5 * 1024 * 1024:
        raise ValueError(f"{LOGO} exceeds the 5 MiB icon limit")

    # Accept the static SVG elements and attributes used by this plugin's logo.
    if re.search(r"<!DOCTYPE|<!ENTITY|<\?(?!xml\s)", logo.decode("utf-8")):
        raise ValueError(f"{LOGO} must not use declarations or processing instructions")
    svg = ElementTree.fromstring(logo)
    namespace = "{http://www.w3.org/2000/svg}"
    if svg.tag != namespace + "svg" or set(svg.attrib) - {"version", "width", "height", "viewBox"}:
        raise ValueError(f"{LOGO} must be a static SVG")
    if "viewBox" in svg.attrib:
        _, _, width, height = map(float, svg.attrib["viewBox"].replace(",", " ").split())
    else:
        width = float(svg.attrib.get("width", "0"))
        height = float(svg.attrib.get("height", "0"))
    if not math.isfinite(width) or width != height or width < 48:
        raise ValueError(f"{LOGO} must be square and at least 48 by 48")
    for shape in svg:
        if shape.tag != namespace + "path" or set(shape.attrib) - {"d", "fill", "transform"} or len(shape):
            raise ValueError(f"{LOGO} must contain static paths only")
        if any(re.search(r"url\s*\(", value, re.IGNORECASE) for value in shape.attrib.values()):
            raise ValueError(f"{LOGO} must not reference external resources")


def openai_zip() -> bytes:
    files = {name: read_source(name) for name in PACKAGE_FILES}
    manifest = load_json(files["plugin.json"])
    interface = manifest["extensions"]["com.openai"]["interface"]
    icon_fields = {"composerIcon", "logo"} | ({"composerIconDark", "logoDark"} & interface.keys())
    for key in sorted(icon_fields):
        if interface.get(key) != f"./{LOGO}":
            raise ValueError(f"OpenAI interface.{key} must reference ./{LOGO}")
    check_logo(files[LOGO])

    mcp = load_json(files["mcp.json"])
    if mcp != {
        "$schema": f"{SCHEMA_ROOT}/mcp.schema.json",
        "mcpServers": {"weave": {"type": "streamable-http", "url": MCP_URL}},
    }:
        raise ValueError(f"mcp.json must declare only the Weave OAuth endpoint {MCP_URL}")

    # OpenAI documents this server-level extension for its importer. Keep it
    # out of the source manifest, where the portable schema forbids it.
    # https://developers.openai.com/plugins/build/plugins
    mcp["mcpServers"]["weave"]["extensions"] = {
        "com.openai": {
            "auth": {"type": "oauth", "client": {"mode": "dcr"}, "baseScopes": ["mcp:tools"]}
        }
    }
    files["mcp.json"] = (json.dumps(mcp, indent=2) + "\n").encode("utf-8")

    output = io.BytesIO()
    # Store files directly so the bytes do not depend on a compression library.
    with ZipFile(output, "w", compression=ZIP_STORED) as archive:
        for name, contents in sorted(files.items()):
            info = ZipInfo(name, date_time=ZIP_TIMESTAMP)
            info.create_system = 3  # Unix file attributes, on every host.
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, contents)
    return output.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help=f"output ZIP (default: {DEFAULT_OUTPUT.relative_to(ROOT)})",
    )
    args = parser.parse_args()
    if args.output.suffix != ".zip":
        parser.error("--output must end in .zip")

    try:
        data = openai_zip()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=args.output.parent) as temporary:
            temp_path = Path(temporary) / "plugin.zip"
            temp_path.write_bytes(data)
            os.replace(temp_path, args.output)
    except (OSError, ValueError, TypeError, KeyError, ElementTree.ParseError) as error:
        parser.exit(1, f"Package build failed: {error}\n")
    print(args.output)


if __name__ == "__main__":
    main()
