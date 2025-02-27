"""Tests for NotifierFactory."""

# Import built-in modules
from typing import Any, Dict
from unittest.mock import patch

# Import third-party modules
import pytest

# Import local modules
from notify_bridge.components import BaseNotifier, NotificationSchema
from notify_bridge.exceptions import NoSuchNotifierError, NotificationError
from notify_bridge.factory import NotifierFactory
from notify_bridge.utils import HTTPClientConfig


class TestSchema(NotificationSchema):
    """Test data schema."""

    model_config = {"extra": "allow"}


class TestNotifier(BaseNotifier):
    """Test notifier."""

    name = "test"
    schema = TestSchema

    def __init__(self, config: HTTPClientConfig = None, **kwargs: Any) -> None:
        """Initialize test notifier.

        Args:
            config: HTTP client configuration.
            **kwargs: Additional arguments.
        """
        super().__init__(config)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def assemble_data(self, data: NotificationSchema) -> Dict[str, Any]:
        """Build payload for data.

        Args:
            data: Notification data.

        Returns:
            Dict[str, Any]: API payload.
        """
        return {"url": data.webhook_url, "json": {"content": data.content, "title": data.title}}

    def send(self, notification: NotificationSchema) -> Dict[str, Any]:
        """Send data.

        Args:
            notification: Notification data.

        Returns:
            Dict[str, Any]: Response data.
        """
        return {"success": True, "name": "test", "message": "Notification sent successfully", "data": {"success": True}}

    async def send_async(self, notification: NotificationSchema) -> Dict[str, Any]:
        """Send data asynchronously.

        Args:
            notification: Notification data.

        Returns:
            Dict[str, Any]: Response data.
        """
        return {"success": True, "name": "test", "message": "Notification sent successfully", "data": {"success": True}}

    def notify(self, notification: Dict[str, Any]) -> Dict[str, Any]:
        """Send data synchronously.

        Args:
            notification: Notification data.

        Returns:
            Dict[str, Any]: Response data.

        Raises:
            NotificationError: If data validation fails.
        """
        if isinstance(notification, dict):
            try:
                notification = self.schema(**notification)
            except Exception as e:
                raise NotificationError(str(e))
        return self.send(notification)

    async def notify_async(self, notification: Dict[str, Any]) -> Dict[str, Any]:
        """Send data asynchronously.

        Args:
            notification: Notification data.

        Returns:
            Dict[str, Any]: Response data.

        Raises:
            NotificationError: If data validation fails.
        """
        if isinstance(notification, dict):
            try:
                notification = self.schema(**notification)
            except Exception as e:
                raise NotificationError(str(e))
        return await self.send_async(notification)


@pytest.fixture
def factory() -> NotifierFactory:
    """Create a NotifierFactory instance."""
    factory = NotifierFactory()
    return factory


@pytest.fixture
def test_notifier() -> TestNotifier:
    """Create test notifier fixture."""
    return TestNotifier()


@pytest.fixture
def test_data() -> Dict[str, Any]:
    """Create test data fixture."""
    return {"webhook_url": "https://example.com", "title": "Test Title", "content": "Test Content", "msg_type": "text"}


def test_register_notifier(factory: NotifierFactory) -> None:
    """Test registering a notifier."""
    factory.register_notifier("test", TestNotifier)
    assert factory.get_notifier_class("test") == TestNotifier


def test_unregister_notifier(factory: NotifierFactory) -> None:
    """Test unregistering a notifier."""
    factory.register_notifier("test", TestNotifier)
    factory.unregister_notifier("test")
    assert "test" not in factory.get_notifier_names()


def test_get_notifier_names(factory: NotifierFactory) -> None:
    """Test getting notifier names."""
    factory.register_notifier("test", TestNotifier)
    assert "test" in factory.get_notifier_names()


def test_get_notifier_class(factory: NotifierFactory) -> None:
    """Test getting notifier class."""
    factory.register_notifier("test", TestNotifier)
    assert factory.get_notifier_class("test") == TestNotifier


def test_create_notifier(factory: NotifierFactory) -> None:
    """Test creating a notifier."""
    factory.register_notifier("test", TestNotifier)
    config = HTTPClientConfig()
    notifier = factory.create_notifier("test", config)
    assert isinstance(notifier, TestNotifier)


def test_create_notifier_invalid(factory: NotifierFactory) -> None:
    """Test creating an invalid notifier."""
    config = HTTPClientConfig()
    with pytest.raises(NoSuchNotifierError):
        factory.create_notifier("invalid", config)


