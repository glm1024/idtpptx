#!/usr/bin/env python3
"""Run an idtpptx delivery quality gate for a PowerPoint file.

This script orchestrates checks that agents otherwise tend to run only
partially. It intentionally calls the base pptx skill for OpenXML validation
and LibreOffice rendering when that skill is available.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from posixpath import dirname, normpath
from pathlib import Path
from xml.etree import ElementTree as ET


PLACEHOLDER_RE = re.compile(
    r"项目名称|汇报主题|章节标题|正文页标题|对比表页标题|步骤说明页标题|"
    r"说明页标题|问题说明页标题|截图占位|方案 A|方案 B|对比项|xxxx|lorem|ipsum",
    re.IGNORECASE,
)

P_NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr


def python_candidates(cli_value: str | None) -> list[str]:
    candidates = []
    if cli_value:
        candidates.append(cli_value)
    if os.environ.get("IDTPPTX_PYTHON"):
        candidates.append(os.environ["IDTPPTX_PYTHON"])
    candidates.extend([sys.executable, "python", "python3"])

    seen = set()
    deduped = []
    for candidate in candidates:
        if candidate and candidate not in seen:
            deduped.append(candidate)
            seen.add(candidate)
    return deduped


def python_has_modules(python_cmd: str, modules: list[str]) -> tuple[bool, str]:
    if not modules:
        code = "print('ok')"
    else:
        code = (
            "import importlib.util, sys; "
            f"mods={modules!r}; "
            "missing=[m for m in mods if importlib.util.find_spec(m) is None]; "
            "print(','.join(missing)); "
            "sys.exit(1 if missing else 0)"
        )
    try:
        proc = subprocess.run(
            [python_cmd, "-c", code],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError:
        return False, "not found"
    detail = (proc.stdout or proc.stderr).strip()
    return proc.returncode == 0, detail


def resolve_python(cli_value: str | None, required_modules: list[str]) -> tuple[str | None, str]:
    failures = []
    for candidate in python_candidates(cli_value):
        ok, detail = python_has_modules(candidate, required_modules)
        if ok:
            return candidate, "ok"
        failures.append(f"{candidate}: {detail or 'module check failed'}")
    module_hint = ", ".join(required_modules) if required_modules else "python"
    return None, f"no usable Python for {module_hint}; tried " + "; ".join(failures)


def find_base_pptx_skill(cli_value: str | None) -> Path | None:
    candidates: list[Path] = []
    if cli_value:
        candidates.append(Path(cli_value).expanduser())
    if os.environ.get("PPTX_SKILL_DIR"):
        candidates.append(Path(os.environ["PPTX_SKILL_DIR"]).expanduser())
    candidates.extend(
        [
            Path.home() / ".agents" / "skills" / "pptx",
            Path.home() / ".codex" / "skills" / "pptx",
        ]
    )
    for candidate in candidates:
        validate = candidate / "scripts" / "office" / "validate.py"
        soffice = candidate / "scripts" / "office" / "soffice.py"
        if validate.exists() and soffice.exists():
            return candidate
    return None


def count_slides(pptx_path: Path) -> int | None:
    try:
        with zipfile.ZipFile(pptx_path) as zf:
            data = zf.read("ppt/presentation.xml")
        root = ET.fromstring(data)
        sld_id_lst = root.find("p:sldIdLst", P_NS)
        return 0 if sld_id_lst is None else len(list(sld_id_lst))
    except Exception:
        return None


def has_notes_master_order_issue(pptx_path: Path) -> bool:
    try:
        with zipfile.ZipFile(pptx_path) as zf:
            text = zf.read("ppt/presentation.xml").decode("utf-8", errors="replace")
    except Exception:
        return False
    notes = text.find("<p:notesMasterIdLst")
    slides = text.find("<p:sldIdLst")
    return notes >= 0 and slides >= 0 and notes > slides


def relationship_source_dir(rel_path: str) -> str:
    if rel_path == "_rels/.rels":
        return ""
    owner_part = rel_path.replace("/_rels/", "/")
    if owner_part.endswith(".rels"):
        owner_part = owner_part[:-5]
    return dirname(owner_part)


def find_package_reference_issues(pptx_path: Path) -> tuple[list[str], list[str]]:
    missing_overrides: list[str] = []
    missing_relationships: list[str] = []

    try:
        with zipfile.ZipFile(pptx_path) as zf:
            names = set(zf.namelist())

            content_types = ET.fromstring(zf.read("[Content_Types].xml"))
            for override in content_types.findall(f"{{{CT_NS}}}Override"):
                part_name = override.attrib.get("PartName", "")
                part = part_name.lstrip("/")
                if part and part not in names:
                    missing_overrides.append(part_name)

            rel_paths = sorted(name for name in names if name.endswith(".rels"))
            for rel_path in rel_paths:
                rel_root = ET.fromstring(zf.read(rel_path))
                source_dir = relationship_source_dir(rel_path)
                for rel in rel_root.findall(f"{{{REL_NS}}}Relationship"):
                    target = rel.attrib.get("Target", "")
                    mode = rel.attrib.get("TargetMode")
                    if not target or mode == "External" or target.startswith(("http:", "https:", "mailto:")):
                        continue
                    target_without_fragment = target.split("#", 1)[0]
                    if target_without_fragment.startswith("/"):
                        resolved = target_without_fragment.lstrip("/")
                    else:
                        resolved = normpath(f"{source_dir}/{target_without_fragment}").lstrip("/")
                    if resolved not in names:
                        rel_id = rel.attrib.get("Id", "(no id)")
                        missing_relationships.append(f"{rel_path} {rel_id} -> {target} ({resolved})")
    except Exception as exc:
        return [f"could not inspect package references: {exc}"], []

    return missing_overrides, missing_relationships


def find_negative_extents(pptx_path: Path) -> list[str]:
    issues: list[str] = []
    try:
        with zipfile.ZipFile(pptx_path) as zf:
            for name in zf.namelist():
                if not name.startswith("ppt/slides/slide") or not name.endswith(".xml"):
                    continue
                root = ET.fromstring(zf.read(name))
                for ext in root.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}ext"):
                    cx = ext.attrib.get("cx", "0")
                    cy = ext.attrib.get("cy", "0")
                    if cx.startswith("-") or cy.startswith("-"):
                        issues.append(f"{name}: cx={cx}, cy={cy}")
    except Exception as exc:
        issues.append(f"could not inspect shape extents: {exc}")
    return issues


def find_notes_parts(pptx_path: Path) -> list[str]:
    try:
        with zipfile.ZipFile(pptx_path) as zf:
            return sorted(
                name
                for name in zf.namelist()
                if name.startswith("ppt/notesSlides/") or name.startswith("ppt/notesMasters/")
            )
    except Exception as exc:
        return [f"could not inspect notes parts: {exc}"]


def make_contact_sheet(images: list[Path], output: Path, python_cmd: str) -> tuple[bool, str]:
    code = r"""
