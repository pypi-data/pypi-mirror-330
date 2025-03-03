import time
from typing import Literal

import pythonping
from node_hermes_core.data.datatypes import SinglePointDataPacket
from node_hermes_core.nodes.source_node import SourceNode


class PingNode(SourceNode):
    class Config(SourceNode.Config):
        type: Literal["ping"]
        host: str

        @classmethod
        def default(cls) -> "PingNode.Config":
            return cls(type="ping", host="google.com")

    config: Config  # type: ignore

    def get_data(self) -> SinglePointDataPacket:
        timestamp = time.time()
        data = pythonping.ping(self.config.host, count=1, interval=0)  # type: ignore

        return SinglePointDataPacket(
            timestamp=timestamp,
            data={"rtt": data.rtt_avg},
            source=self.name,
        )