def test_notify_success(factory: NotifierFactory, test_data: Dict[str, Any]) -> None:
    """Test successful data."""
    factory.register_notifier("test", TestNotifier)
    response = factory.send("test", test_data)

    assert response["success"] is True
    assert response["name"] == "test"
    assert response["message"] == "Notification sent successfully"
    assert response["data"] == {"success": True}


@pytest.mark.asyncio
async def test_notify_async_success(factory: NotifierFactory, test_data: Dict[str, Any]) -> None:
    """Test successful async data."""
    factory.register_notifier("test", TestNotifier)
    response = await factory.send_async("test", test_data)

    assert response["success"] is True
    assert response["name"] == "test"
    assert response["message"] == "Notification sent successfully"
    assert response["data"] == {"success": True}


def test_notify_with_none_notification(notify_factory: NotifierFactory) -> None:
    """Test notification with None data."""
    with pytest.raises(NotificationError):
        notify_factory.send("test", data=None)


@pytest.mark.asyncio
async def test_notify_async_with_none_notification(notify_factory: NotifierFactory) -> None:
    """Test async notification with None data."""
    with pytest.raises(NotificationError):
        await notify_factory.send_async("test", data=None)


def test_notify_notifier_not_found(factory: NotifierFactory, test_data: Dict[str, Any]) -> None:
    """Test data with non-existent notifier."""
    with pytest.raises(NoSuchNotifierError):
        factory.send("non_existent", test_data)


@pytest.mark.asyncio
async def test_notify_async_notifier_not_found(factory: NotifierFactory, test_data: Dict[str, Any]) -> None:
    """Test async data with non-existent notifier."""
    with pytest.raises(NoSuchNotifierError):
        await factory.send_async("non_existent", test_data)


def test_create_notifier_with_kwargs(factory: NotifierFactory) -> None:
    """Test creating a notifier with additional kwargs."""
    factory.register_notifier("test", TestNotifier)
    config = HTTPClientConfig()
    notifier = factory.create_notifier("test", config, custom_param="test")
    assert isinstance(notifier, TestNotifier)
    assert hasattr(notifier, "custom_param")
    assert notifier.custom_param == "test"


@pytest.mark.asyncio
async def test_create_async_notifier(factory: NotifierFactory) -> None:
    """Test creating an async notifier."""
    factory.register_notifier("test", TestNotifier)
    config = HTTPClientConfig()
    notifier = await factory.create_async_notifier("test", config)
    assert isinstance(notifier, TestNotifier)


@pytest.mark.asyncio
async def test_create_async_notifier_invalid(factory: NotifierFactory) -> None:
    """Test creating an invalid async notifier."""
    config = HTTPClientConfig()
    with pytest.raises(NoSuchNotifierError):
        await factory.create_async_notifier("invalid", config)


def test_notify_with_kwargs(factory: NotifierFactory) -> None:
    """Test data with kwargs instead of data object."""
    factory.register_notifier("test", TestNotifier)
    response = factory.send(
        "test", webhook_url="https://example.com", title="Test Title", content="Test Content", msg_type="text"
    )

    assert response["success"] is True
    assert response["name"] == "test"
    assert response["message"] == "Notification sent successfully"
    assert response["data"] == {"success": True}


@pytest.mark.asyncio
async def test_notify_async_with_kwargs(factory: NotifierFactory) -> None:
    """Test async data with kwargs instead of data object."""
    factory.register_notifier("test", TestNotifier)
    response = await factory.send_async(
        "test", webhook_url="https://example.com", title="Test Title", content="Test Content", msg_type="text"
    )

    assert response["success"] is True
    assert response["name"] == "test"
    assert response["message"] == "Notification sent successfully"
    assert response["data"] == {"success": True}


def test_unregister_nonexistent_notifier(factory: NotifierFactory) -> None:
    """Test unregistering a non-existent notifier."""
    # Should not raise any exception
    factory.unregister_notifier("non_existent")


def test_factory_initialization() -> None:
    """Test factory initialization and plugin loading."""
    with patch("notify_bridge.factory.get_all_notifiers") as mock_get_notifiers:
        mock_get_notifiers.return_value = {"test": TestNotifier}
        factory = NotifierFactory()
        assert "test" in factory.get_notifier_names()
        mock_get_notifiers.assert_called_once()


@pytest.fixture
def notify_factory() -> NotifierFactory:
    """Create a NotifierFactory instance."""
    factory = NotifierFactory()
    factory.register_notifier("test", TestNotifier)
    return factory
