import re
from typing import Optional

from backend.modules.drawio.models import TaskStatus, ElementData
from backend.utils.debug_utils import get_func_call
import xml.etree.ElementTree as ET


def _extract_number(element, key: str) -> float | None:
    try:
        value = element.get(key) if element else None
        return float(value) if value is not None else None
    except Exception as ex:
        print(f"FAILED {get_func_call()}: {ex}")
        return None


def _extract_task_status(element, mx_cell: Optional[ElementData]) -> TaskStatus | None:
    try:
        if element and "mx_cell" in element:
            style = element.get("mx_cell")["style"]
        else:
            style = element.get("style")
        if not style:
            style = mx_cell.style
        for task_status in TaskStatus:
            if "fillColor" in style:
                return task_status
        return None
    except Exception as ex:
        print(f"FAILED {get_func_call()}: {ex}")
        return None


def _extract_label(raw_label: Optional[str]) -> str | None:
    try:
        if raw_label:
            if raw_label.startswith("<"):
                return re.sub(r"<[^>]+>", "", raw_label)
            return raw_label.split("<")[0]
        return None
    except Exception as ex:
        print(f"FAILED {get_func_call()}: {ex}")
        return None


def _is_group_marker(element) -> bool:
    return "<h1>" in (element.get("value") or "")


def _extract_mx_cell(element, page_name: str) -> ElementData | None:
    geometry = element.find("geometry")
    value = element.get("value")
    return ElementData(
        id=element.get("id"),
        epic_name=page_name,
        value=value,
        text=_extract_label(raw_label=value),
        is_group_marker=_is_group_marker(element=element),
        task_status=_extract_task_status(element=element, mx_cell=None),
        style=element.get("style"),
        parent=element.get("parent"),
        x=_extract_number(element=element, key="x"),
        y=_extract_number(element=element, key="y"),
        width=_extract_number(element=element, key="width"),
        height=_extract_number(element=element, key="height"),
        link=None,
        mx_cell=None,
        group_id=None,
        group_name=None,
    )


def extract_elements_from_page(file_path: str) -> list[ElementData]:
    tree = ET.parse(file_path)
    root = tree.getroot()
    res = []
    for diagram in root.findall("diagram"):
        page_name = diagram.get("name")
        try:
            for element in diagram.find("mxGraphModel").find("root"):
                if not element.get("value") and element.get("label"):
                    continue
                tag = element.tag
                if tag == "mxCell":
                    res.append(_extract_mx_cell(element=element, page_name=page_name))
                elif tag == "UserObject":
                    mx_cell = _extract_mx_cell(element=element.find("mxCell"), page_name=page_name)
                    label = element.get("label")
                    res.append(
                        ElementData(
                            id=element.get("id"),
                            epic_name=page_name,
                            value=label,
                            text=_extract_label(raw_label=label),
                            is_group_marker=_is_group_marker(element=element),
                            task_status=_extract_task_status(element=element, mx_cell=mx_cell),
                            style=mx_cell.style,
                            link=element.get("link"),
                            x=mx_cell.x,
                            y=mx_cell.y,
                            width=mx_cell.width,
                            height=mx_cell.height,
                            parent=mx_cell.parent,
                            mx_cell=mx_cell,
                            group_id=None,
                            group_name=None,
                        )
                    )
        except Exception as ex:
            print(f"FAILED {get_func_call()}: {ex}")
    return res


def find_group_rectangle(elements: list) -> list:
    res = []
    for element in elements:
        if "h2 style" in (element.get("value") or ""):
            res.append(element)
    return res


def find_inner_elements(elements: list, parent_element) -> list:
    res = []
    for child_element in elements:
        try:
            if (child_element["id"] == parent_element["id"]
                    or child_element.get("x") is None
                    or child_element.get("y") is None
                    or child_element.get("width") is None
                    or child_element.get("height") is None
            ):
                continue
            parent__left = parent_element["x"]
            parent__right = parent_element["x"] + parent_element["width"]
            parent__top = parent_element["y"]
            parent__bottom = parent_element["y"] + parent_element["height"]
            child__left = child_element["x"]
            child__right = child_element["x"] + child_element["width"]
            child__top = child_element["y"]
            child__bottom = child_element["y"] + child_element["height"]
            if (parent__left <= child__left
                    and parent__right >= child__right
                    and parent__top <= child__top
                    and parent__bottom >= child__bottom
            ):
                res.append(child_element)
        except Exception as ex:
            print(f"FAILED {get_func_call()}: {ex}")
    return res


def _get_group_zones(group_makers: list[ElementData]) -> list[dict]:
    return [
        {
            "id": market.id,
            "name": market.text,
            "top": market.y,
            "bottom": group_makers[i + 1].y if i < len(group_makers) - 1 else 999999,
        }
        for i, market in enumerate(group_makers)
    ]


def enrich_with_groups(elements: list[ElementData]) -> None:
    group_makers = [e for e in elements if e.is_group_marker]
    group_zones = _get_group_zones(group_makers=group_makers)
    for e in elements:
        for group_zone in group_zones:
            if (e.y
                    and group_zone["top"] <= e.y < group_zone["bottom"]
                    and not e.is_group_marker):
                e.group_id = group_zone["id"]
                e.group_name = group_zone["name"]


if __name__ == '__main__':
    elements = extract_elements_from_page(file_path="test_data/Work_streams.drawio")
    print("")