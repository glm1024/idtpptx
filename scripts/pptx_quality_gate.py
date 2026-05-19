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
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
OOXML_NS = {"p": P_NS["p"], "a": A_NS}
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
EMUS_PER_INCH = 914400
DEFAULT_LOGO_SAFE_WIDTH_IN = 2.7
DEFAULT_LOGO_SAFE_HEIGHT_IN = 1.1
BRAND_SAFE_ZONE_TEXT_RE = re.compile(
    r"^\s*(?:\d{1,3}|inspur|浪潮|inspur\s*浪潮|浪潮\s*inspur)\s*$",
    re.IGNORECASE,
)


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


def slide_size(pptx_path: Path) -> tuple[int, int]:
    try:
        with zipfile.ZipFile(pptx_path) as zf:
            data = zf.read("ppt/presentation.xml")
        root = ET.fromstring(data)
        size = root.find("p:sldSz", P_NS)
        if size is not None:
            return int(size.attrib["cx"]), int(size.attrib["cy"])
    except Exception:
        pass
    return 12192000, 6858000


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


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_emu(value: str | None) -> int:
    if value is None:
        return 0
    try:
        return int(value)
    except ValueError:
        return 0


def xfrm_rect(xfrm: ET.Element) -> tuple[int, int, int, int]:
    off = xfrm.find("a:off", OOXML_NS)
    ext = xfrm.find("a:ext", OOXML_NS)
    return (
        parse_emu(off.attrib.get("x") if off is not None else None),
        parse_emu(off.attrib.get("y") if off is not None else None),
        parse_emu(ext.attrib.get("cx") if ext is not None else None),
        parse_emu(ext.attrib.get("cy") if ext is not None else None),
    )


def find_object_xfrm(element: ET.Element) -> ET.Element | None:
    for path in ("p:xfrm", "p:spPr/a:xfrm", "p:picPr/a:xfrm", "p:grpSpPr/a:xfrm"):
        xfrm = element.find(path, OOXML_NS)
        if xfrm is not None:
            return xfrm
    return None


def object_name(element: ET.Element) -> str:
    c_nv_pr = element.find(".//p:cNvPr", OOXML_NS)
    return c_nv_pr.attrib.get("name", "") if c_nv_pr is not None else ""


def object_text(element: ET.Element) -> str:
    return "".join(text.text or "" for text in element.findall(".//a:t", OOXML_NS)).strip()


