"""
AHB csv comparison logic.
"""

from typing import List, Tuple

from ahlbatross.enums.diff_types import DiffType
from ahlbatross.models.ahb import AhbRow, AhbRowComparison, AhbRowDiff
from ahlbatross.utils.string_formatting import normalize_entries
from ahlbatross.utils.xlsx_formatting import AHB_PROPERTIES


def _compare_ahb_rows(previous_ahb_row: AhbRow, subsequent_ahb_row: AhbRow) -> AhbRowDiff:
    """
    Compare two AhbRow objects to identify changes.
    """
    changed_entries = []

    # consider all AHB properties except `section_name` (Segmentname) and `formatversion`
    for entry in AHB_PROPERTIES:
        previous_ahb_entry = normalize_entries(getattr(previous_ahb_row, entry, "") or "")
        subsequent_ahb_entry = normalize_entries(getattr(subsequent_ahb_row, entry, "") or "")

        if (previous_ahb_entry or subsequent_ahb_entry) and previous_ahb_entry != subsequent_ahb_entry:
            changed_entries.extend(
                [f"{entry}_{previous_ahb_row.formatversion}", f"{entry}_{subsequent_ahb_row.formatversion}"]
            )

    return AhbRowDiff(
        diff_type=DiffType.MODIFIED if changed_entries else DiffType.UNCHANGED, changed_entries=changed_entries
    )


def _add_empty_row(formatversion: str) -> AhbRow:
    """
    Create an empty row.
    """
    return AhbRow(
        formatversion=formatversion,
        section_name="",
        segment_group_key=None,
        segment_code=None,
        data_element=None,
        segment_id=None,
        value_pool_entry=None,
        name=None,
        ahb_expression=None,
        conditions=None,
    )


def _find_matching_subsequent_row(
    current_ahb_row: AhbRow, subsequent_ahb_rows: List[AhbRow], start_idx: int, duplicate_indices: set[int]
) -> Tuple[int, AhbRow | None]:
    """
    Find matching row in subsequent version starting from given index by consider all AHB properties
    within the same `section_name` group.
    """
    normalized_current = normalize_entries(current_ahb_row.section_name)
    current_key = current_ahb_row.get_key()

    for idx, row in enumerate(subsequent_ahb_rows[start_idx:], start_idx):
        if idx in duplicate_indices:
            continue

        if (
            normalize_entries(row.section_name) == normalized_current
            and row.get_key() == current_key
            and row.segment_id == current_ahb_row.segment_id
        ):
            return idx, row

    # in case no match was found, continue by aligning `Segmentname` entries
    for idx, row in enumerate(subsequent_ahb_rows[start_idx:], start_idx):
        if idx in duplicate_indices:
            continue

        if normalize_entries(row.section_name) == normalized_current:
            if row.ahb_expression is not None and current_ahb_row.ahb_expression is None:
                continue
            return idx, row

    return -1, None


def align_ahb_rows(previous_ahb_rows: List[AhbRow], subsequent_ahb_rows: List[AhbRow]) -> List[AhbRowComparison]:
    """
    Align AHB rows while comparing two formatversions.
    """
    result = []
    i = 0
    j = 0
    duplicate_indices: set[int] = set()

    while i < len(previous_ahb_rows) or j < len(subsequent_ahb_rows):
        if i >= len(previous_ahb_rows):
            # add remaining rows as "new" if not already used
            if j not in duplicate_indices:
                result.append(
                    AhbRowComparison(
                        previous_formatversion=_add_empty_row(subsequent_ahb_rows[j].formatversion),
                        diff=AhbRowDiff(diff_type=DiffType.ADDED),
                        subsequent_formatversion=subsequent_ahb_rows[j],
                    )
                )
            j += 1
            continue

        if j >= len(subsequent_ahb_rows):
            result.append(
                AhbRowComparison(
                    previous_formatversion=previous_ahb_rows[i],
                    # label remaining rows of previous AHB as REMOVED
                    diff=AhbRowDiff(diff_type=DiffType.REMOVED),
                    subsequent_formatversion=_add_empty_row(previous_ahb_rows[i].formatversion),
                )
            )
            i += 1
            continue

        current_row = previous_ahb_rows[i]
        next_match_idx, matching_row = _find_matching_subsequent_row(
            current_row, subsequent_ahb_rows, j, duplicate_indices
        )

        if next_match_idx >= 0 and matching_row is not None:
            # add new rows until `section_name` (Segmentname) matches
            while j < next_match_idx:
                if j not in duplicate_indices:
                    result.append(
                        AhbRowComparison(
                            previous_formatversion=_add_empty_row(subsequent_ahb_rows[j].formatversion),
                            diff=AhbRowDiff(diff_type=DiffType.ADDED),
                            subsequent_formatversion=subsequent_ahb_rows[j],
                        )
                    )
                j += 1

            # add matching rows with comparison
            diff = _compare_ahb_rows(current_row, matching_row)
            result.append(
                AhbRowComparison(
                    previous_formatversion=current_row,
                    diff=diff,
                    subsequent_formatversion=matching_row,
                )
            )
            duplicate_indices.add(next_match_idx)
            i += 1
            j = next_match_idx + 1

        else:
            # if no match found - label as REMOVED
            result.append(
                AhbRowComparison(
                    previous_formatversion=current_row,
                    diff=AhbRowDiff(diff_type=DiffType.REMOVED),
                    subsequent_formatversion=_add_empty_row(current_row.formatversion),
                )
            )
            i += 1

    return result
