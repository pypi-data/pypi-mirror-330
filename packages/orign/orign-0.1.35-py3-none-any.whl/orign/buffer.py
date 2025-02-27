from typing import Dict, List, Optional

import requests

from orign.config import GlobalConfig
from orign.models import (
    V1LlamaFactoryParams,
    V1MSSwiftBufferParams,
    V1ReplayBuffer,
    V1ReplayBufferData,
    V1ReplayBufferRequest,
    V1ReplayBuffersResponse,
)


class ReplayBuffer:
    def __init__(
        self,
        name: str,
        vram_request: Optional[str] = None,
        provider: str = "ms-swift",
        cpu_request: Optional[str] = None,
        trust_remote_code: Optional[bool] = None,
        adapter: Optional[str] = None,
        train_every: int = 50,
        sample_n: int = 100,
        sample_strategy: str = "Random",
        queue: Optional[str] = None,
        ms_swift_params: Optional[V1MSSwiftBufferParams] = None,
        llama_factory_params: Optional[V1LlamaFactoryParams] = None,
        labels: Optional[Dict[str, str]] = None,
        config: Optional[GlobalConfig] = None,
    ):
        name_parts = name.split("/")
        if len(name_parts) == 2:
            namespace, name = name_parts
        else:
            namespace = None
            name = name_parts[0]

        config = config or GlobalConfig.read()
        self.api_key = config.api_key
        self.orign_host = config.server

        # Construct the WebSocket URL with query parameters
        self.buffers_url = f"{self.orign_host}/v1/buffers"

        response = requests.get(
            self.buffers_url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        buffers = V1ReplayBuffersResponse.model_validate(response.json())
        self.buffer = next((b for b in buffers.buffers if b.name == name), None)

        if not self.buffer:
            if not vram_request:
                raise ValueError("vram_request is required")

            request = V1ReplayBufferRequest(
                name=name,
                namespace=namespace,
                provider=provider,
                vram_request=vram_request,
                cpu_request=cpu_request,
                trust_remote_code=trust_remote_code,
                adapter=adapter,
                ms_swift_params=ms_swift_params,
                llama_factory_params=llama_factory_params,
                labels=labels,
                train_every=train_every,
                sample_n=sample_n,
                sample_strategy=sample_strategy,
                queue=queue,
            )
            response = requests.post(
                self.buffers_url,
                json=request.model_dump(),
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            response.raise_for_status()
            self.buffer = V1ReplayBuffer.model_validate(response.json())
            print(f"Created buffer {self.buffer.name}")
        else:
            print(f"Found buffer {self.buffer.name}")

    def send(self, data: List[dict]):
        if not self.buffer or not self.buffer.name:
            raise ValueError("Buffer not found")

        url = f"{self.buffers_url}/{self.buffer.namespace}/{self.buffer.name}/examples"

        request = V1ReplayBufferData(examples=data)

        response = requests.post(
            url,
            json=request.model_dump(),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        return response.json()

    @classmethod
    def get(
        cls,
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
    ) -> List[V1ReplayBuffer]:
        config = config or GlobalConfig.read()

        # Construct the WebSocket URL with query parameters
        buffers_url = f"{config.server}/v1/buffers"

        response = requests.get(
            buffers_url, headers={"Authorization": f"Bearer {config.api_key}"}
        )
        response.raise_for_status()
        buffer_response = V1ReplayBuffersResponse.model_validate(response.json())
        buffers = buffer_response.buffers
        if name:
            buffers = [b for b in buffers if b.name == name]

        if namespace:
            buffers = [b for b in buffers if b.namespace == namespace]

        return buffers
