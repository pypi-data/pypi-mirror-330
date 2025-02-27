"""
Tests for the YAML loader.
"""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from astrolab.core.types import Agent, FunctionDefinition, Parameter
from astrolab.utils.yaml_loader import load_agent_from_yaml, save_agent_to_yaml


def test_load_agent_from_yaml():
    """Test loading an agent from a YAML file."""
    # Create a temporary YAML file
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
        yaml_content = """
        name: "Test Agent"
        description: "A test agent"
        model: "gpt-4o"
        instructions: "You are a test agent."
        functions:
          - name: test_function
            description: "A test function"
            parameters:
              - name: param1
                type: string
                description: "A test parameter"
                required: true
              - name: param2
                type: integer
                description: "Another test parameter"
                required: false
        """
        f.write(yaml_content.encode())
        yaml_file = f.name

    try:
        # Load the agent
        agent = load_agent_from_yaml(yaml_file)

        # Check the agent
        assert agent.name == "Test Agent"
        assert agent.description == "A test agent"
        assert agent.model == "gpt-4o"
        assert agent.instructions == "You are a test agent."
        assert len(agent.functions) == 1

        # Check the function
        function = agent.functions[0]
        assert function.name == "test_function"
        assert function.description == "A test function"
        assert len(function.parameters) == 2

        # Check the parameters
        param1 = function.parameters[0]
        assert param1.name == "param1"
        assert param1.type == "string"
        assert param1.description == "A test parameter"
        assert param1.required is True

        param2 = function.parameters[1]
        assert param2.name == "param2"
        assert param2.type == "integer"
        assert param2.description == "Another test parameter"
        assert param2.required is False

    finally:
        # Clean up
        os.unlink(yaml_file)


def test_save_agent_to_yaml():
    """Test saving an agent to a YAML file."""
    # Create an agent
    agent = Agent(
        name="Test Agent",
        description="A test agent",
        model="gpt-4o",
        instructions="You are a test agent.",
        functions=[
            FunctionDefinition(
                name="test_function",
                description="A test function",
                parameters=[
                    Parameter(
                        name="param1",
                        type="string",
                        description="A test parameter",
                        required=True,
                    ),
                    Parameter(
                        name="param2",
                        type="integer",
                        description="Another test parameter",
                        required=False,
                    ),
                ],
            ),
        ],
    )

    # Create a temporary YAML file
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
        yaml_file = f.name

    try:
        # Save the agent
        save_agent_to_yaml(agent, yaml_file)

        # Load the YAML file
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        # Check the data
        assert data["name"] == "Test Agent"
        assert data["description"] == "A test agent"
        assert data["model"] == "gpt-4o"
        assert data["instructions"] == "You are a test agent."
        assert len(data["functions"]) == 1

        # Check the function
        function = data["functions"][0]
        assert function["name"] == "test_function"
        assert function["description"] == "A test function"
        assert len(function["parameters"]) == 2

        # Check the parameters
        param1 = function["parameters"][0]
        assert param1["name"] == "param1"
        assert param1["type"] == "string"
        assert param1["description"] == "A test parameter"
        assert "required" not in param1  # required=True is the default

        param2 = function["parameters"][1]
        assert param2["name"] == "param2"
        assert param2["type"] == "integer"
        assert param2["description"] == "Another test parameter"
        assert param2["required"] is False

    finally:
        # Clean up
        os.unlink(yaml_file)


def test_roundtrip():
    """Test saving and loading an agent."""
    # Create an agent
    original_agent = Agent(
        name="Test Agent",
        description="A test agent",
        model="gpt-4o",
        instructions="You are a test agent.",
        functions=[
            FunctionDefinition(
                name="test_function",
                description="A test function",
                parameters=[
                    Parameter(
                        name="param1",
                        type="string",
                        description="A test parameter",
                        required=True,
                    ),
                    Parameter(
                        name="param2",
                        type="integer",
                        description="Another test parameter",
                        required=False,
                    ),
                ],
            ),
        ],
    )

    # Create a temporary YAML file
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
        yaml_file = f.name

    try:
        # Save the agent
        save_agent_to_yaml(original_agent, yaml_file)

        # Load the agent
        loaded_agent = load_agent_from_yaml(yaml_file)

        # Check that the loaded agent is the same as the original
        assert loaded_agent.name == original_agent.name
        assert loaded_agent.description == original_agent.description
        assert loaded_agent.model == original_agent.model
        assert loaded_agent.instructions == original_agent.instructions
        assert len(loaded_agent.functions) == len(original_agent.functions)

        # Check the function
        original_function = original_agent.functions[0]
        loaded_function = loaded_agent.functions[0]
        assert loaded_function.name == original_function.name
        assert loaded_function.description == original_function.description
        assert len(loaded_function.parameters) == len(original_function.parameters)

        # Check the parameters
        original_param1 = original_function.parameters[0]
        loaded_param1 = loaded_function.parameters[0]
        assert loaded_param1.name == original_param1.name
        assert loaded_param1.type == original_param1.type
        assert loaded_param1.description == original_param1.description
        assert loaded_param1.required == original_param1.required

        original_param2 = original_function.parameters[1]
        loaded_param2 = loaded_function.parameters[1]
        assert loaded_param2.name == original_param2.name
        assert loaded_param2.type == original_param2.type
        assert loaded_param2.description == original_param2.description
        assert loaded_param2.required == original_param2.required

    finally:
        # Clean up
        os.unlink(yaml_file)
