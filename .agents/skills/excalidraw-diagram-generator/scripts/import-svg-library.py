#!/usr/bin/env python3
"""Convert a directory of simple SVG icons into an Excalidraw library.

Paths are flattened into filled Excalidraw line polygons. This keeps the
library self-contained; SVG rasterization is intentionally not used because
library items cannot carry the binary files required by image elements.
"""

import argparse
import hashlib
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from math import cos, pi, sin
from pathlib import Path

from svgpathtools import parse_path


def uid(seed: str) -> str:
    return hashlib.sha256(seed.encode()).hexdigest()[:20]


def color(value: str | None, gradients: dict[str, str] | None = None) -> str:
    if not value or value in {"none", "transparent"}:
        return "transparent"
    if value.startswith("url("):
        gradient_id = re.fullmatch(r"url\(#([^)]*)\)", value)
        return gradients.get(gradient_id.group(1), "#000000") if gradient_id and gradients else "#000000"
    if value.startswith("#"):
        return value
    match = re.fullmatch(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", value)
    if match:
        return "#%02x%02x%02x" % tuple(map(int, match.groups()))
    return value


def attrs(element: ET.Element) -> dict[str, str]:
    result = dict(element.attrib)
    for declaration in result.pop("style", "").split(";"):
        if ":" in declaration:
            key, value = declaration.split(":", 1)
            result.setdefault(key.strip(), value.strip())
    return result


def inherited_attrs(element: ET.Element, parent: dict[str, str]) -> dict[str, str]:
    result = parent.copy()
    result.update(attrs(element))
    return result


def points_for_path(path_data: str, samples: int) -> list[list[float]]:
    path = parse_path(path_data)
    points: list[list[float]] = []
    for segment in path:
        count = max(2, math.ceil(max(abs(segment.length()), 1) / samples))
        for index in range(count):
            point = segment.point(index / (count - 1))
            pair = [round(point.real, 3), round(point.imag, 3)]
            if not points or pair != points[-1]:
                points.append(pair)
    return points


def points_for_shape(node: ET.Element) -> list[list[float]]:
    data = attrs(node)
    tag = node.tag.rsplit("}", 1)[-1]
    if tag == "rect":
        x, y = float(data.get("x", 0)), float(data.get("y", 0))
        width, height = float(data["width"]), float(data["height"])
        return [[x, y], [x + width, y], [x + width, y + height], [x, y + height]]
    if tag == "circle":
        cx, cy, radius = float(data["cx"]), float(data["cy"]), float(data["r"])
        return [
            [cx + radius * cos(2 * pi * i / 32), cy + radius * sin(2 * pi * i / 32)]
            for i in range(32)
        ]
    if tag in {"polygon", "polyline"}:
        values = [float(value) for value in re.findall(r"[-+]?\d*\.?\d+(?:e[-+]?\d+)?", data["points"], re.I)]
        return [values[i : i + 2] for i in range(0, len(values) - 1, 2)]
    return []


def svg_size(root: ET.Element) -> tuple[float, float]:
    viewbox = root.get("viewBox", "").replace(",", " ").split()
    if len(viewbox) == 4:
        return float(viewbox[2]), float(viewbox[3])
    return float(root.get("width", 18)), float(root.get("height", 18))


def make_element(
    points: list[list[float]], fill: str, stroke: str, stroke_width: float, name: str, index: int
) -> dict:
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return {
        "id": uid(f"{name}:{index}"),
        "type": "line",
        "x": min(xs),
        "y": min(ys),
        "width": max(xs) - min(xs),
        "height": max(ys) - min(ys),
        "angle": 0,
        "strokeColor": stroke,
        "backgroundColor": fill,
        "fillStyle": "solid",
        "strokeWidth": stroke_width,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [uid(name)],
        "roundness": None,
        "seed": index + 1,
        "version": 1,
        "versionNonce": index + 1,
        "isDeleted": False,
        "boundElements": [],
        "updated": 0,
        "link": None,
        "locked": False,
        "points": [[x - min(xs), y - min(ys)] for x, y in points],
        "lastCommittedPoint": None,
        "startBinding": None,
        "endBinding": None,
        "startArrowhead": None,
        "endArrowhead": None,
        "polygon": fill != "transparent",
    }


def convert(svg: Path, samples: int) -> dict:
    root = ET.parse(svg).getroot()
    gradients = {}
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1] not in {"linearGradient", "radialGradient"}:
            continue
        stops = [attrs(child) for child in node if child.tag.rsplit("}", 1)[-1] == "stop"]
        if node.get("id") and stops:
            stop_color = stops[0].get("stop-color")
            if stop_color:
                gradients[node.get("id")] = color(stop_color)
    elements = []
    path_index = 0

    def visit(node: ET.Element, parent_attrs: dict[str, str]) -> None:
        nonlocal path_index
        data = inherited_attrs(node, parent_attrs)
        tag = node.tag.rsplit("}", 1)[-1]
        if tag in {"path", "rect", "circle", "polygon", "polyline"}:
            fill = color(
                data.get("fill") if "fill" in data or "stroke" in data else "#000000",
                gradients,
            )
            stroke = color(data.get("stroke"), gradients)
            if fill != "transparent" or stroke != "transparent":
                try:
                    points = points_for_path(data["d"], samples) if tag == "path" else points_for_shape(node)
                except (AssertionError, TypeError, ValueError, ZeroDivisionError):
                    points = []
                if len(points) >= 3:
                    try:
                        stroke_width = float(data.get("stroke-width", 0))
                    except ValueError:
                        stroke_width = 0
                    elements.append(
                        make_element(points, fill, stroke, stroke_width, svg.stem, path_index)
                    )
            path_index += 1
        for child in node:
            visit(child, data)

    visit(root, {})
    if not elements:
        raise ValueError(f"no filled paths found in {svg}")
    return {
        "id": uid(svg.as_posix()),
        "status": "published",
        "elements": elements,
        "created": 0,
        "name": svg.stem.replace("-", " "),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--samples", type=int, default=2)
    args = parser.parse_args()
    files = sorted(args.source.rglob("*.svg"))
    items = []
    skipped = []
    for svg in files:
        try:
            items.append(convert(svg, args.samples))
        except (ET.ParseError, ValueError, TypeError, AssertionError) as error:
            skipped.append(f"{svg}: {error}")
    if not items:
        raise SystemExit("No SVG icons could be converted")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(
            {"type": "excalidrawlib", "version": 2, "source": "https://excalidraw.com", "libraryItems": items},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"converted {len(items)} of {len(files)} SVGs")
    if skipped:
        print(f"skipped {len(skipped)} SVGs", file=sys.stderr)


if __name__ == "__main__":
    main()
