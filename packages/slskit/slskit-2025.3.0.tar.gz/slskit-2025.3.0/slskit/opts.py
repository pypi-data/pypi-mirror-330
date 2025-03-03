import os
from dataclasses import dataclass
from functools import cached_property
from typing import Any, Optional, cast
from string import Template

import jsonschema
import salt.config
import salt.utils
import yaml
from funcy import get_in, post_processing

from . import PACKAGE_NAME
from .types import AnyDict

DEFAULT_CONFIG_PATHS = (f"{PACKAGE_NAME}.yaml", f"{PACKAGE_NAME}.yml")

SCHEMA: AnyDict = {
    "type": "object",
    "properties": {
        "salt": {"type": "object"},
        PACKAGE_NAME: {
            "type": "object",
            "properties": {
                "skip_fileserver_update": {"type": "boolean"},
                "roster": {
                    "type": "object",
                    "additionalProperties": {
                        "oneOf": [
                            {"type": "null"},
                            {
                                "type": "object",
                                "properties": {"grains": {"type": "object"}},
                            },
                        ]
                    },
                },
                "default_grains": {"type": "object"},
            },
        },
    },
}


def validate(instance: AnyDict, schema: Optional[AnyDict] = None) -> AnyDict:
    jsonschema.validate(instance, schema or SCHEMA)
    return instance


@dataclass
class Config:
    config_path: str
    dynamic_overrides: AnyDict

    @cached_property
    def opts(self) -> AnyDict:
        overrides = {
            "root_dir": f".{PACKAGE_NAME}",
            "state_events": False,
            "file_client": "local",
        }

        if self._get_setting("slskit.skip_fileserver_update", True):
            # skip fileserver update for faster rendering
            # see salt.fileserver.FSChan implementation
            overrides["__fs_update"] = True

        overrides.update(self.settings.get("salt", {}))
        overrides.update(self.dynamic_overrides)
        opts = salt.config.apply_minion_config(overrides)
        return cast(AnyDict, opts)

    @cached_property
    def roster(self) -> AnyDict:
        result = self._get_setting(f"{PACKAGE_NAME}.roster", {})
        return cast(AnyDict, result)

    @cached_property
    @post_processing(validate)
    def settings(self) -> AnyDict:
        if self.config_path is not None:
            return load_yaml(self.config_path)
        for path in DEFAULT_CONFIG_PATHS:
            if os.path.exists(path):
                return load_yaml(path)
        return {}

    def grains_for(self, minion_id: str) -> AnyDict:
        grains = {"id": minion_id}
        salt.utils.dictupdate.update(
            grains, self._get_setting(f"{PACKAGE_NAME}.default_grains", {})
        )
        salt.utils.dictupdate.update(
            grains, self._get_setting(f"{PACKAGE_NAME}.roster.{minion_id}.grains", {})
        )
        return grains

    def _get_setting(self, path: str, default: Any, separator: str = ".") -> Any:
        try:
            return get_in(self.settings, path.split(separator), default)
        except TypeError:
            return default


def load_yaml(path: str) -> AnyDict:
    with open(path) as f:
        content = f.read()
        content = Template(content).substitute(os.environ)
        result = yaml.safe_load(content)
        return cast(AnyDict, result)
