import time, uuid
from typing import Dict, Tuple, Optional

class RoundStore:
    def __init__(self, ttl_seconds: int = 20 * 60):
        self.ttl = ttl_seconds
        self._items: Dict[str, Tuple[float, float, float, dict]] = {}

    def new_round(self, lat: float, lon: float, meta: dict) -> str:
        rid = uuid.uuid4().hex
        self._items[rid] = (lat, lon, time.time() + self.ttl, meta)
        return rid

    def get_answer(self, rid: str) -> Optional[Tuple[float, float, dict]]:
        item = self._items.get(rid)
        if not item: return None
        lat, lon, exp, meta = item
        if time.time() > exp:
            self._items.pop(rid, None)
            return None
        return (lat, lon, meta)

    def pop(self, rid: str):
        self._items.pop(rid, None)
