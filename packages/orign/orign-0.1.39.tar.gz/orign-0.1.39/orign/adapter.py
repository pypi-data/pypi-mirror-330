from typing import Optional

import requests

from orign.config import GlobalConfig


class Adapter:
    @classmethod
    def get(cls, name: Optional[str] = None, config: Optional[GlobalConfig] = None):
        config = config or GlobalConfig.read()

        name_parts = name.split("/") if name else []
        if len(name_parts) == 2:
            namespace, short_name = name_parts
        else:
            namespace = None
            short_name = name_parts[0]

        # Construct the WebSocket URL with query parameters
        adapters_url = f"{config.server}/v1/adapters"

        response = requests.get(
            adapters_url, headers={"Authorization": f"Bearer {config.api_key}"}
        )
        response.raise_for_status()
        response_jdict = response.json()
        adapters = response_jdict.get("adapters", [])

        if namespace:
            adapters = [a for a in adapters if a == name]
        else:
            adapters = [a for a in adapters if a.split("/")[1] == short_name]
        return adapters
