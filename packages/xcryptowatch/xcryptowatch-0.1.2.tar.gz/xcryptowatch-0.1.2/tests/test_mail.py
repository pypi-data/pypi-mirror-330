import pytest
from xcryptowatch.mail import send_analysis, status_update

@pytest.mark.asyncio
async def test_send_analysis(valid_config):
    analysis = "Test analysis content"
    await send_analysis(analysis, valid_config)

@pytest.mark.asyncio
async def test_status_update(valid_config):
    status = "Test status update"
    await status_update(status, valid_config)

@pytest.fixture
def mock_smtp(mocker):
    return mocker.patch('smtplib.SMTP')

def test_smtp_email(mock_smtp, valid_config):
    from xcryptowatch.mail import _send_smtp_email
    msg = "Test message"
    _send_smtp_email(valid_config['email']['smtp'], msg)
    mock_smtp.assert_called_once() 