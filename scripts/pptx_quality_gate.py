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
PROCESS_LEAK_RE = re.compile(
    r"初版目标与讨论范围|初版.{0,8}(讨论范围|目标)|"
    r"可讨论\s*PPT|可讨论的?结构草稿|结构草稿|形成一版可讨论|"
    r"后续.{0,8}(逐页)?补(充|齐).{0,8}(数据|截图|真实)|"
    r"本轮.{0,6}不展开|先不展开|不追求最终视觉定稿|最终视觉定稿|"
    r"先把主线讲顺.{0,12}证据补齐|先统一(口径|路径).{0,12}再讨论(实现)?细节",
    re.IGNORECASE,
)
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
ENGLISH_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_+-]*")

P_NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
OOXML_NS = {"p": P_NS["p"], "a": A_NS}
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
EMUS_PER_INCH = 914400
DEFAULT_LOGO_PADDING_IN = 0.06
EDGE_TOLERANCE_IN = 0.02
NEAR_EDGE_IN = 0.06
LOGO_WARNING_PADDING_IN = 0.30
LOGO_METADATA_RE = re.compile(r"logo|inspur|浪潮|标志", re.IGNORECASE)
WHITE_FILL_VALUES = {"FFFFFF", "FDFDFD", "FAFAFA"}
WHITE_SCHEME_VALUES = {"bg1", "lt1"}
PLACEHOLDER_FILL_VALUES = {"FFFFFF", "FDFDFD", "FAFAFA", "F2F2F2", "F5F5F5", "EFEFEF", "EDEDED"}
MUTED_TEXT_LUMA_THRESHOLD = 80
MUTED_TEXT_CHANNEL_SPREAD = 50
THEME_CONTRACT_REF = "references/theme-contract.md"
THEME_TEXT_COLOR_VALUES = {
    "000000",
    "111111",
    "1F2933",
    "202020",
    "213261",
    "0062AC",
    "00518E",
    "FFFFFF",
    "D93025",
    "C00000",
    "FF4B4B",
    "FF0000",
    "2E7D32",
    "70AD47",
    "FFC000",
    "D6B656",
}
THEME_FILL_COLOR_VALUES = THEME_TEXT_COLOR_VALUES | {
    "FAFAFA",
    "FDFDFD",
    "F2F2F2",
    "F2F4F7",
    "EDEDED",
    "F5F5F5",
    "A4A3A4",
    "D9D9D9",
    "BBE0E3",
}
ALLOWED_FONT_KEYWORDS = ("微软雅黑", "microsoft yahei", "yahei")
ALLOWED_MONOSPACE_FONTS = {
    "consolas",
    "menlo",
    "monaco",
    "courier new",
    "courier",
    "sfmono-regular",
}
THEME_FILL_WARNING_MIN_AREA = EMUS_PER_INCH * EMUS_PER_INCH * 0.25
CHINESE_FIRST_REF = "references/writing-style.md"
CHINESE_FIRST_ALLOWED_ENGLISH = {
    "ai",
    "api",
    "bi",
    "crm",
    "erp",
    "etl",
    "excel",
    "git",
    "http",
    "https",
    "ide",
    "idt",
    "inspur",
    "ip",
    "json",
    "kpi",
    "ldap",
    "mac",
    "oa",
    "okr",
    "pc",
    "pdf",
    "ppt",
    "pptx",
    "sql",
    "sso",
    "ui",
    "url",
    "xml",
    "word",
    "commit",
}
TEXT_OVERLAP_MIN_WIDTH = EMUS_PER_INCH * 0.20
TEXT_OVERLAP_MIN_HEIGHT = EMUS_PER_INCH * 0.10
TEXT_OVERLAP_MIN_AREA = EMUS_PER_INCH * EMUS_PER_INCH * 0.03
TEXT_OVERLAP_MIN_RATIO = 0.12


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


