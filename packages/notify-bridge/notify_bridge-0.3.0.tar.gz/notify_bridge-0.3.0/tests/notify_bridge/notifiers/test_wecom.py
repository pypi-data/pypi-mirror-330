"""Test WeCom notifier implementation."""

# Import built-in modules
from pathlib import Path

# Import third-party modules
import pytest

# Import local modules
from notify_bridge.components import MessageType
from notify_bridge.exceptions import NotificationError
from notify_bridge.notifiers.wecom import Article, WeComNotifier, WeComSchema


def test_article_schema():
    """Test Article schema."""
    # Test valid article
    article_data = {
        "title": "Test Title",
        "description": "Test Description",
        "url": "https://test.url",
        "picurl": "https://test.url/image.png",
    }
    article = Article(**article_data)
    assert article.title == "Test Title"
    assert article.description == "Test Description"
    assert article.url == "https://test.url"
    assert article.picurl == "https://test.url/image.png"

    # Test article without optional fields
    article = Article(title="Test Title", url="https://test.url")
    assert article.title == "Test Title"
    assert article.description is None
    assert article.url == "https://test.url"
    assert article.picurl is None


def test_wecom_notifier_initialization():
    """Test WeComNotifier initialization."""
    notifier = WeComNotifier()
    assert notifier.name == "wecom"
    assert notifier.schema_class == WeComSchema
    assert MessageType.TEXT in notifier.supported_types
    assert MessageType.MARKDOWN in notifier.supported_types
    assert MessageType.IMAGE in notifier.supported_types
    assert MessageType.NEWS in notifier.supported_types


def test_build_text_payload():
    """Test text message payload building."""
    notifier = WeComNotifier()

    # Test text message with mentions
    notification = WeComSchema(
        webhook_url="https://test.url",
        msg_type="text",
        content="Test content",
        mentioned_list=["user1", "user2"],
        mentioned_mobile_list=["12345678901"],
    )
    payload = notifier.assemble_data(notification)
    assert payload["msgtype"] == "text"
    assert payload["text"]["content"] == "Test content"
    assert payload["text"]["mentioned_list"] == ["user1", "user2"]
    assert payload["text"]["mentioned_mobile_list"] == ["12345678901"]

    # Test text message without mentions
    notification = WeComSchema(webhook_url="https://test.url", msg_type="text", content="Test content")
    payload = notifier.assemble_data(notification)
    assert payload["msgtype"] == "text"
    assert payload["text"]["content"] == "Test content"
    assert payload["text"]["mentioned_list"] == []
    assert payload["text"]["mentioned_mobile_list"] == []


def test_build_markdown_payload():
    """Test markdown message payload building."""
    notifier = WeComNotifier()

    # Test markdown message
    notification = WeComSchema(
        webhook_url="https://test.url", msg_type="markdown", content="# Test Title\n\nTest content"
    )
    payload = notifier.assemble_data(notification)
    assert payload["msgtype"] == "markdown"
    assert payload["markdown"]["content"] == "# Test Title\n\nTest content"


def test_build_image_payload():
    """Test image message payload building."""
    notifier = WeComNotifier()

    # Mock image data
    mock_base64 = "SGVsbG8gV29ybGQ="  # "Hello World" in base64
    mock_md5 = "ed076287532e86365e841e92bfc50d8c"  # MD5 of "Hello World"

    # Patch _encode_image method
    original_encode_image = notifier._encode_image
    try:
        notifier._encode_image = lambda _: (mock_base64, mock_md5)

        # Test image message
        notification = WeComSchema(webhook_url="https://test.url", msg_type="image", image_path="test.png")
        payload = notifier.assemble_data(notification)
        assert payload["msgtype"] == "image"
        assert payload["image"]["base64"] == mock_base64
        assert payload["image"]["md5"] == mock_md5
    finally:
        # Restore original method
        notifier._encode_image = original_encode_image


