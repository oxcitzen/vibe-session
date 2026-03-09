"""Very small local persistence for recipe ratings (prototype)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


class RatingsStore:
    """
    Stores ratings in a local JSON file.

    Format:
    {
      "ratings": {
        "<recipeId>": { "count": 2, "sum": 9, "avg": 4.5 }
      }
    }
    """

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def _read(self) -> Dict[str, Any]:
        if not self.file_path.exists():
            return {"ratings": {}}
        try:
            return json.loads(self.file_path.read_text(encoding="utf-8"))
        except Exception:
            return {"ratings": {}}

    def _write(self, data: Dict[str, Any]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def add_rating(self, recipe_id: str, rating: int) -> Dict[str, Any]:
        data = self._read()
        ratings: Dict[str, Any] = data.setdefault("ratings", {})
        entry = ratings.get(recipe_id) or {"count": 0, "sum": 0, "avg": 0.0}
        entry["count"] = int(entry.get("count", 0)) + 1
        entry["sum"] = int(entry.get("sum", 0)) + int(rating)
        entry["avg"] = round(entry["sum"] / max(entry["count"], 1), 2)
        ratings[recipe_id] = entry
        self._write(data)
        return entry

    def get_rating_summary(self, recipe_id: str) -> Optional[Dict[str, Any]]:
        data = self._read()
        ratings: Dict[str, Any] = data.get("ratings", {})
        return ratings.get(recipe_id)