def presentation_rels(pptx_path: Path) -> dict[str, str]:
    rels: dict[str, str] = {}
    try:
        with zipfile.ZipFile(pptx_path) as zf:
            root = ET.fromstring(zf.read("ppt/_rels/presentation.xml.rels"))
            for rel in root.findall(f"{{{REL_NS}}}Relationship"):
                rel_id = rel.attrib.get("Id", "")
                target = rel.attrib.get("Target", "")
                if rel_id and target:
                    rels[rel_id] = normpath(f"ppt/{target}").lstrip("/")
    except Exception:
        return {}
    return rels


def slide_paths_in_order(pptx_path: Path) -> list[str]:
    try:
        with zipfile.ZipFile(pptx_path) as zf:
            root = ET.fromstring(zf.read("ppt/presentation.xml"))
        rels = presentation_rels(pptx_path)
        sld_id_lst = root.find("p:sldIdLst", P_NS)
        if sld_id_lst is None:
            return []
        ordered: list[str] = []
        for slide_id in list(sld_id_lst):
            rel_id = slide_id.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            if rel_id and rel_id in rels:
                ordered.append(rels[rel_id])
        return ordered
    except Exception:
        return []


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


def object_description(element: ET.Element) -> str:
    c_nv_pr = element.find(".//p:cNvPr", OOXML_NS)
    return c_nv_pr.attrib.get("descr", "") if c_nv_pr is not None else ""


def object_text(element: ET.Element) -> str:
    return "".join(text.text or "" for text in element.findall(".//a:t", OOXML_NS)).strip()


def solid_fill_value(solid: ET.Element) -> str:
    srgb = solid.find("a:srgbClr", OOXML_NS)
    if srgb is not None:
        return srgb.attrib.get("val", "").upper()
    scheme = solid.find("a:schemeClr", OOXML_NS)
    if scheme is not None:
        return f"scheme:{scheme.attrib.get('val', '')}"
    return "solid"


def object_fill(element: ET.Element) -> str:
    sp_pr = element.find("p:spPr", OOXML_NS)
    if sp_pr is None:
        return ""
    if sp_pr.find("a:noFill", OOXML_NS) is not None:
        return ""
    solid = sp_pr.find("a:solidFill", OOXML_NS)
    if solid is None:
        return ""
    return solid_fill_value(solid)


def object_text_colors(element: ET.Element) -> list[str]:
    colors: list[str] = []
    for path in (".//a:rPr/a:solidFill", ".//a:endParaRPr/a:solidFill", ".//a:defRPr/a:solidFill"):
        for solid in element.findall(path, OOXML_NS):
            color = solid_fill_value(solid)
            if color:
                colors.append(color)
    return colors


def object_font_faces(element: ET.Element) -> list[str]:
    fonts: list[str] = []
    for font_node in element.findall(".//a:latin", OOXML_NS):
        typeface = font_node.attrib.get("typeface", "").strip()
        if typeface:
            fonts.append(typeface)
    for font_node in element.findall(".//a:ea", OOXML_NS):
        typeface = font_node.attrib.get("typeface", "").strip()
        if typeface:
            fonts.append(typeface)
    for font_node in element.findall(".//a:cs", OOXML_NS):
        typeface = font_node.attrib.get("typeface", "").strip()
        if typeface:
            fonts.append(typeface)
    return sorted(set(fonts))