def test_build_news_payload():
    """Test news message payload building."""
    notifier = WeComNotifier()

    # Test news message
    notification = WeComSchema(
        webhook_url="https://test.url",
        msg_type="news",
        articles=[
            {
                "title": "Test Title",
                "description": "Test Description",
                "url": "https://test.url",
                "picurl": "https://test.url/image.png",
            }
        ],
    )
    payload = notifier.assemble_data(notification)
    assert payload["msgtype"] == "news"
    assert len(payload["news"]["articles"]) == 1
    assert payload["news"]["articles"][0]["title"] == "Test Title"
    assert payload["news"]["articles"][0]["description"] == "Test Description"
    assert payload["news"]["articles"][0]["url"] == "https://test.url"
    assert payload["news"]["articles"][0]["picurl"] == "https://test.url/image.png"


def test_build_file_payload():
    """Test file message payload building."""
    notifier = WeComNotifier()

    # Mock upload_media method
    original_upload_media = notifier._upload_media
    try:
        notifier._upload_media = lambda _, __: "test_media_id"

        # Test file message with media_path
        notification = WeComSchema(
            webhook_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key",
            msg_type="file",
            media_path="test.txt",
        )
        payload = notifier.assemble_data(notification)
        assert payload["msgtype"] == "file"
        assert payload["file"]["media_id"] == "test_media_id"

        # Test file message with media_id
        notification = WeComSchema(
            webhook_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key",
            msg_type="file",
            media_id="existing_media_id",
        )
        payload = notifier.assemble_data(notification)
        assert payload["msgtype"] == "file"
        assert payload["file"]["media_id"] == "existing_media_id"

        # Test file message without media_id or media_path
        notification = WeComSchema(
            webhook_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key", msg_type="file"
        )
        with pytest.raises(NotificationError, match="Either media_id or media_path is required"):
            notifier.assemble_data(notification)
    finally:
        # Restore original method
        notifier._upload_media = original_upload_media


def test_build_voice_payload():
    """Test voice message payload building."""
    notifier = WeComNotifier()

    # Mock upload_media method
    original_upload_media = notifier._upload_media
    try:
        notifier._upload_media = lambda _, __: "test_media_id"

        # Test voice message with media_path
        notification = WeComSchema(
            webhook_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key",
            msg_type="voice",
            media_path="test.amr",
        )
        payload = notifier.assemble_data(notification)
        assert payload["msgtype"] == "voice"
        assert payload["voice"]["media_id"] == "test_media_id"

        # Test voice message with media_id
        notification = WeComSchema(
            webhook_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key",
            msg_type="voice",
            media_id="existing_media_id",
        )
        payload = notifier.assemble_data(notification)
        assert payload["msgtype"] == "voice"
        assert payload["voice"]["media_id"] == "existing_media_id"

        # Test voice message without media_id or media_path
        notification = WeComSchema(
            webhook_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key", msg_type="voice"
        )
        with pytest.raises(NotificationError, match="Either media_id or media_path is required"):
            notifier.assemble_data(notification)
    finally:
        # Restore original method
        notifier._upload_media = original_upload_media


def test_upload_media_validation(tmp_path: Path):
    """Test media upload validation."""
    notifier = WeComNotifier()
    notifier._webhook_key = "test-key"  # Set webhook key for testing

    # Test file not found
    with pytest.raises(NotificationError, match="File not found"):
        notifier._upload_media("nonexistent_file.txt", "file")

    # Test file too small
    small_file = tmp_path / "small.txt"
    small_file.write_bytes(b"1234")  # 4 bytes
    with pytest.raises(NotificationError, match="File size must be greater than 5 bytes"):
        notifier._upload_media(str(small_file), "file")

    # Test file too large
    large_file = tmp_path / "large.txt"
    large_file.write_bytes(b"x" * (20 * 1024 * 1024 + 1))  # 20MB + 1 byte
    with pytest.raises(NotificationError, match="File size must not exceed 20MB"):
        notifier._upload_media(str(large_file), "file")

    # Test voice file too large
    large_voice = tmp_path / "large.amr"
    large_voice.write_bytes(b"x" * (2 * 1024 * 1024 + 1))  # 2MB + 1 byte
    with pytest.raises(NotificationError, match="Voice file size must not exceed 2MB"):
        notifier._upload_media(str(large_voice), "voice")


