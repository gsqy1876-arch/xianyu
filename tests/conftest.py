"""Pytest 配置和共享 fixtures"""

import pytest
import os
import sys

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def sample_config():
    """示例配置数据"""
    return {
        'WEBSOCKET_URL': 'wss://test.example.com/',
        'HEARTBEAT_INTERVAL': 15,
        'AUTO_REPLY': {
            'enabled': True,
            'paid_message': 'Test message'
        }
    }


@pytest.fixture
def temp_config_file(tmp_path, sample_config):
    """创建临时配置文件"""
    import yaml
    
    config_file = tmp_path / "global_config.yml"
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.safe_dump(sample_config, f, allow_unicode=True)
    
    return config_file
