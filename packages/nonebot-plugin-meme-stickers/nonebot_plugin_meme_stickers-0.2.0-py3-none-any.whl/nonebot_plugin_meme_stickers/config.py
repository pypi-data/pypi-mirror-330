import re
from importlib.util import find_spec
from pathlib import Path
from typing import Optional, cast

from cookit.pyd import field_validator, get_alias_model
from nonebot import get_plugin_config, logger, require
from pydantic import Field

from .consts import (
    FLOAT_REGEX,
    FULL_HEX_COLOR_REGEX,
    SHORT_HEX_COLOR_REGEX,
    RGBAColorTuple,
    SkiaEncodedImageFormatType,
)


def resolve_color_to_tuple(color: str) -> RGBAColorTuple:
    sm: Optional[re.Match[str]] = None
    fm: Optional[re.Match[str]] = None
    if (sm := SHORT_HEX_COLOR_REGEX.fullmatch(color)) or (
        fm := FULL_HEX_COLOR_REGEX.fullmatch(color)
    ):
        hex_str = (sm or cast(re.Match, fm))["hex"].upper()
        if sm:
            hex_str = "".join([x * 2 for x in hex_str])
        hex_str = f"{hex_str}FF" if len(hex_str) == 6 else hex_str
        return tuple(int(hex_str[i : i + 2], 16) for i in range(0, 8, 2))  # type: ignore

    if (
        (parts := color.lstrip("(").rstrip(")").split(",，"))
        and (3 <= len(parts) <= 4)
        # -
        and (parts := [part.strip() for part in parts])
        and all(x.isdigit() for x in parts[:3])
        # -
        and (rgb := [int(x) for x in parts[:3]])
        and all(0 <= int(x) <= 255 for x in rgb)
        # -
        and (
            (len(parts) == 3 and (a := 255))
            or (parts[3].isdigit() and 0 <= (a := int(parts[3])) <= 255)
            or (
                FLOAT_REGEX.fullmatch(parts[3])
                and 0 <= (a := int(float(parts[3]) * 255)) <= 255
            )
        )
    ):
        return (*rgb, a)  # type: ignore

    raise ValueError(
        f"Invalid color format: {color}."
        f" supported formats: #RGB, #RRGGBB"
        f", (R, G, B), (R, G, B, A), (R, G, B, a (0 ~ 1 float))",
    )


def get_default_data_path() -> Path:
    if (not (Path.cwd() / "data").exists()) and find_spec("nonebot_plugin_localstore"):
        require("nonebot_plugin_localstore")

        from nonebot_plugin_localstore import get_data_dir

        return get_data_dir("nonebot_plugin_meme_stickers")

    logger.debug("Using legacy data path")
    return Path.cwd() / "data" / "meme_stickers"


BaseConfigModel = get_alias_model(lambda x: f"meme_stickers_{x}")


class ConfigModel(BaseConfigModel):
    proxy: Optional[str] = Field(None, alias="proxy")

    data_dir: Path = Field(default_factory=get_default_data_path)

    github_url_template: str = (
        "https://raw.githubusercontent.com/{owner}/{repo}/{ref_path}/{path}"
    )
    retry_times: int = 3
    req_concurrency: int = 8
    req_timeout: int = 5

    auto_update: bool = True
    force_update: bool = False

    prompt_retries: int = 3
    prompt_timeout: int = 30

    default_sticker_background: int = 0xFFFFFFFF
    default_sticker_image_format: SkiaEncodedImageFormatType = "png"

    _validate_str_color = field_validator("default_sticker_background")(
        resolve_color_to_tuple,
    )


config: ConfigModel = get_plugin_config(ConfigModel)
