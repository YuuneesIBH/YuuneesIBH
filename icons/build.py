"""Builds the tech stack rows in skillicons.dev style.

Icons without a skillicons.dev version are drawn from Iconify logos on the same
dark rounded tile. Run `python3 icons/build.py` after editing ROWS.
"""
import re
import urllib.request
from pathlib import Path

OUT = Path(__file__).parent
TILE = "#242938"

# skillicons id, or ("custom", iconify-id)
CUSTOM = {
    "sql": "vscode-icons:file-type-sql",
    "argocd": "devicon:argocd",
    "traefik": "devicon:traefikproxy",
    "entra": "selfhst:microsoft-entra-id",
    "n8n": "logos:n8n-icon",
    "powerautomate": "selfhst:microsoft-power-automate",
    "copilot": "selfhst:microsoft-copilot",
    "m365": "selfhst:microsoft-365",
    "ollama": "selfhst:ollama-light",
    "chatgpt": "selfhst:chatgpt-light",
    "claude": "devicon:claude",
}

ROWS = {
    "languages": "python java cs cpp c js ts swift lua html css sql",
    "frameworks": "react nextjs dotnet flask fastapi nodejs tailwind bootstrap",
    "devops": "docker kubernetes terraform azure aws gcp gitlab linux bash powershell raspberrypi argocd traefik entra grafana",
    "automation": "n8n powerautomate copilot m365 chatgpt claude ollama",
    "databases": "postgres mysql mongodb git github vscode visualstudio",
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req).read().decode()


def prefix_ids(svg, p):
    svg = re.sub(r'id="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', svg)
    svg = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{p}{m.group(1)})", svg)
    return re.sub(r'href="#([^"]+)"', lambda m: f'href="#{p}{m.group(1)}"', svg)


def icon(name):
    if name not in CUSTOM:
        return get(f"https://skillicons.dev/icons?i={name}&theme=dark").split("<g transform")[1].split(">", 1)[1].rsplit("</g>", 1)[0]
    prefix, ident = CUSTOM[name].split(":")
    logo = get(f"https://api.iconify.design/{prefix}/{ident}.svg")
    root, rest = logo.split(">", 1)
    root = re.sub(r'\s(width|height)="[^"]*"', "", root)
    logo = root.replace("<svg", '<svg x="48" y="48" width="160" height="160"', 1) + ">" + rest
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" fill="none" viewBox="0 0 256 256"><rect width="256" height="256" fill="{TILE}" rx="60"/>{logo}</svg>'


for row, names in ROWS.items():
    names = names.split()
    vb = len(names) * 300 - 44
    parts = [
        f'<g transform="translate({i * 300}, 0)">{prefix_ids(icon(n), f"{n}_")}</g>'
        for i, n in enumerate(names)
    ]
    svg = (
        f'<svg width="{vb * 48 / 256:g}" height="48" viewBox="0 0 {vb} 256" fill="none" '
        f'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
        + "".join(parts) + "</svg>\n"
    )
    (OUT / f"{row}.svg").write_text(svg)
    print(row, len(names))
