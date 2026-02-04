import asyncio
import yaml
import time
import os
from datetime import datetime
from playwright.async_api import async_playwright

async def update_config(cookie_str):
    """更新 global_config.yml 中的 Cookie"""
    config_path = 'global_config.yml'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if 'COOKIES' not in config:
            config['COOKIES'] = {}
            
        config['COOKIES']['value'] = cookie_str
        config['COOKIES']['last_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(config, f, allow_unicode=True, sort_keys=False)
            
        print(f"\n[√] 配置文件已更新！")
        print(f"[√] 更新时间: {config['COOKIES']['last_update_time']}")
        return True
    except Exception as e:
        print(f"\n[×] 更新配置文件失败: {e}")
        return False

async def run():
    async with async_playwright() as p:
        # 启动浏览器
        print("[1/3] 正在启动浏览器...")
        # 尝试使用系统的 Chrome 浏览器，由于闲鱼对反爬要求极高，系统浏览器指纹更真实
        browser = await p.chromium.launch(channel="chrome", headless=False, args=["--disable-blink-features=AutomationControlled"]) 
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        )
        
        # 注入脚本，进一步隐藏自动化特征
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        page = await context.new_page()
        
        # 用于实时存储拦截到的 Cookie
        intercepted_cookies = {}

        # 拦截响应，捕获最新的 set-cookie
        async def handle_response(response):
            if "goofish.com" in response.url or "m.taobao.com" in response.url:
                headers = response.headers
                if "set-cookie" in headers:
                    # 简单解析 set-cookie (这里仅作辅助，主要还是靠 context.cookies())
                    pass

        page.on("response", handle_response)

        print("[2/3] 正在打开闲鱼官网，请在弹出的浏览器中完成登录...")
        await page.goto("https://www.goofish.com/")
        
        print("\n" + "="*50)
        print("提示：请在浏览器窗口中完成扫码登录或短信登录。")
        print("登录成功后，程序会自动识别并保存 Cookie。")
        print("="*50 + "\n")

        # 监控登录状态
        logged_in = False
        start_time = time.time()
        timeout = 300 # 5分钟超时

        while not logged_in:
            if time.time() - start_time > timeout:
                print("\n[!] 登录超时，请重新运行脚本。")
                break

            try:
                # 获取当前的所有 cookies
                cookies = await context.cookies()
                cookie_dict = {c['name']: c['value'] for c in cookies}
                
                # 关键：检查是否包含 unb 字段，这是登录成功的标志
                if 'unb' in cookie_dict:
                    # 检查是否包含核心安全字段 x5sec
                    if 'x5sec' in cookie_dict:
                        print("[3/3] 检测到登录成功且获取到安全权标！正在提取 Cookie...")
                        
                        # 格式化
                        cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
                        
                        # 更新配置
                        if await update_config(cookie_str):
                            logged_in = True
                        break
                    else:
                        # 即使不包含 x5sec，如果 unb 已经稳定存在，也可以尝试提取
                        # 有时候 x5sec 会稍晚一点点出现
                        await asyncio.sleep(1)
                        continue
                
                if page.is_closed():
                    print("\n[!] 浏览器窗口已关闭，任务取消。")
                    break
                    
                await asyncio.sleep(1)
            except Exception as e:
                print(f"监控中出现错误: {e}")
                break

        if logged_in:
            print("\n[√] 恭喜！Cookie 已成功捕获并保存。")
            print("您现在可以关闭此窗口，并运行: python Start.py")
            # 保持窗口一会，让用户确认
            await asyncio.sleep(5)
        
        await browser.close()


if __name__ == "__main__":
    if not os.path.exists('global_config.yml'):
        print("[×] 错误：未找到 global_config.yml 文件，请在项目根目录下运行。")
    else:
        try:
            asyncio.run(run())
        except KeyboardInterrupt:
            print("\n[!] 用户中断运行。")
