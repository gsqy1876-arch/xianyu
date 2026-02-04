"""闲鱼自动回复系统启动脚本

主程序入口,负责初始化和启动闲鱼自动回复服务。
"""

import os
import sys
import asyncio
import signal
from loguru import logger
from XianyuAutoAsync import XianyuLive
from config import config


def setup_logging() -> None:
    """配置日志系统"""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    logger.remove()  # 移除默认处理器
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    )
    logger.info(f"日志级别: {log_level}")


def check_environment() -> bool:
    """检查运行环境
    
    Returns:
        环境检查是否通过
    """
    # 检查配置文件
    if not config.validate():
        logger.error("配置验证失败,请检查 global_config.yml")
        return False
    
    # 检查 Cookie
    cookies_str = config.get('COOKIES.value', '')
    if not cookies_str:
        logger.warning("未找到有效的 Cookie,请先运行: python login_helper.py")
        return False
    
    logger.info("环境检查通过")
    return True


def signal_handler(signum, frame) -> None:
    """信号处理器,用于优雅退出"""
    logger.info(f"收到信号 {signum},正在退出...")
    sys.exit(0)


async def main() -> None:
    """主函数"""
    # 设置日志
    setup_logging()
    
    logger.info("=" * 60)
    logger.info("闲鱼自动回复系统启动中...")
    logger.info("=" * 60)
    
    # 检查环境
    if not check_environment():
        logger.error("环境检查失败,程序退出")
        sys.exit(1)
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # 获取 Cookie (优先从环境变量)
        cookies_str = os.getenv('COOKIES_STR') or config.get('COOKIES.value', '')
        
        # 创建并启动服务
        logger.info("正在初始化闲鱼服务...")
        xianyu_live = XianyuLive(cookies_str)
        
        logger.info("服务启动成功,开始监听消息...")
        await xianyu_live.main()
        
    except KeyboardInterrupt:
        logger.info("用户中断程序")
    except Exception as e:
        logger.exception(f"程序运行出错: {e}")
        sys.exit(1)
    finally:
        logger.info("程序已退出")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序已停止")
 