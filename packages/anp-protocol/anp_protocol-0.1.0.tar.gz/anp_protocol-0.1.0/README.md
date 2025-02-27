# ANP Protocol

Agent Network Protocol (ANP) implementation for agent communication and interoperability.

This package is a wrapper around the `agent-connect` package, providing the same functionality under a different package name.

## Features

- Identity authentication
- End-to-end encrypted communication
- Automatic protocol negotiation based on LLMs
- Efficient data exchange
- Agent description and discovery

## Installation

```bash
pip install anp-protocol
```

## Usage

```python
# You can use it exactly the same way as agent-connect
from anp_protocol import AgentConnect

# Initialize an agent
agent = AgentConnect(agent_id="your-agent-id")

# Use the agent for communication
# ...
```

## Documentation

For detailed documentation, please refer to the [Agent Network Protocol documentation](https://github.com/agent-network-protocol/AgentNetworkProtocol).

## License

MIT
