from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, cast

from maxflexsim.fabric.island import Island
from maxflexsim.fabric.noc import NoC
from maxflexsim.fabric.tile import Tile


@dataclass(frozen=True)
class RoutingTier:
    delay_per_hop: float


@dataclass(frozen=True)
class RoutingParams:
    local: RoutingTier
    regional: RoutingTier


@dataclass(frozen=True)
class Fabric:
    name: str
    width: int
    height: int
    tile_capacity: int
    island_rows: int
    island_cols: int
    routing: RoutingParams
    noc: NoC
    fingerprint: str

    @classmethod
    def from_json(cls, path: str | Path) -> "Fabric":
        raw = Path(path).read_text(encoding="utf-8")
        data = json.loads(raw)
        schema_path = Path(__file__).resolve().parents[3] / "fabric" / "fabric_schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        _validate_schema(data, schema)
        fingerprint = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return cls(
            name=data["name"],
            width=data["grid"]["width"],
            height=data["grid"]["height"],
            tile_capacity=data["tile"]["capacity"],
            island_rows=data["islands"]["rows"],
            island_cols=data["islands"]["cols"],
            routing=RoutingParams(
                local=RoutingTier(delay_per_hop=data["routing"]["local"]["delay_per_hop"]),
                regional=RoutingTier(delay_per_hop=data["routing"]["regional"]["delay_per_hop"]),
            ),
            noc=NoC(
                router_latency=data["noc"]["router_latency"],
                link_bandwidth=data["noc"]["link_bandwidth"],
            ),
            fingerprint=fingerprint,
        )

    @property
    def island_width(self) -> int:
        return self.width // self.island_cols

    @property
    def island_height(self) -> int:
        return self.height // self.island_rows

    def islands(self) -> list[Island]:
        islands: list[Island] = []
        for row in range(self.island_rows):
            for col in range(self.island_cols):
                islands.append(
                    Island(
                        row=row,
                        col=col,
                        x_start=col * self.island_width,
                        y_start=row * self.island_height,
                        width=self.island_width,
                        height=self.island_height,
                    )
                )
        return islands

    def tiles(self) -> Iterable[Tile]:
        for y in range(self.height):
            for x in range(self.width):
                yield Tile(x=x, y=y, capacity=self.tile_capacity)

    def island_for_tile(self, x: int, y: int) -> Island:
        col = min(x // self.island_width, self.island_cols - 1)
        row = min(y // self.island_height, self.island_rows - 1)
        return Island(
            row=row,
            col=col,
            x_start=col * self.island_width,
            y_start=row * self.island_height,
            width=self.island_width,
            height=self.island_height,
        )


def _validate_schema(data: Mapping[str, Any], schema: Mapping[str, Any]) -> None:
    required = schema.get("required", [])
    if isinstance(required, list):
        for key in required:
            if key not in data:
                raise ValueError(f"Missing required key: {key}")
    properties = schema.get("properties", {})
    if isinstance(properties, dict):
        for key, prop in properties.items():
            if key in data and isinstance(prop, Mapping):
                nested_required = prop.get("required", [])
                if isinstance(nested_required, list) and isinstance(data[key], dict):
                    nested_data = cast(dict[str, Any], data[key])
                    for nested_key in nested_required:
                        if nested_key not in nested_data:
                            raise ValueError(f"Missing required key: {key}.{nested_key}")
