"""测试配置模块"""

import os
import pytest
import yaml
from config import Config, config


class TestConfig:
    """配置类测试"""

    def test_singleton_pattern(self):
        """测试单例模式"""
        config1 = Config()
        config2 = Config()
        assert config1 is config2

    def test_get_config(self):
        """测试获取配置"""
        # 测试获取存在的配置
        websocket_url = config.get('WEBSOCKET_URL')
        assert websocket_url is not None
        
        # 测试获取不存在的配置,返回默认值
        result = config.get('NON_EXISTENT_KEY', 'default')
        assert result == 'default'

    def test_get_nested_config(self):
        """测试获取嵌套配置"""
        # 测试多级配置获取
        auto_reply_enabled = config.get('AUTO_REPLY.enabled')
        assert auto_reply_enabled is not None

    def test_set_config(self):
        """测试设置配置"""
        test_key = 'TEST_KEY'
        test_value = 'test_value'
        
        config.set(test_key, test_value)
        assert config.get(test_key) == test_value

    def test_set_nested_config(self):
        """测试设置嵌套配置"""
        config.set('TEST.NESTED.KEY', 'value')
        assert config.get('TEST.NESTED.KEY') == 'value'

    def test_env_override(self, monkeypatch):
        """测试环境变量覆盖配置"""
        # 设置环境变量
        monkeypatch.setenv('HEARTBEAT_INTERVAL', '30')
        
        # 环境变量应该覆盖配置文件
        result = config.get('HEARTBEAT_INTERVAL')
        assert result == 30

    def test_env_value_conversion(self):
        """测试环境变量值类型转换"""
        # 测试布尔值转换
        assert config._convert_env_value('true') is True
        assert config._convert_env_value('false') is False
        assert config._convert_env_value('1') is True
        assert config._convert_env_value('0') is False
        
        # 测试数字转换
        assert config._convert_env_value('123') == 123
        assert config._convert_env_value('3.14') == 3.14
        
        # 测试字符串
        assert config._convert_env_value('hello') == 'hello'

    def test_validate_config(self):
        """测试配置验证"""
        # 配置应该包含必需的键
        assert config.validate() is True

    def test_config_property(self):
        """测试获取完整配置"""
        full_config = config.config
        assert isinstance(full_config, dict)
        assert 'WEBSOCKET_URL' in full_config or 'AUTO_REPLY' in full_config


class TestConfigFile:
    """配置文件操作测试"""

    def test_save_and_reload(self, tmp_path):
        """测试保存和重新加载配置"""
        # 创建临时配置文件
        config_file = tmp_path / "test_config.yml"
        test_config = {
            'TEST_KEY': 'test_value',
            'NESTED': {
                'KEY': 'value'
            }
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(test_config, f, allow_unicode=True)
        
        # 验证文件内容
        with open(config_file, 'r', encoding='utf-8') as f:
            loaded_config = yaml.safe_load(f)
        
        assert loaded_config['TEST_KEY'] == 'test_value'
        assert loaded_config['NESTED']['KEY'] == 'value'