from pathlib import Path
import sys
from PIL import Image, ImageDraw

output = Path(sys.argv[1])
image_paths = [Path(item) for item in sys.argv[2:]]
thumbs = []

for image_path in image_paths:
    image = Image.open(image_path).convert("RGB")
    image.thumbnail((520, 293))
    canvas = Image.new("RGB", (560, 350), "white")
    canvas.paste(image, ((560 - image.width) // 2, 40))
    ImageDraw.Draw(canvas).text((20, 12), image_path.name, fill=(0, 0, 0))
    thumbs.append(canvas)

if not thumbs:
    raise SystemExit("no slide images")

cols = 3
rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 560, rows * 350), "white")
for index, thumb in enumerate(thumbs):
    sheet.paste(thumb, ((index % cols) * 560, (index // cols) * 350))
sheet.save(output, quality=92)
"""
    code_status, stdout, stderr = run([python_cmd, "-c", code, str(output), *[str(p) for p in images]])
    return code_status == 0, (stderr or stdout).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run idtpptx PPTX QA checks.")
    parser.add_argument("pptx", type=Path, help="PPTX file to validate")
    parser.add_argument("--pptx-skill-dir", help="Path to the installed base pptx skill")
    parser.add_argument("--python", help="Python command used for helper modules such as markitdown/defusedxml")
    parser.add_argument("--outdir", type=Path, help="Directory for render artifacts")
    parser.add_argument("--skip-render", action="store_true", help="Skip PDF/image rendering")
    parser.add_argument("--allow-notes", action="store_true", help="Allow speaker notes parts in the PPTX package")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args()

    pptx_path = args.pptx.expanduser().resolve()
    outdir = (args.outdir.expanduser().resolve() if args.outdir else Path(tempfile.mkdtemp(prefix="idtpptx-qa-")))
    outdir.mkdir(parents=True, exist_ok=True)

    report: dict[str, object] = {
        "pptx": str(pptx_path),
        "outdir": str(outdir),
        "checks": [],
        "blockers": [],
        "warnings": [],
        "artifacts": {},
    }

    def check(name: str, ok: bool, detail: str = "") -> None:
        report["checks"].append({"name": name, "ok": ok, "detail": detail})
        if not ok:
            report["blockers"].append(f"{name}: {detail}")

    def warn(message: str) -> None:
        report["warnings"].append(message)

    if not pptx_path.exists():
        check("input exists", False, "file not found")
        print_report(report, args.json)
        return 1
    check("input exists", True, f"{pptx_path.stat().st_size} bytes")

    try:
        with zipfile.ZipFile(pptx_path) as zf:
            bad = zf.testzip()
        check("zip package", bad is None, f"first bad entry: {bad}" if bad else "ok")
    except Exception as exc:
        check("zip package", False, str(exc))

    slide_count = count_slides(pptx_path)
    if slide_count is None:
        check("slide count", False, "cannot read ppt/presentation.xml")
    else:
        check("slide count", slide_count > 0, f"{slide_count} slide(s)")

    check(
        "PowerPoint presentation.xml order",
        not has_notes_master_order_issue(pptx_path),
        "p:notesMasterIdLst appears after p:sldIdLst" if has_notes_master_order_issue(pptx_path) else "ok",
    )

    missing_overrides, missing_relationships = find_package_reference_issues(pptx_path)
    check(
        "Content_Types part references",
        not missing_overrides,
        "ok" if not missing_overrides else "; ".join(missing_overrides[:20]),
    )
    check(
        "relationship targets",
        not missing_relationships,
        "ok" if not missing_relationships else "; ".join(missing_relationships[:20]),
    )
    negative_extents = find_negative_extents(pptx_path)
    check(
        "non-negative shape extents",
        not negative_extents,
        "ok" if not negative_extents else "; ".join(negative_extents[:20]),
    )
    notes_parts = find_notes_parts(pptx_path)
    check(
        "notes parts",
        args.allow_notes or not notes_parts,
        "ok" if not notes_parts else f"{len(notes_parts)} note-related part(s); pass --allow-notes only when speaker notes are intentional",
    )

    markitdown_python, python_detail = resolve_python(args.python, ["markitdown"])
    if markitdown_python is None:
        check("text extraction", False, python_detail)
    else:
        report.setdefault("python", {})["markitdown"] = markitdown_python
        code, stdout, stderr = run([markitdown_python, "-m", "markitdown", str(pptx_path)])
        if code == 0:
            text_path = outdir / "text.md"
            text_path.write_text(stdout, encoding="utf-8")
            report["artifacts"]["text"] = str(text_path)
            check("text extraction", True, f"wrote {text_path}")
            hits = [line for line in stdout.splitlines() if PLACEHOLDER_RE.search(line)]
            hit_path = outdir / "placeholder-hits.txt"
            hit_path.write_text("\n".join(hits), encoding="utf-8")
            report["artifacts"]["placeholder_hits"] = str(hit_path)
            check("placeholder scan", not hits, f"{len(hits)} hit(s)")
        else:
            check("text extraction", False, (stderr or stdout).strip() or "markitdown failed")

    base_skill = find_base_pptx_skill(args.pptx_skill_dir)
    if base_skill is None:
        check("base pptx skill", False, "could not find installed pptx skill; pass --pptx-skill-dir or set PPTX_SKILL_DIR")
    else:
        report["base_pptx_skill"] = str(base_skill)
        validate_py = base_skill / "scripts" / "office" / "validate.py"
        validate_python, python_detail = resolve_python(args.python, ["defusedxml"])
        if validate_python is None:
            check("OpenXML validation", False, python_detail)
        else:
            report.setdefault("python", {})["validate"] = validate_python
            code, stdout, stderr = run([validate_python, str(validate_py), str(pptx_path)])
            validation_log = outdir / "validate.log"
            validation_log.write_text(stdout + stderr, encoding="utf-8")
            report["artifacts"]["validate_log"] = str(validation_log)
            check("OpenXML validation", code == 0, (stdout + stderr).strip() or "validate.py failed")

        if not args.skip_render:
            soffice_py = base_skill / "scripts" / "office" / "soffice.py"
            render_python, _ = resolve_python(args.python, [])
            render_python = render_python or validate_python or markitdown_python or sys.executable
            report.setdefault("python", {})["render"] = render_python
            code, stdout, stderr = run(
                [
                    render_python,
                    str(soffice_py),
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    str(outdir),
                    str(pptx_path),
                ]
            )
            render_log = outdir / "render.log"
            render_log.write_text(stdout + stderr, encoding="utf-8")
            report["artifacts"]["render_log"] = str(render_log)
            pdf_path = outdir / f"{pptx_path.stem}.pdf"
            check("PDF render", code == 0 and pdf_path.exists(), (stdout + stderr).strip() or str(pdf_path))

            if pdf_path.exists():
                pdftoppm = shutil.which("pdftoppm")
                if pdftoppm is None:
                    check("slide image render", False, "pdftoppm not found")
                else:
                    prefix = outdir / "slide"
                    code, stdout, stderr = run([pdftoppm, "-jpeg", "-r", "150", str(pdf_path), str(prefix)])
                    images = sorted(outdir.glob("slide-*.jpg"))
                    report["artifacts"]["slide_images"] = [str(p) for p in images]
                    expected = slide_count or 0
                    ok = code == 0 and bool(images) and (expected == 0 or len(images) == expected)
                    detail = f"{len(images)} image(s); expected {expected}" if expected else f"{len(images)} image(s)"
                    check("slide image render", ok, detail)
                    if images:
                        contact_sheet = outdir / "contact-sheet.jpg"
                        pillow_python, pillow_detail = resolve_python(args.python, ["PIL"])
                        if pillow_python is None:
                            warn(f"Pillow is unavailable; contact sheet was not generated. {pillow_detail}")
                        else:
                            report.setdefault("python", {})["pillow"] = pillow_python
                        contact_ok = False
                        contact_detail = ""
                        if pillow_python:
                            contact_ok, contact_detail = make_contact_sheet(images, contact_sheet, pillow_python)
                        if contact_ok:
                            report["artifacts"]["contact_sheet"] = str(contact_sheet)
                            check("contact sheet", True, str(contact_sheet))
                        else:
                            warn(f"Contact sheet was not generated; inspect the individual slide images. {contact_detail}".strip())

    if not args.skip_render:
        warn("Automated checks do not replace visual inspection. Inspect rendered slides or contact-sheet.jpg before delivery.")

    print_report(report, args.json)
    return 1 if report["blockers"] else 0


def print_report(report: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print(f"PPTX: {report['pptx']}")
    print(f"Artifacts: {report['outdir']}")
    for item in report["checks"]:
        status = "PASS" if item["ok"] else "BLOCK"
        print(f"[{status}] {item['name']}: {item['detail']}")
    if report["warnings"]:
        print("\nWarnings:")
        for message in report["warnings"]:
            print(f"- {message}")
    if report["blockers"]:
        print("\nBlocking issues:")
        for message in report["blockers"]:
            print(f"- {message}")
    else:
        print("\nAutomated QA passed. Do the final visual inspection before delivery.")


if __name__ == "__main__":
    raise SystemExit(main())
