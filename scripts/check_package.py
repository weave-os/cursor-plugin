"""Validate the Weave manifests, shared skill, and reproducible OpenAI upload."""

import argparse
import hashlib
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit
from urllib.request import urlopen
from zipfile import BadZipFile, ZipFile

from package_openai import LOGO, MCP_URL, ROOT, SCHEMA_ROOT, SKILL, load_json, read_source


# Snapshot of the tool registrations used by the skill. This release check
# requires neither access to the product monorepo nor a customer's OAuth token.
# https://github.com/weave-os/weave/blob/b27f25b3e67329719d214b30427b0dfdf66afbe4/mcp/src/mcp_server/public/server.py
CORE_TOOLS = {"resolve_entities", "get_metric_overview", "get_metric_drill_down"}
OPTIONAL_TOOLS = {"get_pr_details", "search_prs", "search_documentation", "get_documentation"}
PLACEHOLDER = re.compile(
    r"\$\{[^}]+\}|\{\{[^}]+\}\}|<(?:your|insert|replace)[-_][^>]*>"
    r"|\b(?:TODO|TBD|REPLACE_ME)\b|https?://(?:www\.)?example\.(?:com|org|net)\b",
    re.IGNORECASE,
)
CREDENTIAL_FIELDS = {"headers", "authorization", "apikey", "accesstoken", "refreshtoken", "clientsecret", "testcredentials"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def check_manifest_values(value: object, location: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized_key = key.lower().replace("_", "").replace("-", "")
            require(normalized_key not in CREDENTIAL_FIELDS, f"{location} contains a credential or header field")
            check_manifest_values(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            check_manifest_values(child, f"{location}[{index}]")
    elif isinstance(value, str):
        require(PLACEHOLDER.search(value) is None, f"{location} contains placeholder text")


def check_schema(name: str, document: dict) -> None:
    from jsonschema import Draft202012Validator

    url = f"{SCHEMA_ROOT}/{name.removesuffix('.json')}.schema.json"
    with urlopen(url, timeout=15) as response:
        schema = load_json(response.read())
    require(schema.get("$id") == url, f"Unexpected schema ID at {url}")
    Draft202012Validator.check_schema(schema)
    error = next(Draft202012Validator(schema).iter_errors(document), None)
    if error is not None:
        raise ValueError(f"{name} failed the Agent Plugins schema at {error.json_path} ({error.validator})")


def check_manifests() -> dict:
    names = (
        "plugin.json",
        "mcp.json",
        ".mcp.json",
        ".claude-plugin/plugin.json",
        ".claude-plugin/marketplace.json",
        ".cursor-plugin/plugin.json",
    )
    manifests = {name: load_json(read_source(name)) for name in names}
    for name, document in manifests.items():
        check_manifest_values(document, name)

    portable = manifests["plugin.json"]
    portable_mcp = manifests["mcp.json"]
    check_schema("plugin.json", portable)
    check_schema("mcp.json", portable_mcp)
    require(portable["name"] == "weave", "plugin.json must preserve the weave plugin ID")
    require(re.fullmatch(r"\d+\.\d+\.\d+(?:-[\w.-]+)?(?:\+[\w.-]+)?", portable["version"]) is not None,
            "plugin.json must declare a release version")
    for name in (".claude-plugin/plugin.json", ".cursor-plugin/plugin.json"):
        for field in ("name", "version", "repository", "license"):
            require(manifests[name][field] == portable[field], f"{name}.{field} must match plugin.json")
        for field in ("name", "email"):
            require(manifests[name]["author"][field] == portable["author"][field],
                    f"{name}.author.{field} must match plugin.json")
    require(manifests[".cursor-plugin/plugin.json"]["logo"] == LOGO, f"Cursor logo must reference {LOGO}")

    claude_marketplace = manifests[".claude-plugin/marketplace.json"]
    require(claude_marketplace["name"] == "weave", "Claude marketplace must preserve the weave ID")
    listing, = claude_marketplace["plugins"]
    require(listing["name"] == "weave" and listing["source"] == "./",
            "Claude marketplace must list the weave plugin at the repository root")

    for name, transport in (("mcp.json", "streamable-http"), (".mcp.json", "http")):
        require(manifests[name]["mcpServers"] == {"weave": {"type": transport, "url": MCP_URL}},
                f"{name} must declare only the Weave OAuth endpoint {MCP_URL}")

    interface = portable["extensions"]["com.openai"]["interface"]
    for key, limit in (("displayName", 30), ("shortDescription", 30), ("longDescription", 4000), ("developerName", 80), ("category", 80)):
        value = interface[key]
        require(isinstance(value, str) and bool(value.strip()) and len(value) <= limit,
                f"OpenAI interface.{key} must contain 1 to {limit} characters")
    for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        value = interface[key]
        url = urlsplit(value)
        require(len(value) <= 1024 and url.scheme == "https" and bool(url.hostname) and url.username is None,
                f"OpenAI interface.{key} must be an HTTPS URL without credentials")
    return portable_mcp


def check_skill() -> None:
    discovered = {path.relative_to(ROOT).as_posix() for path in ROOT.glob("skills/*/SKILL.md")}
    require(discovered == {SKILL}, "The plugin must discover only the shared engineering analytics skill")
    skill = read_source(SKILL).decode("utf-8").replace("\r\n", "\n")
    match = re.fullmatch(r"---\n(.*?)\n---\n(.+)", skill, re.DOTALL)
    require(match is not None, f"{SKILL} needs frontmatter and a body")
    header, body = match.groups()
    require(re.findall(r"^name:[ \t]*(\S+)$", header, re.MULTILINE) == [Path(SKILL).parent.name],
            f"{SKILL} name must match its directory")
    description = re.search(r"^description:[ \t]*(\S[^\n]*)$", header, re.MULTILINE)
    require(description is not None and bool(body.strip()), f"{SKILL} needs a description and instructions")
    if description[1] in {">", ">-", ">+", "|", "|-", "|+"}:
        require(re.match(r"\n +\S", header[description.end():]) is not None, f"{SKILL} description is empty")

    tools = set(re.findall(r"`((?:get|resolve|search)_[a-z0-9_]+)`", body))
    require(CORE_TOOLS <= tools, f"{SKILL} is missing core tools: {', '.join(sorted(CORE_TOOLS - tools))}")
    unknown = tools - CORE_TOOLS - OPTIONAL_TOOLS
    require(not unknown, f"{SKILL} references tools outside its checked catalog: {', '.join(sorted(unknown))}")


def check_zip(portable_mcp: dict) -> str:
    with tempfile.TemporaryDirectory() as directory:
        work = Path(directory)
        builder = ROOT / "scripts/package_openai.py"
        first, second = work / "first.zip", work / "second.zip"
        for seed, output in enumerate((first, second), start=1):
            subprocess.run(
                [sys.executable, str(builder), "--output", str(output)],
                cwd=work, env={**os.environ, "PYTHONHASHSEED": str(seed)},
                stdout=subprocess.DEVNULL, check=True,
            )
        data = first.read_bytes()
        require(data == second.read_bytes(), "OpenAI ZIP bytes must match across independent builds")

        with ZipFile(first) as archive:
            require(archive.testzip() is None, "OpenAI ZIP member checksum failed")
            expected = sorted(["LICENSE", LOGO, "mcp.json", "plugin.json", SKILL])
            require(archive.namelist() == expected, "OpenAI ZIP must contain only the approved root files")
            for member in archive.infolist():
                mode = member.external_attr >> 16
                require(stat.S_ISREG(mode) and not mode & 0o111, f"Unsafe mode for {member.filename}")
                if member.filename != "mcp.json":
                    require(archive.read(member) == read_source(member.filename), f"ZIP changed {member.filename}")
            mcp = load_json(archive.read("mcp.json"))
            check_manifest_values(mcp, "OpenAI ZIP mcp.json")

    overlay = mcp["mcpServers"]["weave"].pop("extensions")
    require(overlay == {"com.openai": {"auth": {
        "type": "oauth", "client": {"mode": "dcr"}, "baseScopes": ["mcp:tools"],
    }}}, "OpenAI ZIP must supply the documented DCR OAuth settings")
    require(mcp == portable_mcp, "OpenAI ZIP MCP config must otherwise match the portable source")
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, epilog="Requires jsonschema==4.25.1 and access to agent-plugins.org.")
    parser.parse_args()
    try:
        portable_mcp = check_manifests()
        check_skill()
        digest = check_zip(portable_mcp)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, ImportError, BadZipFile, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Package checks failed: {error}\n")
    print(f"Validated manifests, shared skill, and OpenAI ZIP (SHA-256 {digest})")


if __name__ == "__main__":
    main()
