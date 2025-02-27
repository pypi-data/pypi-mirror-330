import pytest
from xcryptowatch.gpt import _create_gpt_message, analyze_post
import openai

@pytest.mark.asyncio
async def test_analyze_post_no_crypto():
    post = "Just had a great lunch at the new restaurant!"
    result = await analyze_post(post)
    assert result == "nothing"

@pytest.mark.asyncio
async def test_analyze_post_with_crypto():
    post = "Bitcoin price is soaring today! Very bullish on crypto markets."
    result = await analyze_post(post)
    assert result is not None
    assert result != "nothing"
    assert "Bitcoin" in result or "crypto" in result

def test_create_gpt_message():
    test_post = "Test post content"
    messages = _create_gpt_message(test_post)
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == test_post 