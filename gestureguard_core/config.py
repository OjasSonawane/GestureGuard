from pathlib import Path
from pydantic import BaseModel, Field
import yaml

# -----------------------
# Paths
# -----------------------
APP_NAME = "gestureguard"
DEFAULT_CONFIG_DIR = Path.home() / f".{APP_NAME}"
DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_DIR / "config.yaml"


# -----------------------
# Config Models
# -----------------------
class GestureConfig(BaseModel):
    hold_frames: int = 6
    cooldown_frames: int = 12
    confidence_min: float = 0.5


class AppConfig(BaseModel):
    camera_index: int = 0
    frame_width: int = 960
    frame_height: int = 540
    max_fps: int = 30

    gestures: GestureConfig = Field(default_factory=GestureConfig)

    enabled: dict[str, bool] = Field(
        default_factory=lambda: {
            "open_palm": True,
            "point_left": True,
            "point_right": True,
            "thumbs_up": True,
            "thumbs_down": True,
            "fist": True,
        }
    )


# -----------------------
# Config IO
# -----------------------
def load_config(path: Path = DEFAULT_CONFIG_PATH) -> AppConfig:
    if path.exists():
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return AppConfig(**data)

    DEFAULT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    cfg = AppConfig()
    path.write_text(
        yaml.safe_dump(cfg.model_dump(), sort_keys=False),
        encoding="utf-8",
    )
    return cfg


def save_config(cfg: AppConfig, path: Path = DEFAULT_CONFIG_PATH) -> None:
    DEFAULT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(cfg.model_dump(), sort_keys=False),
        encoding="utf-8",
    )
