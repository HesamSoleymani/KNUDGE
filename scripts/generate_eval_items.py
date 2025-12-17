#!/usr/bin/env python3
"""
Generate an `eval_items.csv` file listing dialog comparisons for `gpt_tree_eval.py`.

It scans the `root_output_path` for dialog folders and their `json_outputs/` files, then
creates rows with columns: dialog_id, method_1, method_2, method_3, method_4.

Usage:
  python scripts/generate_eval_items.py --root_output_path tmp/e2e_dialogs/gpt-4-1106-preview --output_file eval_items.csv

Make sure you have already generated dialogs with `npc_dialog/graph_dialogwriter.py` or other writers
so that `tmp/e2e_dialogs/<dialog_id>/json_outputs/*.json` exist.
"""
import argparse
import csv
import itertools
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root_output_path", type=str, default="tmp/e2e_dialogs")
    parser.add_argument("--output_file", type=str, default="eval_items.csv")
    parser.add_argument(
        "--max_rows_per_dialog",
        type=int,
        default=50,
        help="limit number of rows generated per dialog (0=no limit)",
    )
    args = parser.parse_args()

    root = args.root_output_path
    if not os.path.isdir(root):
        raise SystemExit(f"root_output_path not found: {root}")

    rows = []
    # iterate dialogs
    for dialog_id in sorted(os.listdir(root)):
        print("*", dialog_id)
        json_dir = os.path.join(root, dialog_id, "json_outputs")
        if not os.path.isdir(json_dir):
            print("  json_outputs/ not found, skipping")
            continue
        methods = sorted(
            [
                os.path.splitext(f)[0]
                for f in os.listdir(json_dir)
                if f.endswith(".json")
            ]
        )
        print(f"  found methods: {methods}")
        if len(methods) < 2:
            print("  less than 2 methods, skipping")
            continue

        # use unordered unique pairs for diversity
        pair_list = list(itertools.combinations(methods, 2))
        if not pair_list:
            continue

        # for each pair, pair with the next pair (wrap-around), or with itself if only one pair
        for i, pair1 in enumerate(pair_list):
            if args.max_rows_per_dialog and i >= args.max_rows_per_dialog:
                break
            pair2 = pair_list[(i + 1) % len(pair_list)] if len(pair_list) > 1 else pair1
            rows.append([dialog_id, pair1[0], pair1[1], pair2[0], pair2[1]])

    # write CSV
    with open(args.output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["dialog_id", "method_1", "method_2", "method_3", "method_4"])
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.output_file}")


if __name__ == "__main__":
    main()