def overlaps(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def rect_intersection(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    x1 = max(ax, bx)
    y1 = max(ay, by)
    x2 = min(ax + aw, bx + bw)
    y2 = min(ay + ah, by + bh)
    return x1, y1, max(0, x2 - x1), max(0, y2 - y1)


def inches(value: float) -> float:
    return value * EMUS_PER_INCH


def rect_area(rect: tuple[float, float, float, float]) -> float:
    _x, _y, width, height = rect
    return max(0, width) * max(0, height)


def rect_label(obj: dict[str, object]) -> str:
    name = str(obj.get("name", "")) or "(unnamed)"
    text = str(obj.get("text", ""))
    if text:
        return f"{name!r} text={text[:30]!r}"
    return repr(name)


def is_significant_edge_object(obj: dict[str, object]) -> bool:
    if obj["kind"] in {"pic", "graphicFrame"}:
        return True
    return bool(str(obj.get("text", "")).strip())


def is_large_background_like(rect: tuple[float, float, float, float], slide_w: int, slide_h: int) -> bool:
    x, y, width, height = rect
    return (
        x <= inches(0.05)
        and y <= inches(0.05)
        and width >= slide_w * 0.9
        and height >= slide_h * 0.9
    )


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
            "description": object_description(child),
            "text": object_text(child),
            "fill": object_fill(child),
            "text_colors": object_text_colors(child),
            "fonts": object_font_faces(child),
            "rect": transform(xfrm_rect(xfrm)),
        }


def slide_number_from_path(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def is_bottom_right_logo_like_picture(obj: dict[str, object], slide_w: int, slide_h: int) -> bool:
    if obj["kind"] != "pic" or str(obj["text"]):
        return False
    x, y, width, height = obj["rect"]
    if width <= 0 or height <= 0:
        return False
    aspect_ratio = width / height
    return (
        0.5 * EMUS_PER_INCH <= width <= 3.2 * EMUS_PER_INCH
        and 0.12 * EMUS_PER_INCH <= height <= 0.8 * EMUS_PER_INCH
        and aspect_ratio >= 3
        and x >= slide_w * 0.55
        and y >= slide_h * 0.8
        and x + width >= slide_w - 0.45 * EMUS_PER_INCH
        and y + height >= slide_h - 0.25 * EMUS_PER_INCH
    )


def is_logo_object(obj: dict[str, object], slide_w: int, slide_h: int) -> bool:
    text = str(obj["text"])
    name = str(obj["name"]).lower()
    description = str(obj.get("description", "")).lower()
    if obj["kind"] == "pic" and text == "" and LOGO_METADATA_RE.search(f"{name} {description}"):
        return True
    if is_bottom_right_logo_like_picture(obj, slide_w, slide_h):
        return True
    return False


def padded_rect(
    rect: tuple[float, float, float, float],
    padding_in: float,
    slide_w: int,
    slide_h: int,
) -> tuple[float, float, float, float]:
    x, y, width, height = rect
    padding = padding_in * EMUS_PER_INCH
    x1 = max(0, x - padding)
    y1 = max(0, y - padding)
    x2 = min(slide_w, x + width + padding)
    y2 = min(slide_h, y + height + padding)
    return x1, y1, max(0, x2 - x1), max(0, y2 - y1)


def related_part_path(zf: zipfile.ZipFile, source_path: str, relationship_suffix: str) -> str | None:
    rel_path = f"{dirname(source_path)}/_rels/{Path(source_path).name}.rels"
    try:
        root = ET.fromstring(zf.read(rel_path))
    except Exception:
        return None
    for rel in root.findall(f"{{{REL_NS}}}Relationship"):
        rel_type = rel.attrib.get("Type", "")
        target = rel.attrib.get("Target", "")
        if rel_type.endswith(relationship_suffix) and target:
            return normpath(f"{dirname(source_path)}/{target}").lstrip("/")
    return None


def related_layout_path(zf: zipfile.ZipFile, slide_path: str) -> str | None:
    return related_part_path(zf, slide_path, "/slideLayout")


def related_master_path(zf: zipfile.ZipFile, layout_path: str) -> str | None:
    return related_part_path(zf, layout_path, "/slideMaster")


def layout_shows_master_shapes(zf: zipfile.ZipFile, layout_path: str) -> bool:
    try:
        root = ET.fromstring(zf.read(layout_path))
    except Exception:
        return True
    return root.attrib.get("showMasterSp") != "0"


def logo_source_paths(zf: zipfile.ZipFile, slide_path: str) -> list[str]:
    paths = [slide_path]
    layout_path = related_layout_path(zf, slide_path)
    if layout_path:
        paths.append(layout_path)
        if layout_shows_master_shapes(zf, layout_path):
            master_path = related_master_path(zf, layout_path)
            if master_path:
                paths.append(master_path)
    return paths


def logo_protection_rects(
    zf: zipfile.ZipFile,
    slide_path: str,
    slide_w: int,
    slide_h: int,
    padding_in: float,
) -> list[tuple[float, float, float, float]]:
    rects: list[tuple[float, float, float, float]] = []
    for path in logo_source_paths(zf, slide_path):
        if path not in zf.namelist():
            continue
        root = ET.fromstring(zf.read(path))
        sp_tree = root.find("p:cSld/p:spTree", OOXML_NS)
        if sp_tree is None:
            continue
        for obj in iter_slide_objects(sp_tree):
            if is_logo_object(obj, slide_w, slide_h):
                rects.append(padded_rect(obj["rect"], padding_in, slide_w, slide_h))

    return rects


def find_logo_overlap_issues(
    pptx_path: Path,
    padding_in: float = DEFAULT_LOGO_PADDING_IN,
) -> list[str]:
    issues: list[str] = []
    slide_w, slide_h = slide_size(pptx_path)
    try:
        with zipfile.ZipFile(pptx_path) as zf:
            slide_paths = sorted(
                (name for name in zf.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml")),
                key=slide_number_from_path,
            )
            for slide_path in slide_paths:
                logo_rects = logo_protection_rects(
                    zf,
                    slide_path,
                    slide_w,
                    slide_h,
                    padding_in,
                )
                if not logo_rects:
                    continue
                root = ET.fromstring(zf.read(slide_path))
                sp_tree = root.find("p:cSld/p:spTree", OOXML_NS)
                if sp_tree is None:
                    continue
                for obj in iter_slide_objects(sp_tree):
                    if is_logo_object(obj, slide_w, slide_h):
                        continue
                    rect = obj["rect"]
                    if not any(overlaps(rect, logo_rect) for logo_rect in logo_rects):
                        continue
                    name = str(obj["name"]) or "(unnamed)"
                    text = str(obj["text"])
                    excerpt = f" text={text[:30]!r}" if text else ""
                    issues.append(f"{slide_path}: {obj['kind']} {name!r}{excerpt} overlaps logo")
    except Exception as exc:
        issues.append(f"could not inspect bottom-right logo overlap: {exc}")
    return issues


def is_white_fill(fill: str) -> bool:
    if not fill:
        return False
    if fill.startswith("scheme:"):
        return fill.split(":", 1)[1] in WHITE_SCHEME_VALUES
    return fill.upper() in WHITE_FILL_VALUES


def find_cover_white_panel_issues(pptx_path: Path) -> list[str]:
    issues: list[str] = []
    slide_paths = slide_paths_in_order(pptx_path)
    first_slide = slide_paths[0] if slide_paths else "ppt/slides/slide1.xml"

    try:
        with zipfile.ZipFile(pptx_path) as zf:
            paths = [first_slide]
            layout_path = related_layout_path(zf, first_slide)
            if layout_path:
                paths.append(layout_path)
            for path in paths:
                if path not in zf.namelist():
                    continue
                root = ET.fromstring(zf.read(path))
                sp_tree = root.find("p:cSld/p:spTree", OOXML_NS)
                if sp_tree is None:
                    continue
                for obj in iter_slide_objects(sp_tree):
                    fill = str(obj.get("fill", ""))
                    if not is_white_fill(fill):
                        continue
                    x, y, width, height = obj["rect"]
                    if width < 0.6 * EMUS_PER_INCH or height < 0.25 * EMUS_PER_INCH:
                        continue
                    name = str(obj["name"]) or "(unnamed)"
                    text = str(obj["text"])
                    excerpt = f" text={text[:30]!r}" if text else ""
                    issues.append(f"{path}: {obj['kind']} {name!r} fill={fill}{excerpt}")
    except Exception as exc:
        issues.append(f"could not inspect cover white panels: {exc}")
    return issues


def parse_hex_rgb(color: str) -> tuple[int, int, int] | None:
    if len(color) != 6 or not re.fullmatch(r"[0-9A-Fa-f]{6}", color):
        return None
    return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)


def is_muted_gray_text_color(color: str) -> bool:
    if not color or color.startswith("scheme:"):
        return False
    if color.upper() in WHITE_FILL_VALUES:
        return False
    rgb = parse_hex_rgb(color)
    if rgb is None:
        return False
    r, g, b = rgb
    channel_spread = max(rgb) - min(rgb)
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return channel_spread <= MUTED_TEXT_CHANNEL_SPREAD and luma >= MUTED_TEXT_LUMA_THRESHOLD


def explicit_hex_color(color: str) -> str | None:
    if not color or color.startswith("scheme:"):
        return None
    value = color.strip().lstrip("#").upper()
    return value if parse_hex_rgb(value) is not None else None


def color_luma(color: str) -> float | None:
    rgb = parse_hex_rgb(color)
    if rgb is None:
        return None
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def color_spread(color: str) -> int | None:
    rgb = parse_hex_rgb(color)
    if rgb is None:
        return None
    return max(rgb) - min(rgb)


def is_allowed_theme_text_color(color: str) -> bool:
    value = explicit_hex_color(color)
    return value is None or value in THEME_TEXT_COLOR_VALUES


def is_allowed_theme_fill_color(color: str) -> bool:
    value = explicit_hex_color(color)
    return value is None or value in THEME_FILL_COLOR_VALUES


def normalize_font_face(font: str) -> str:
    return re.sub(r"\s+", " ", font.strip()).lower()


def is_allowed_font_face(font: str) -> bool:
    raw = font.strip()
    normalized = normalize_font_face(raw)
    if not normalized:
        return True
    if any(keyword in normalized for keyword in ALLOWED_FONT_KEYWORDS):
        return True
    if raw and any(keyword in raw for keyword in ALLOWED_FONT_KEYWORDS):
        return True
    return normalized in ALLOWED_MONOSPACE_FONTS


def is_theme_font_reference(font: str) -> bool:
    return normalize_font_face(font).startswith("+")


def english_tokens(text: str) -> list[str]:
    return ENGLISH_TOKEN_RE.findall(text)


def is_camel_case_token(token: str) -> bool:
    return bool(re.search(r"[a-z][A-Z]", token))


def is_allowed_chinese_first_english(token: str) -> bool:
    normalized = token.strip("_+-").lower()
    if not normalized:
        return True
    if normalized in CHINESE_FIRST_ALLOWED_ENGLISH:
        return True
    return token.isupper() and 2 <= len(token) <= 8


def should_warn_chinese_first(text: str) -> tuple[bool, list[str]]:
    tokens = english_tokens(text)
    if not tokens:
        return False, []
    unapproved = [token for token in tokens if not is_allowed_chinese_first_english(token)]
    if not unapproved:
        return False, []

    has_cjk = bool(CJK_RE.search(text))
    if has_cjk:
        warning_weight = len(tokens) >= 2 or any(len(token) >= 8 or is_camel_case_token(token) for token in unapproved)
        return warning_weight, unapproved
    return len(tokens) >= 2, unapproved


def find_chinese_first_warnings(pptx_path: Path) -> list[str]:
    warnings: list[str] = []
    slide_w, slide_h = slide_size(pptx_path)
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
                    if is_logo_object(obj, slide_w, slide_h):
                        continue
                    text = str(obj.get("text", "")).strip()
                    if not text or PLACEHOLDER_RE.search(text) or PROCESS_LEAK_RE.search(text):
                        continue
                    should_warn, terms = should_warn_chinese_first(text)
                    if not should_warn:
                        continue
                    unique_terms = sorted(dict.fromkeys(terms), key=str.lower)
                    warnings.append(
                        f"{slide_path}: Chinese-first wording warning on {obj['kind']} {rect_label(obj)} "
                        f"english_terms={','.join(unique_terms[:8])}; prefer Chinese labels per {CHINESE_FIRST_REF}"
                    )
    except Exception as exc:
        warnings.append(f"could not inspect Chinese-first wording: {exc}")
    return warnings


def find_muted_text_color_issues(pptx_path: Path) -> list[str]:
    issues: list[str] = []
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
                    text = str(obj["text"])
                    if not text:
                        continue
                    if PLACEHOLDER_RE.search(text):
                        continue
                    colors = sorted({str(color) for color in obj.get("text_colors", [])})
                    muted = [color for color in colors if is_muted_gray_text_color(color)]
                    if not muted:
                        continue
                    name = str(obj["name"]) or "(unnamed)"
                    excerpt = f" text={text[:30]!r}" if text else ""
                    issues.append(f"{slide_path}: {obj['kind']} {name!r} muted_text={','.join(muted)}{excerpt}")
    except Exception as exc:
        issues.append(f"could not inspect muted gray text colors: {exc}")
    return issues


def find_theme_drift_warnings(pptx_path: Path) -> list[str]:
    warnings: list[str] = []
    slide_w, slide_h = slide_size(pptx_path)

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
                    if obj["kind"] == "pic" or is_logo_object(obj, slide_w, slide_h):
                        continue

                    text = str(obj.get("text", "")).strip()
                    if text and not PLACEHOLDER_RE.search(text):
                        fonts = sorted({str(font) for font in obj.get("fonts", [])})
                        theme_font_refs = [font for font in fonts if is_theme_font_reference(font)]
                        unexpected_fonts = [
                            font
                            for font in fonts
                            if not is_theme_font_reference(font) and not is_allowed_font_face(font)
                        ]
                        if not fonts:
                            warnings.append(
                                f"{slide_path}: theme drift font on {obj['kind']} {rect_label(obj)} "
                                f"has no explicit font; set YaHei per {THEME_CONTRACT_REF}"
                            )
                        if theme_font_refs:
                            warnings.append(
                                f"{slide_path}: theme drift font on {obj['kind']} {rect_label(obj)} "
                                f"uses theme font reference={','.join(theme_font_refs)}; check {THEME_CONTRACT_REF}"
                            )
                        if unexpected_fonts:
                            warnings.append(
                                f"{slide_path}: theme drift font on {obj['kind']} {rect_label(obj)} "
                                f"fonts={','.join(unexpected_fonts)}; check {THEME_CONTRACT_REF}"
                            )

                        colors = sorted({str(color) for color in obj.get("text_colors", [])})
                        unexpected_colors = [color for color in colors if not is_allowed_theme_text_color(color)]
                        if unexpected_colors:
                            warnings.append(
                                f"{slide_path}: theme drift text color on {obj['kind']} {rect_label(obj)} "
                                f"colors={','.join(unexpected_colors)}; check {THEME_CONTRACT_REF}"
                            )

                    fill = str(obj.get("fill", ""))
                    fill_hex = explicit_hex_color(fill)
                    if fill_hex is None:
                        continue

                    rect = obj["rect"]
                    fill_area = rect_area(rect)
                    luma = color_luma(fill_hex)
                    spread = color_spread(fill_hex)
                    large_theme_background = is_large_background_like(rect, slide_w, slide_h) and (
                        (luma is not None and luma < 80) or (spread is not None and spread > 95)
                    )
                    if large_theme_background:
                        warnings.append(
                            f"{slide_path}: large dark/high-saturation background may be non-IDT theme "
                            f"fill={fill_hex}; check {THEME_CONTRACT_REF}"
                        )
                        continue

                    if not is_allowed_theme_fill_color(fill) and fill_area >= THEME_FILL_WARNING_MIN_AREA:
                        warnings.append(
                            f"{slide_path}: theme drift fill on {obj['kind']} {rect_label(obj)} "
                            f"fill={fill_hex}; check {THEME_CONTRACT_REF}"
                        )
    except Exception as exc:
        warnings.append(f"could not inspect theme drift: {exc}")

    return warnings


def find_edge_warnings(pptx_path: Path) -> list[str]:
    warnings: list[str] = []
    slide_w, slide_h = slide_size(pptx_path)
    off_tolerance = inches(EDGE_TOLERANCE_IN)
    near_edge = inches(NEAR_EDGE_IN)

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
                    if is_logo_object(obj, slide_w, slide_h):
                        continue
                    rect = obj["rect"]
                    x, y, width, height = rect
                    if width <= 0 or height <= 0:
                        continue

                    off_slide = (
                        x < -off_tolerance
                        or y < -off_tolerance
                        or x + width > slide_w + off_tolerance
                        or y + height > slide_h + off_tolerance
                    )
                    if off_slide:
                        warnings.append(f"{slide_path}: {obj['kind']} {rect_label(obj)} extends outside slide bounds")
                        continue

                    if not is_significant_edge_object(obj):
                        continue
                    if is_large_background_like(rect, slide_w, slide_h):
                        continue
                    near = x < near_edge or y < near_edge or slide_w - (x + width) < near_edge or slide_h - (y + height) < near_edge
                    if near:
                        warnings.append(f"{slide_path}: {obj['kind']} {rect_label(obj)} is very close to slide edge")
    except Exception as exc:
        warnings.append(f"could not inspect slide edge risks: {exc}")

    return warnings


def find_text_overlap_warnings(pptx_path: Path) -> list[str]:
    warnings: list[str] = []
    slide_w, slide_h = slide_size(pptx_path)
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
                text_objects: list[dict[str, object]] = []
                for obj in iter_slide_objects(sp_tree):
                    text = str(obj.get("text", "")).strip()
                    if not text or PLACEHOLDER_RE.search(text) or PROCESS_LEAK_RE.search(text):
                        continue
                    if is_logo_object(obj, slide_w, slide_h):
                        continue
                    rect = obj["rect"]
                    if rect_area(rect) <= 0:
                        continue
                    text_objects.append(obj)
                for idx, left in enumerate(text_objects):
                    for right in text_objects[idx + 1 :]:
                        ix, iy, iw, ih = rect_intersection(left["rect"], right["rect"])
                        intersection_area = iw * ih
                        if iw < TEXT_OVERLAP_MIN_WIDTH or ih < TEXT_OVERLAP_MIN_HEIGHT:
                            continue
                        if intersection_area < TEXT_OVERLAP_MIN_AREA:
                            continue
                        smaller_area = min(rect_area(left["rect"]), rect_area(right["rect"]))
                        if smaller_area <= 0 or intersection_area / smaller_area < TEXT_OVERLAP_MIN_RATIO:
                            continue
                        warnings.append(
                            f"{slide_path}: possible editable text overlap between {rect_label(left)} "
                            f"and {rect_label(right)}; inspect render"
                        )
    except Exception as exc:
        warnings.append(f"could not inspect editable text overlap: {exc}")
    return warnings


def find_slide_risk_warnings(pptx_path: Path) -> list[str]:
    warnings: list[str] = []
    slide_w, slide_h = slide_size(pptx_path)

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
                objects = list(iter_slide_objects(sp_tree))
                picture_count = sum(1 for obj in objects if obj["kind"] == "pic" and not is_logo_object(obj, slide_w, slide_h))
                graphic_count = sum(1 for obj in objects if obj["kind"] == "graphicFrame")
                text_count = sum(1 for obj in objects if str(obj.get("text", "")).strip())
                empty_filled = [
                    obj
                    for obj in objects
                    if obj["kind"] == "sp"
                    and not str(obj.get("text", "")).strip()
                    and str(obj.get("fill", "")).upper() in PLACEHOLDER_FILL_VALUES
                    and rect_area(obj["rect"]) >= inches(1.0) * inches(0.45)
                    and not is_large_background_like(obj["rect"], slide_w, slide_h)
                ]

                reasons: list[str] = []
                if picture_count >= 2:
                    reasons.append(f"{picture_count} non-logo images")
                if len(objects) >= 30:
                    reasons.append(f"{len(objects)} positioned objects")
                if graphic_count >= 1 and text_count >= 8:
                    reasons.append("table/chart plus dense text")
                if empty_filled:
                    reasons.append(f"{len(empty_filled)} large empty filled shape(s)")

                logo_warning_rects = logo_protection_rects(
                    zf,
                    slide_path,
                    slide_w,
                    slide_h,
                    LOGO_WARNING_PADDING_IN,
                )
                if logo_warning_rects:
                    near_logo = [
                        obj
                        for obj in objects
                        if not is_logo_object(obj, slide_w, slide_h)
                        and any(overlaps(obj["rect"], logo_rect) for logo_rect in logo_warning_rects)
                    ]
                    if near_logo:
                        reasons.append(f"{len(near_logo)} object(s) near bottom-right logo")

                if reasons:
                    warnings.append(f"{slide_path}: high-risk visual inspection recommended ({'; '.join(reasons)})")
    except Exception as exc:
        warnings.append(f"could not inspect high-risk slides: {exc}")

    return warnings


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
    parser.add_argument("--logo-padding-in", type=float, default=DEFAULT_LOGO_PADDING_IN, help="Padding around the detected bottom-right logo in inches")
    parser.add_argument("--logo-safe-width-in", type=float, help=argparse.SUPPRESS)
    parser.add_argument("--logo-safe-height-in", type=float, help=argparse.SUPPRESS)
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
    logo_overlap_issues = find_logo_overlap_issues(
        pptx_path,
        padding_in=args.logo_padding_in,
    )
    check(
        "bottom-right logo overlap",
        not logo_overlap_issues,
        "ok" if not logo_overlap_issues else "; ".join(logo_overlap_issues[:20]),
    )
    cover_white_panel_issues = find_cover_white_panel_issues(pptx_path)
    check(
        "cover white panels",
        not cover_white_panel_issues,
        "ok" if not cover_white_panel_issues else "; ".join(cover_white_panel_issues[:20]),
    )
    muted_text_color_issues = find_muted_text_color_issues(pptx_path)
    check(
        "muted gray text colors",
        not muted_text_color_issues,
        "ok" if not muted_text_color_issues else "; ".join(muted_text_color_issues[:20]),
    )
    notes_parts = find_notes_parts(pptx_path)
    check(
        "notes parts",
        args.allow_notes or not notes_parts,
        "ok" if not notes_parts else f"{len(notes_parts)} note-related part(s); pass --allow-notes only when speaker notes are intentional",
    )

    edge_warnings = find_edge_warnings(pptx_path)
    for message in edge_warnings[:20]:
        warn(message)
    if len(edge_warnings) > 20:
        warn(f"{len(edge_warnings) - 20} additional slide edge warning(s) omitted")

    risk_warnings = find_slide_risk_warnings(pptx_path)
    for message in risk_warnings[:20]:
        warn(message)
    if len(risk_warnings) > 20:
        warn(f"{len(risk_warnings) - 20} additional high-risk slide warning(s) omitted")

    theme_warnings = find_theme_drift_warnings(pptx_path)
    for message in theme_warnings[:20]:
        warn(message)
    if len(theme_warnings) > 20:
        warn(f"{len(theme_warnings) - 20} additional theme drift warning(s) omitted")

    chinese_first_warnings = find_chinese_first_warnings(pptx_path)
    for message in chinese_first_warnings[:20]:
        warn(message)
    if len(chinese_first_warnings) > 20:
        warn(f"{len(chinese_first_warnings) - 20} additional Chinese-first wording warning(s) omitted")

    text_overlap_warnings = find_text_overlap_warnings(pptx_path)
    for message in text_overlap_warnings[:20]:
        warn(message)
    if len(text_overlap_warnings) > 20:
        warn(f"{len(text_overlap_warnings) - 20} additional editable text overlap warning(s) omitted")

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
            process_hits = [line for line in stdout.splitlines() if PROCESS_LEAK_RE.search(line)]
            process_hit_path = outdir / "process-leak-hits.txt"
            process_hit_path.write_text("\n".join(process_hits), encoding="utf-8")
            report["artifacts"]["process_leak_hits"] = str(process_hit_path)
            check("deck-drafting process leakage", not process_hits, f"{len(process_hits)} hit(s)")
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
