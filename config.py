"""配置管理模块

提供全局配置的加载、读取、修改和保存功能。
支持从 YAML 配置文件和环境变量加载配置。
"""

import os
import yaml
from typing import Dict, Any, Optional
from datetime import datetime
from loguru import logger

try:
    from dotenv import load_dotenv
    load_dotenv()  # 加载 .env 文件
except ImportError:
    logger.warning("python-dotenv 未安装,无法从 .env 文件加载环境变量")


class Config:
    """配置管理类
    
    用于加载和管理全局配置文件(global_config.yml)。
    支持配置的读取、修改和保存,以及环境变量覆盖。
    
    使用单例模式确保全局只有一个配置实例。
    """
    
    _instance: Optional['Config'] = None
    _config: Dict[str, Any] = {}
    _config_path: str = ""

    def __new__(cls) -> 'Config':
        """单例模式实现"""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self) -> None:
        """加载配置文件
        
        从 global_config.yml 文件中加载配置信息。
        如果文件不存在则创建默认配置。
        
        Raises:
            yaml.YAMLError: YAML 文件格式错误
        """
        self._config_path = os.path.join(os.path.dirname(__file__), 'global_config.yml')
        
        if not os.path.exists(self._config_path):
            logger.warning(f"配置文件不存在: {self._config_path}, 将创建默认配置")
            self._create_default_config()
            return

        try:
            with open(self._config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
            logger.info(f"配置文件加载成功: {self._config_path}")
        except yaml.YAMLError as e:
            logger.error(f"配置文件格式错误: {e}")
            raise
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            raise

    def _create_default_config(self) -> None:
        """创建默认配置文件"""
        default_config = {
            'WEBSOCKET_URL': 'wss://wss-goofish.dingtalk.com/',
            'HEARTBEAT_INTERVAL': 15,
            'HEARTBEAT_TIMEOUT': 5,
            'TOKEN_REFRESH_INTERVAL': 3600,
            'TOKEN_RETRY_INTERVAL': 300,
            'MESSAGE_EXPIRE_TIME': 300000,
            'AUTO_REPLY': {
                'enabled': True,
                'enable_chat_reply': False,
                'paid_message': '感谢购买!',
                'api': {
                    'enabled': False,
                    'url': 'http://localhost:8080/xianyu/reply',
                    'timeout': 10
                }
            },
            'LOG_CONFIG': {
                'level': 'INFO',
                'rotation': '10 MB',
                'retention': '7 days'
            },
            'COOKIES': {
                'value': '',
                'last_update_time': ''
            }
        }
        self._config = default_config
        self.save()

    def reload(self) -> None:
        """重新加载配置文件"""
        logger.info("重新加载配置文件")
        self._load_config()

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项
        
        支持从环境变量覆盖配置。环境变量优先级高于配置文件。
        
        Args:
            key: 配置项的键,支持点号分隔的多级键 (如 'AUTO_REPLY.enabled')
            default: 当配置项不存在时返回的默认值
            
        Returns:
            配置项的值或默认值
            
        Examples:
            >>> config.get('WEBSOCKET_URL')
            'wss://wss-goofish.dingtalk.com/'
            >>> config.get('AUTO_REPLY.enabled', True)
            True
        """
        # 首先尝试从环境变量获取
        env_key = key.replace('.', '_').upper()
        env_value = os.getenv(env_key)
        if env_value is not None:
            # 尝试转换类型
            return self._convert_env_value(env_value)
        
        # 从配置文件获取
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    def _convert_env_value(self, value: str) -> Any:
        """转换环境变量值为合适的类型
        
        Args:
            value: 环境变量字符串值
            
        Returns:
            转换后的值
        """
        # 布尔值转换
        if value.lower() in ('true', 'yes', '1'):
            return True
        if value.lower() in ('false', 'no', '0'):
            return False
        
        # 数字转换
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        
        return value

    def set(self, key: str, value: Any) -> None:
        """设置配置项
        
        Args:
            key: 配置项的键,支持点号分隔的多级键
            value: 要设置的值
            
        Examples:
            >>> config.set('AUTO_REPLY.enabled', False)
            >>> config.set('HEARTBEAT_INTERVAL', 30)
        """
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        logger.debug(f"配置项已更新: {key} = {value}")

    def save(self) -> None:
        """保存配置到文件
        
        将当前配置保存回 global_config.yml 文件
        
        Raises:
            IOError: 文件写入失败
        """
        try:
            with open(self._config_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self._config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            logger.info(f"配置文件已保存: {self._config_path}")
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
            raise

    def validate(self) -> bool:
        """验证配置完整性
        
        Returns:
            配置是否有效
        """
        required_keys = [
            'WEBSOCKET_URL',
            'HEARTBEAT_INTERVAL',
            'AUTO_REPLY'
        ]
        
        for key in required_keys:
            if self.get(key) is None:
                logger.error(f"缺少必需的配置项: {key}")
                return False
        
        logger.info("配置验证通过")
        return True

    @property
    def config(self) -> Dict[str, Any]:
        """获取完整配置
        
        Returns:
            包含所有配置项的字典
        """
        return self._config


# 创建全局配置实例
config = Config()

# 导出常用配置项
COOKIES_STR = config.get('COOKIES.value', '')
COOKIES_LAST_UPDATE = config.get('COOKIES.last_update_time', '')
WEBSOCKET_URL = config.get('WEBSOCKET_URL', 'wss://wss-goofish.dingtalk.com/')
HEARTBEAT_INTERVAL = config.get('HEARTBEAT_INTERVAL', 15)
HEARTBEAT_TIMEOUT = config.get('HEARTBEAT_TIMEOUT', 5)
TOKEN_REFRESH_INTERVAL = config.get('TOKEN_REFRESH_INTERVAL', 3600)
TOKEN_RETRY_INTERVAL = config.get('TOKEN_RETRY_INTERVAL', 300)
MESSAGE_EXPIRE_TIME = config.get('MESSAGE_EXPIRE_TIME', 300000)
API_ENDPOINTS = config.get('API_ENDPOINTS', {})
DEFAULT_HEADERS = config.get('DEFAULT_HEADERS', {})
WEBSOCKET_HEADERS = config.get('WEBSOCKET_HEADERS', {})
APP_CONFIG = config.get('APP_CONFIG', {})
AUTO_REPLY = config.get('AUTO_REPLY', {
    'enabled': True,
    'default_message': '亲爱的"{send_user_name}" 老板你好！所有宝贝都可以拍，秒发货的哈~不满意的话可以直接申请退款哈~',
    'api': {
        'enabled': False,
        'url': 'http://localhost:8080/xianyu/reply',
        'timeout': 10
    }
})
MANUAL_MODE = config.get('MANUAL_MODE', {})
LOG_CONFIG = config.get('LOG_CONFIG', {})
 