def test_webhook_key_extraction():
    """Test webhook key extraction from URL."""
    notifier = WeComNotifier()

    # Test simple URL
    notification = WeComSchema(
        webhook_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key", msg_type="text", content="test"
    )
    notifier.validate(notification)
    assert notifier._webhook_key == "test-key"

    # Test URL with additional parameters
    notification = WeComSchema(
        webhook_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key&other=param",
        msg_type="text",
        content="test",
    )
    notifier.validate(notification)
    assert notifier._webhook_key == "test-key"


def test_invalid_schema():
    """Test invalid schema handling."""
    notifier = WeComNotifier()
    with pytest.raises(NotificationError):
        notifier.assemble_data({"invalid": "data"})


def test_format_markdown():
    """Test markdown formatting."""
    notifier = WeComNotifier()

    # Test headers
    assert "# 标题1" in notifier._format_markdown("# 标题1")
    assert "## 标题2" in notifier._format_markdown("## 标题2")

    # Test lists
    assert "• 项目1" in notifier._format_markdown("- 项目1")
    assert "• 项目2" in notifier._format_markdown("* 项目2")
    assert "• 项目3" in notifier._format_markdown("+ 项目3")

    # Test ordered lists with Chinese numbers
    content = notifier._format_markdown("1. 项目1")
    assert "一、项目1" in content
    content = notifier._format_markdown("2. 项目2")
    assert "二、项目2" in content
    content = notifier._format_markdown("11. 项目11")
    assert "11." in content  # Numbers > 10 stay as is

    # Test horizontal rule
    content = notifier._format_markdown("---")
    assert "\n---\n" in content
    content = notifier._format_markdown("----")
    assert "\n---\n" in content

    # Test colored text with default colors
    colored_text = '<font color="info">提示信息</font>'
    assert colored_text in notifier._format_markdown(colored_text)

    # Test colored text with custom colors
    custom_color_map = {"success": "绿色", "error": "红色"}
    content = notifier._format_markdown(
        '<font color="success">成功</font>\n<font color="error">错误</font>', color_map=custom_color_map
    )
    assert '<font color="success">成功</font>' in content
    assert '<font color="error">错误</font>' in content

    # Test text formatting
    assert "**加粗文本**" in notifier._format_markdown("**加粗文本**")
    assert "*斜体文本*" in notifier._format_markdown("*斜体文本*")
    assert "*斜体文本*" in notifier._format_markdown("_斜体文本_")
    assert "`代码`" in notifier._format_markdown("`代码`")
    assert "> 引用" in notifier._format_markdown("> 引用")
    assert "[链接](https://example.com)" in notifier._format_markdown("[链接](https://example.com)")

    # Test complex markdown
    complex_md = """# 标题1
## 标题2

- 无序列表1
- 无序列表2

1. 有序列表1
2. 有序列表2

---

**加粗文本**
*斜体文本*
`代码示例`
> 引用文本

[链接](https://example.com)

<font color="info">提示信息</font>
<font color="warning">警告信息</font>"""

    formatted = notifier._format_markdown(complex_md)
    assert "# 标题1" in formatted
    assert "## 标题2" in formatted
    assert "• 无序列表1" in formatted
    assert "• 无序列表2" in formatted
    assert "一、有序列表1" in formatted
    assert "二、有序列表2" in formatted
    assert "\n---\n" in formatted
    assert "**加粗文本**" in formatted
    assert "*斜体文本*" in formatted
    assert "`代码示例`" in formatted
    assert "> 引用文本" in formatted
    assert "[链接](https://example.com)" in formatted
    assert '<font color="info">提示信息</font>' in formatted
    assert '<font color="warning">警告信息</font>' in formatted


def test_markdown_payload_with_custom_colors():
    """Test markdown payload with custom colors."""
    notifier = WeComNotifier()

    # Test with default colors
    data = WeComSchema(
        base_url="https://example.com", message='# 标题\n<font color="info">提示</font>', msg_type="markdown"
    )
    payload = notifier.assemble_data(data)
    assert '<font color="info">提示</font>' in payload["markdown"]["content"]

    # Test with custom colors
    data = WeComSchema(
        base_url="https://example.com",
        message='# 标题\n<font color="success">成功</font>',
        msg_type="markdown",
        color_map={"success": "绿色"},
    )
    payload = notifier.assemble_data(data)
    assert '<font color="success">成功</font>' in payload["markdown"]["content"]
