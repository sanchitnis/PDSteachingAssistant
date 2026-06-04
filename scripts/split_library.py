#!/usr/bin/env python3
"""
split_library.py
----------------
Splits exercises/library.json into three focused files:

  exercises/prerequisites.json  — prerequisite (bridge) exercises
  exercises/practice.json       — ACP syllabus extra-practice exercises (CO1-CO5)
  exercises/advanced.json       — beyond-syllabus enrichment exercises

Category values inside each file are updated to match the file_type:
  old "prerequisite" → "prerequisite"   (unchanged)
  old "syllabus"     → "practice"       (renamed for clarity)
  old "advanced"     → "advanced"       (unchanged)
"""

import json
import copy
from pathlib import Path

LIBRARY_PATH = Path("exercises/library.json")

SPLIT_CONFIG = {
    "prerequisite": {
        "file":      Path("exercises/prerequisites.json"),
        "file_type": "prerequisites",
        "category":  "prerequisite",
        "description": (
            "Foundation/bridging exercises assumed from the prior C course. "
            "Available on demand when students need to review fundamentals "
            "before tackling ACP syllabus topics."
        ),
    },
    "syllabus": {
        "file":      Path("exercises/practice.json"),
        "file_type": "practice",
        "category":  "practice",
        "description": (
            "Extra practice exercises aligned to the ACP syllabus COs (CO1-CO5). "
            "Same schema as lab_programs.json. Use these for additional "
            "reinforcement after completing the mandatory lab programs."
        ),
    },
    "advanced": {
        "file":      Path("exercises/advanced.json"),
        "file_type": "advanced",
        "category":  "advanced",
        "description": (
            "Beyond-syllabus enrichment exercises for fast finishers. "
            "Topics not assessed in the ACP exam (recursion, unions, enums, "
            "random file access). Unlocked after CO1-CO5 are at Level 3."
        ),
    },
}


def main():
    lib = json.loads(LIBRARY_PATH.read_text(encoding="utf-8"))

    for old_cat, cfg in SPLIT_CONFIG.items():
        new_cat = cfg["category"]

        out = {
            "schema_version":  lib["schema_version"],
            "file_type":       cfg["file_type"],
            "last_updated":    lib["last_updated"],
            "description":     cfg["description"],
            "institution":     lib["institution"],
            "department":      lib["department"],
            "course":          lib["course"],
            "co_descriptions": lib["co_descriptions"],
            "topics": {},
        }

        for code, topic in lib["topics"].items():
            if topic.get("category") != old_cat:
                continue

            t = copy.deepcopy(topic)
            t["category"] = new_cat

            for ex in t.get("exercises", []):
                if ex.get("category") == old_cat:
                    ex["category"] = new_cat

            out["topics"][code] = t

        cfg["file"].write_text(
            json.dumps(out, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        topic_count = len(out["topics"])
        ex_count    = sum(len(t.get("exercises", [])) for t in out["topics"].values())
        print("Written:", cfg["file"],
              " (%d topics, %d exercises)" % (topic_count, ex_count))

    print("Done. library.json is unchanged (still the master source).")


if __name__ == "__main__":
    main()
