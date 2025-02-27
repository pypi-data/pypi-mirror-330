import json

from markdown_it import MarkdownIt
from nltk.tokenize import sent_tokenize


def sentences(text, num_sentences=5) -> str:
    sentences = sent_tokenize(text)[:num_sentences]
    return " ".join(sentences)


def strip_markdown(text) -> str:
    md = MarkdownIt()
    parsed = md.parse(text)
    return "".join(token.content for token in parsed if token.type == "inline")


def extract_cpe(data) -> list[str]:
    # vulnrichement
    vuln_cpes = []
    if vulnrichment := data.get("vulnerability-lookup:meta", {}).get(
        "vulnrichment", False
    ):
        containers = json.loads(vulnrichment["containers"])

        # Check ADP section
        if "adp" in containers:
            for entry in containers["adp"]:
                if "affected" in entry:
                    for affected in entry["affected"]:
                        if "cpes" in affected:
                            vuln_cpes.extend(affected["cpes"])

        # Check CNA section
        if "cna" in containers and "affected" in containers["cna"]:
            for affected in containers["cna"]["affected"]:
                if "cpes" in affected:
                    vuln_cpes.extend(affected["cpes"])

    # fkie
    if fkie := data.get("vulnerability-lookup:meta", {}).get("fkie_nvd", False):
        if "configurations" in fkie:
            configurations = json.loads(fkie["configurations"])
            for config in configurations:
                if "nodes" in config:
                    for node in config["nodes"]:
                        if "cpeMatch" in node:
                            vuln_cpes.extend(
                                match["criteria"]
                                for match in node["cpeMatch"]
                                if "criteria" in match
                            )

    # default container
    for elem in data["containers"]["cna"]["affected"]:
        if "cpes" in elem:
            vuln_cpes.extend(elem["cpes"])

    vuln_cpes = list(dict.fromkeys(cpe.lower() for cpe in vuln_cpes))
    return vuln_cpes


def format_cvss_version(version: str) -> str:
    return f"cvss_v{version.replace('.', '_')}".lower()


def extract_cvss_cve(data) -> dict[str, float]:
    """
    Extract CVSS scores from a CVE entry, checking multiple sources.

    Args:
        data (dict): The CVE vulnerability data.

    Returns:
        dict[str, float]: A dictionary mapping CVSS version strings to base scores.
    """
    cvss_scores = {}

    # Check in the main CNA metrics section
    for metric in data.get("containers", {}).get("cna", {}).get("metrics", []):
        for key in metric:
            if key.startswith("cvssV") and "baseScore" in metric[key]:
                cvss_scores[format_cvss_version(metric[key]["version"])] = metric[key][
                    "baseScore"
                ]

    # If no CVSS found, check vulnerability-lookup:meta (for embedded NVD JSON)
    if not cvss_scores:
        nvd_meta = data.get("vulnerability-lookup:meta", {}).get("nvd")
        if isinstance(nvd_meta, str):  # Ensure it's a JSON string
            try:
                nvd_data = json.loads(nvd_meta)
                for version, metrics in (
                    nvd_data.get("cve", {}).get("metrics", {}).items()
                ):
                    for key in metrics:
                        if "cvssData" in key and "baseScore" in key["cvssData"]:
                            cvss_scores[
                                format_cvss_version(key["cvssData"]["version"])
                            ] = key["cvssData"]["baseScore"]
            except json.JSONDecodeError:
                pass  # Ignore invalid JSON

    return cvss_scores


def extract_cvss_cve_old(data) -> dict[str, float]:
    cvss_scores = {}

    # Check in the main CNA metrics section
    for metric in data.get("containers", {}).get("cna", {}).get("metrics", []):
        for key in metric:
            if key.startswith("cvssV"):
                cvss_scores[format_cvss_version(metric[key]["version"])] = metric[key][
                    "baseScore"
                ]

    if not cvss_scores:
        # Check in vulnerability-lookup:meta (if embedded NVD JSON exists)
        nvd_meta = data.get("vulnerability-lookup:meta", {}).get("nvd")
        if nvd_meta:
            try:
                nvd_data = json.loads(nvd_meta)
                for version, metric in (
                    nvd_data.get("cve", {}).get("metrics", {}).items()
                ):
                    for key in metric:
                        cvss_scores[format_cvss_version(key["cvssData"]["version"])] = (
                            key["cvssData"]["baseScore"]
                        )
            except json.JSONDecodeError:
                pass  # Handle invalid JSON string in meta

    return cvss_scores


def extract_cvss_from_github_advisory(data) -> dict[str, float]:
    cvss_scores = {}

    # Extract CVSS scores from the 'severity' section
    for severity in data.get("severity", []):
        if severity.get("type", "").startswith("CVSS"):
            cvss_scores[severity["type"].lower()] = severity["score"]

    return cvss_scores