def overlaps(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def contains(container: tuple[float, float, float, float], item: tuple[float, float, float, float]) -> bool:
    cx, cy, cw, ch = container
    ix, iy, iw, ih = item
    return ix >= cx and iy >= cy and ix + iw <= cx + cw and iy + ih <= cy + ch


def make_group_transform(
    group_xfrm: ET.Element,
    parent_transform,
):
    group_rect = parent_transform(xfrm_rect(group_xfrm))
    group_x, group_y, group_w, group_h = group_rect
    ch_off = group_xfrm.find("a:chOff", OOXML_NS)
    ch_ext = group_xfrm.find("a:chExt", OOXML_NS)
    ch_x = parse_emu(ch_off.attrib.get("x") if ch_off is not None else None)
    ch_y = parse_emu(ch_off.attrib.get("y") if ch_off is not None else None)
    ch_w = parse_emu(ch_ext.attrib.get("cx") if ch_ext is not None else None)
    ch_h = parse_emu(ch_ext.attrib.get("cy") if ch_ext is not None else None)
    scale_x = group_w / ch_w if ch_w else 1
    scale_y = group_h / ch_h if ch_h else 1

    def transform(rect: tuple[int, int, int, int]) -> tuple[float, float, float, float]:
        x, y, w, h = rect
        return (
            group_x + (x - ch_x) * scale_x,
            group_y + (y - ch_y) * scale_y,
            w * scale_x,
            h * scale_y,
        )

    return transform


def iter_slide_objects(sp_tree: ET.Element, transform=None):
    if transform is None:
        transform = lambda rect: rect

    for child in list(sp_tree):
        tag = local_name(child.tag)
        if tag in {"nvGrpSpPr", "grpSpPr"}:
            continue
        if tag == "grpSp":
            xfrm = find_object_xfrm(child)
            child_transform = make_group_transform(xfrm, transform) if xfrm is not None else transform
            yield from iter_slide_objects(child, child_transform)
            continue
        if tag not in {"sp", "graphicFrame", "pic", "cxnSp"}:
            continue
        xfrm = find_object_xfrm(child)
        if xfrm is None:
            continue
        yield {
            "kind": tag,
            "name": object_name(child),
            "text": object_text(child),
            "rect": transform(xfrm_rect(xfrm)),
        }


def slide_number_from_path(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def is_allowed_safe_zone_object(obj: dict[str, object], safe_zone: tuple[float, float, float, float]) -> bool:
    rect = obj["rect"]
    text = str(obj["text"])
    name = str(obj["name"]).lower()
    if not contains(safe_zone, rect):
        return False
    if BRAND_SAFE_ZONE_TEXT_RE.match(text):
        return True
    if text == "" and any(token in name for token in ("logo", "inspur", "浪潮", "slide number", "page number", "页码")):
        return True
    if obj["kind"] == "pic" and text == "":
        _, _, width, height = rect
        return width <= 2.6 * EMUS_PER_INCH and height <= 0.5 * EMUS_PER_INCH
    return False


def find_logo_safe_zone_issues(
    pptx_path: Path,
    width_in: float = DEFAULT_LOGO_SAFE_WIDTH_IN,
    height_in: float = DEFAULT_LOGO_SAFE_HEIGHT_IN,
) -> list[str]:
    issues: list[str] = []
    slide_w, slide_h = slide_size(pptx_path)
    safe_zone = (
        slide_w - width_in * EMUS_PER_INCH,
        slide_h - height_in * EMUS_PER_INCH,
        width_in * EMUS_PER_INCH,
        height_in * EMUS_PER_INCH,
    )
    try:
        with zipfile.ZipFile(pptx_path) as zf:
            slide_paths = sorted(
                (name for name in zf.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml")),
                key=slide_number_from_path,
            )
            for slide_path in slide_paths:
                root = ET.fromstring(zf.read(slide_path))
                sp_tree = root.find("p:cSld/p:spTree", OOXML_NS)
                if sp_tree is None:
                    continue
                for obj in iter_slide_objects(sp_tree):
                    rect = obj["rect"]
                    if not overlaps(rect, safe_zone):
                        continue
                    if is_allowed_safe_zone_object(obj, safe_zone):
                        continue
                    name = str(obj["name"]) or "(unnamed)"
                    text = str(obj["text"])
                    excerpt = f" text={text[:30]!r}" if text else ""
                    issues.append(f"{slide_path}: {obj['kind']} {name!r}{excerpt}")
    except Exception as exc:
        issues.append(f"could not inspect bottom-right logo safe zone: {exc}")
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
    parser.add_argument("--logo-safe-width-in", type=float, default=DEFAULT_LOGO_SAFE_WIDTH_IN, help="Reserved bottom-right logo safe-zone width in inches")
    parser.add_argument("--logo-safe-height-in", type=float, default=DEFAULT_LOGO_SAFE_HEIGHT_IN, help="Reserved bottom-right logo safe-zone height in inches")
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
    logo_safe_zone_issues = find_logo_safe_zone_issues(
        pptx_path,
        width_in=args.logo_safe_width_in,
        height_in=args.logo_safe_height_in,
    )
    check(
        "bottom-right logo safe zone",
        not logo_safe_zone_issues,
        "ok" if not logo_safe_zone_issues else "; ".join(logo_safe_zone_issues[:20]),
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
