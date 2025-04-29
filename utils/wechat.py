import aiohttp
from fastapi import HTTPException
import os
from typing import Dict
import random
import string
import ssl
import certifi

class WechatAPI:
    """微信API工具类"""
    
    def __init__(self):
        # 从环境变量获取微信小程序配置
        self.app_id = os.getenv("WECHAT_APP_ID", "wx32842e0cc8a17d1c")
        self.app_secret = os.getenv("WECHAT_APP_SECRET", "6e42b0fb73f26434ea65069dc42cc846")
        if not self.app_id or not self.app_secret:
            raise ValueError("请设置 WECHAT_APP_ID 和 WECHAT_APP_SECRET 环境变量")
        self.session = None
    
    async def get_session(self):
        """
        获取或创建 aiohttp 会话
        
        Returns:
            aiohttp.ClientSession: aiohttp 会话对象
        """
        if self.session is None:
            # 创建 SSL 上下文，禁用证书验证
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            self.session = aiohttp.ClientSession(connector=connector)
        return self.session

    async def get_openid(self, code: str) -> str:
        """
        通过 code 获取用户 openid
        
        Args:
            code: 小程序登录时获取的 code
            
        Returns:
            str: 用户的 openid
            
        Raises:
            HTTPException: 当调用微信API失败时
        """
        try:
            # 使用 code2session 接口获取用户 openid
            url = (
                f"https://api.weixin.qq.com/sns/jscode2session"
                f"?appid={self.app_id}"
                f"&secret={self.app_secret}"
                f"&js_code={code}"
                f"&grant_type=authorization_code"
            )
            print(self.app_id)
            print(self.app_secret)
            print(code)
            
            session = await self.get_session()
            async with session.get(url, ssl=False) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=500,
                        detail=f"微信API请求失败，状态码: {response.status}"
                    )
                    
                data = await response.json()
                if "errcode" in data and data["errcode"] != 0:
                    raise HTTPException(
                        status_code=500,
                        detail=f"微信API返回错误: {data['errmsg']}"
                    )
                
                return data.get("openid", "")
                
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"调用微信API失败: {str(e)}"
            )
    
    @staticmethod
    def generate_robot_name() -> str:
        """生成机器人名称"""
        # 生成4位随机字符（数字和大写字母的组合）
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"机器人_{random_chars}"

if __name__ == "__main__":
    import asyncio
    api = WechatAPI()
    # 注意：这里需要传入从小程序获取的 code，而不是 openid
    # code 的有效期很短，需要在小程序端调用 wx.login() 获取
    test_code = "0f1FLSkl2VW5uf4kv6ml2kkepN1FLSkA"  # 这里需要替换为真实的code
    res = asyncio.run(api.get_openid(test_code))
    print(res)
