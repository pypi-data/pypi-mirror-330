"""
Tests for the plugin system.
"""

import pytest

from astrolab.core.plugin import Plugin, PluginManager
from astrolab.core.types import AgentFunction, Result


class TestPlugin(Plugin):
    """Test plugin for testing."""

    name = "test_plugin"
    version = "0.1.0"
    description = "A test plugin"

    def get_functions(self):
        """Get the functions provided by this plugin."""
        return [self.example_function, self.another_function]

    def example_function(self, param1: str) -> str:
        """
        Example function.

        Args:
            param1: A test parameter

        Returns:
            A test result
        """
        return f"Example function called with param1={param1}"

    def another_function(self, param1: str, param2: int = 42) -> Result:
        """
        Another test function.

        Args:
            param1: A test parameter
            param2: Another test parameter

        Returns:
            A test result
        """
        return Result(
            value=f"Another function called with param1={param1}, param2={param2}",
            context_variables={"param1": param1, "param2": param2},
        )


def test_plugin_manager():
    """Test the plugin manager."""
    # Create a plugin manager
    manager = PluginManager()

    # Check that there are no plugins
    assert len(manager.get_all_plugins()) == 0
    assert len(manager.get_all_functions()) == 0

    # Create a plugin
    plugin = TestPlugin()

    # Register the plugin
    manager.register_plugin(plugin)

    # Check that the plugin is registered
    assert len(manager.get_all_plugins()) == 1
    assert manager.get_plugin("test_plugin") is plugin

    # Check that the functions are registered
    functions = manager.get_all_functions()
    assert len(functions) == 2
    assert "example_function" in functions
    assert "another_function" in functions

    # Call the functions
    result1 = functions["example_function"]("test")
    assert result1 == "Example function called with param1=test"

    result2 = functions["another_function"]("test", param2=123)
    assert isinstance(result2, Result)
    assert result2.value == "Another function called with param1=test, param2=123"
    assert result2.context_variables == {"param1": "test", "param2": 123}

    # Unregister the plugin
    manager.unregister_plugin("test_plugin")

    # Check that the plugin is unregistered
    assert len(manager.get_all_plugins()) == 0
    assert manager.get_plugin("test_plugin") is None

    # Check that the functions are unregistered
    assert len(manager.get_all_functions()) == 0
    assert manager.get_function("example_function") is None
    assert manager.get_function("another_function") is None


def test_plugin_manager_errors():
    """Test error handling in the plugin manager."""
    # Create a plugin manager
    manager = PluginManager()

    # Create a plugin
    plugin = TestPlugin()

    # Register the plugin
    manager.register_plugin(plugin)

    # Try to register the same plugin again
    with pytest.raises(ValueError):
        manager.register_plugin(plugin)

    # Try to unregister a non-existent plugin
    with pytest.raises(ValueError):
        manager.unregister_plugin("non_existent_plugin")

    # Create another plugin with the same function name
    class ConflictingPlugin(Plugin):
        name = "conflicting_plugin"
        version = "0.1.0"

        def get_functions(self):
            return [self.example_function]

        def example_function(self, param1: str) -> str:
            return f"Conflicting function called with param1={param1}"

    # Try to register the conflicting plugin
    with pytest.raises(ValueError):
        manager.register_plugin(ConflictingPlugin())
