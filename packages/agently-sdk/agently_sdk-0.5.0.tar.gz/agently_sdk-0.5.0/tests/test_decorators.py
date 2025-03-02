"""
Tests for the decorators module.
"""

import pytest

from agently_sdk.plugins.decorators import agently_function, kernel_function


def test_agently_function_direct_usage():
    """Test that agently_function works when used directly."""

    @agently_function
    def test_func(x: int) -> int:
        """Test function."""
        return x * 2

    # Test function execution
    assert test_func(5) == 10

    # Test metadata
    assert hasattr(test_func, "_is_agently_function")
    assert test_func._is_agently_function is True
    assert hasattr(test_func, "_is_kernel_function")
    assert test_func._is_kernel_function is True

    # Check for Semantic Kernel compatibility
    assert hasattr(test_func, "__kernel_function__")
    assert test_func.__kernel_function__ is True


def test_agently_function_with_args():
    """Test that agently_function works when used with arguments."""

    @agently_function(
        description="Test function with description",
        name="custom_name",
        input_description="Input description",
    )
    def test_func(x: int) -> int:
        """Test function."""
        return x * 3

    # Test function execution
    assert test_func(5) == 15

    # Test metadata
    assert hasattr(test_func, "_is_agently_function")
    assert test_func._is_agently_function is True
    assert hasattr(test_func, "_is_kernel_function")
    assert test_func._is_kernel_function is True
    assert hasattr(test_func, "_description")
    assert test_func._description == "Test function with description"
    assert hasattr(test_func, "_name")
    assert test_func._name == "custom_name"
    assert hasattr(test_func, "_input_description")
    assert test_func._input_description == "Input description"

    # Check for Semantic Kernel compatibility
    assert hasattr(test_func, "__kernel_function__")
    assert test_func.__kernel_function__ is True


def test_kernel_function_alias():
    """Test that kernel_function is an alias for agently_function."""

    @kernel_function
    def test_func(x: int) -> int:
        """Test function."""
        return x * 4

    # Test function execution
    assert test_func(5) == 20

    # Test metadata
    assert hasattr(test_func, "_is_agently_function")
    assert test_func._is_agently_function is True
    assert hasattr(test_func, "_is_kernel_function")
    assert test_func._is_kernel_function is True

    # Check for Semantic Kernel compatibility
    assert hasattr(test_func, "__kernel_function__")
    assert test_func.__kernel_function__ is True


def test_semantic_kernel_integration():
    """Test integration with semantic_kernel if available."""
    try:
        from semantic_kernel.functions import kernel_function as sk_kernel_function

        # Create a reference function with SK's decorator directly
        @sk_kernel_function(description="SK test function", name="sk_test")
        def sk_decorated_func(x: int) -> int:
            """SK decorated function."""
            return x * 5

        # Create a function with our decorator
        @agently_function(description="SK test function", name="sk_test")
        def our_decorated_func(x: int) -> int:
            """Our decorated function."""
            return x * 5

        # Test direct usage of our decorator
        @agently_function
        def our_direct_func(x: int) -> int:
            """Our directly decorated function."""
            return x * 5

        # Check for the __kernel_function__ attribute
        assert hasattr(
            sk_decorated_func, "__kernel_function__"
        ), "SK decorated function missing __kernel_function__ attribute"
        assert (
            getattr(sk_decorated_func, "__kernel_function__") is True
        ), "SK __kernel_function__ attribute should be True"

        # Ensure our decorated functions also have this attribute
        assert hasattr(
            our_decorated_func, "__kernel_function__"
        ), "Our decorated function missing __kernel_function__ attribute"
        assert (
            getattr(our_decorated_func, "__kernel_function__") is True
        ), "Our __kernel_function__ attribute should be True"

        assert hasattr(
            our_direct_func, "__kernel_function__"
        ), "Our direct decorated function missing __kernel_function__ attribute"
        assert (
            getattr(our_direct_func, "__kernel_function__") is True
        ), "Our direct __kernel_function__ attribute should be True"

        # Verify function execution still works
        assert our_decorated_func(5) == 25
        assert our_direct_func(5) == 25

    except ImportError:
        pytest.skip("semantic_kernel not available, skipping integration test")
