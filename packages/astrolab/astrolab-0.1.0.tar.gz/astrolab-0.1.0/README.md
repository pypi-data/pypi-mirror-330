# Astrolab

A declarative framework for building AI agents with a focus on simplicity and extensibility.

## Features

- **Declarative Agent Definitions**: Define agents using YAML for easy configuration
- **Plugin System**: Extend functionality with custom plugins
- **OpenAI Integration**: Built-in support for OpenAI models
- **CLI Tool**: Command-line interface for managing agents
- **Easy Deployment**: Simple deployment options for your agents

## Installation

Using `uv` (recommended):

```bash
uv pip install astrolab
```

Using pip:

```bash
pip install astrolab
```

From source:

```bash
git clone https://github.com/yourusername/astrolab.git
cd astrolab
make setup
```

## Quick Start

### Create an Agent

Create a YAML file `my_agent.yaml`:

```yaml
name: "My First Agent"
description: "A simple agent that responds to user queries"
model: "gpt-4o"
instructions: |
  You are a helpful assistant that provides concise and accurate information.
  Always be polite and professional in your responses.
functions:
  - name: get_weather
    description: "Get the current weather for a location"
    parameters:
      - name: location
        type: string
        description: "The city and state, e.g. San Francisco, CA"
        required: true
```

### Run the Agent

```bash
astrolab run my_agent.yaml
```

### Create a Plugin

```bash
astrolab create-plugin my_plugin
```

This will create a plugin template in `astrolab/plugins/my_plugin/`.

## Agent Configuration

Agents are defined using YAML files with the following structure:

```yaml
name: "Agent Name"
description: "Agent description"
model: "gpt-4o"  # OpenAI model to use
instructions: "System instructions for the agent"
functions:
  - name: function_name
    description: "Function description"
    parameters:
      - name: param_name
        type: string  # string, number, boolean, array, object
        description: "Parameter description"
        required: true  # or false
```

## Plugin Development

Plugins allow you to extend Astrolab with custom functionality. A plugin consists of:

1. A plugin definition file
2. One or more function implementations

Example plugin structure:

```
astrolab/plugins/my_plugin/
├── __init__.py
└── plugin.py
```

Example plugin implementation:

```python
from astrolab.core.plugin import Plugin

class MyPlugin(Plugin):
    name = "my_plugin"
    version = "0.1.0"
    
    def get_functions(self):
        return [self.my_function]
    
    def my_function(self, param1: str) -> str:
        """
        My custom function
        
        Args:
            param1: A parameter
            
        Returns:
            A result string
        """
        return f"Processed: {param1}"
```

## CLI Commands

- `astrolab run <agent_file>`: Run an agent from a YAML file
- `astrolab create-agent`: Interactive agent creation wizard
- `astrolab list-plugins`: List available plugins
- `astrolab create-plugin <name>`: Create a new plugin template

## License

MIT
