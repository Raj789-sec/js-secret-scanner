import re
import sys
import base64
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def banner():
    console.print(Panel.fit("[bold magenta]🔍 JavaScript Secret Scanner[/bold magenta]\n[cyan]Coded by Raj ✨[/cyan]", border_style="blue"))

def looks_like_secret(s):
    """Detect high entropy / random-looking strings"""
    if len(s) < 20:
        return False
    charset = len(set(s))
    return charset > 10  # more variation = likely secret

def extract_data(js_content):
    results = {
        "URLs": [],
        "Endpoints": [],
        "API Keys / Secrets": [],
        "S3 Buckets": [],
        "AWS URLs": [],
        "Cloud Keys": [],
        "High-Entropy Strings": [],
        "Sensitive Endpoints": []
    }

    # Regex patterns
    url_pattern = re.compile(r'https?://[^\s\'"<>]+')
    endpoint_pattern = re.compile(r'(/[a-zA-Z0-9_\-\/]+)')
    api_key_pattern = re.compile(r'(?i)(?:api[_-]?key|secret|token|auth)["\']?\s*[:=]\s*["\']([A-Za-z0-9\-\._]{10,})["\']')

    # AWS / Cloud patterns
    s3_pattern = re.compile(r'(?:s3://[a-zA-Z0-9\.\-_]+|[a-zA-Z0-9\.\-_]+\.s3\.amazonaws\.com)')
    aws_url_pattern = re.compile(r'https?://[a-zA-Z0-9\.\-]+\.amazonaws\.com[^\s\'"<>]*')
    aws_key_pattern = re.compile(r'AKIA[0-9A-Z]{16}')
    aws_secret_pattern = re.compile(r'(?<![A-Za-z0-9])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9])')
    gcp_key_pattern = re.compile(r'AIza[0-9A-Za-z\-_]{35}')
    slack_token_pattern = re.compile(r'xox[baprs]-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{24}')
    stripe_key_pattern = re.compile(r'sk_live_[0-9a-zA-Z]{24}')
    github_token_pattern = re.compile(r'gh[pousr]_[A-Za-z0-9]{36}')
    jwt_pattern = re.compile(r'eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}')

    # Sensitive endpoints
    sensitive_endpoints = re.findall(r'/(admin|debug|config|swagger|graphql|internal)[^\s\'"<>]*', js_content)

    # Find matches
    urls = url_pattern.findall(js_content)
    s3_buckets = s3_pattern.findall(js_content)
    aws_urls = aws_url_pattern.findall(js_content)

    # Fill results
    results["URLs"] = sorted(set(urls) - set(aws_urls))
    results["Endpoints"] = sorted(set(endpoint_pattern.findall(js_content)))
    results["API Keys / Secrets"] = sorted(set(api_key_pattern.findall(js_content)))
    results["S3 Buckets"] = sorted(set(s3_buckets))
    results["AWS URLs"] = sorted(set(aws_urls) - set(s3_buckets))
    results["Cloud Keys"] = sorted(set(
        aws_key_pattern.findall(js_content) +
        aws_secret_pattern.findall(js_content) +
        gcp_key_pattern.findall(js_content) +
        slack_token_pattern.findall(js_content) +
        stripe_key_pattern.findall(js_content) +
        github_token_pattern.findall(js_content) +
        jwt_pattern.findall(js_content)
    ))

    # High-entropy detection
    for word in re.findall(r'["\']([A-Za-z0-9+/=]{20,})["\']', js_content):
        if looks_like_secret(word):
            results["High-Entropy Strings"].append(word)

    results["High-Entropy Strings"] = sorted(set(results["High-Entropy Strings"]))
    results["Sensitive Endpoints"] = sorted(set(sensitive_endpoints))

    return results

def pretty_print(extracted):
    for category, items in extracted.items():
        if not items:
            continue

        table = Table(title=f"[cyan]{category}[/cyan]", header_style="bold green")
        table.add_column("No.", justify="center", style="yellow", width=6)
        table.add_column("Value", style="white")

        for i, item in enumerate(items, 1):
            table.add_row(str(i), item)

        console.print(table)
        console.print()  # spacing

def export_json(extracted, out_file="results.json"):
    with open(out_file, "w") as f:
        json.dump(extracted, f, indent=4)
    console.print(f"[green]✅ Results saved to {out_file}[/green]")

def export_html(extracted, out_file="results.html"):
    html = ["<html><head><title>JS Secrets Report</title></head><body>"]
    html.append("<h1>🔍 JavaScript Secret Scanner Report</h1>")
    for category, items in extracted.items():
        if not items:
            continue
        html.append(f"<h2>{category}</h2><ul>")
        for item in items:
            html.append(f"<li>{item}</li>")
        html.append("</ul>")
    html.append("</body></html>")
    with open(out_file, "w") as f:
        f.write("\n".join(html))
    console.print(f"[green]✅ HTML Report saved to {out_file}[/green]")

def main(file_path, mode):
    path = Path(file_path)
    if not path.exists():
        console.print(f"[red]❌ File not found: {file_path}[/red]")
        return

    content = path.read_text(errors="ignore")
    extracted = extract_data(content)

    banner()

    if mode == "console":
        pretty_print(extracted)
    elif mode == "json":
        export_json(extracted)
    elif mode == "html":
        export_html(extracted)
    else:
        console.print("[red]❌ Invalid mode! Use console/json/html[/red]")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        console.print("[yellow]Usage:[/yellow] python js_secret_scanner.py <main.js> <console|json|html>")
    else:
        main(sys.argv[1], sys.argv[2])

