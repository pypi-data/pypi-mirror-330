import pytest
import os
import json
from xcryptowatch.config_json import load_config, _validate_config, twitter_enabled, truth_enabled, postal_enabled

@pytest.fixture
def valid_config():
    return {
        "version": "0.1.1",
        "twitter": {
            "bearer_token": "test_bearer",
            "consumer_key": "test_key",
            "consumer_secret": "test_secret",
            "access_token": "test_token",
            "access_token_secret": "test_token_secret",
            "check_interval": 15
        },
        "truth": {
            "username": "test_user",
            "password": "test_pass",
            "check_interval": 15
        },
        "openai": {
            "api_key": "test_openai_key"
        },
        "email": {
            "from_email": "test@example.com",
            "to_email": ["recipient@example.com"],
            "subject": "Test Subject",
            "postal": {
                "enabled": True,
                "server": "postal.example.com",
                "api_key": "test_postal_key"
            },
            "smtp": {
                "enabled": False,
                "host": "",
                "port": 587,
                "username": "",
                "password": "",
                "use_tls": True
            }
        },
        "watch_accounts": [
            {
                "username": "test_account",
                "platform": "twitter"
            }
        ]
    }

def test_validate_config(valid_config):
    assert _validate_config(valid_config) == True

def test_twitter_enabled(valid_config):
    assert twitter_enabled(valid_config) == True
    
    # Test with missing credentials
    invalid_config = valid_config.copy()
    invalid_config["twitter"]["bearer_token"] = ""
    assert twitter_enabled(invalid_config) == False

def test_truth_enabled(valid_config):
    assert truth_enabled(valid_config) == True
    
    # Test with missing credentials
    invalid_config = valid_config.copy()
    invalid_config["truth"]["username"] = ""
    assert truth_enabled(invalid_config) == False

def test_postal_enabled(valid_config):
    assert postal_enabled(valid_config) == True
    
    # Test with disabled postal
    invalid_config = valid_config.copy()
    invalid_config["email"]["postal"]["enabled"] = False
    assert postal_enabled(invalid_config) == False 