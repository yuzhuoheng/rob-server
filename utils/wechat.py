import httpx
from fastapi import HTTPException
import os
from typing import Dict

class WechatAPI:
    """微信API工具类"""
    
    def __init__(self):
        # 从环境变量获取微信小程序配置
        self.app_id = os.getenv("wx32842e0cc8a17d1c")
        self.app_secret = os.getenv("6e42b0fb73f26434ea65069dc42cc846")
        
        if not self.app_id or not self.app_secret:
            raise ValueError("请设置 WECHAT_APP_ID 和 WECHAT_APP_SECRET 环境变量")
    
    async def get_user_info(self, openid: str) -> Dict[str, str]:
        """
        获取微信用户信息
        
        Args:
            openid: 用户的openid
            
        Returns:
            Dict: 包含用户信息的字典
            {
                "nickname": "用户昵称",
                "avatar_url": "头像URL",
                "openid": "用户openid"
            }
            
        Raises:
            HTTPException: 当调用微信API失败时
        """
        try:
            # 获取接口调用凭证
            access_token_url = (
                f"https://api.weixin.qq.com/cgi-bin/token"
                f"?grant_type=client_credential"
                f"&appid={self.app_id}"
                f"&secret={self.app_secret}"
            )
            
            async with httpx.AsyncClient() as client:
                # 获取access_token
                response = await client.get(access_token_url)
                token_data = response.json()
                
                if "access_token" not in token_data:
                    raise HTTPException(
                        status_code=500,
                        detail=f"获取微信access_token失败: {token_data.get('errmsg', '未知错误')}"
                    )
                
                access_token = token_data["access_token"]
                
                # 获取用户信息
                user_info_url = (
                    f"https://api.weixin.qq.com/cgi-bin/user/info"
                    f"?access_token={access_token}"
                    f"&openid={openid}"
                    f"&lang=zh_CN"
                )
                
                response = await client.get(user_info_url)
                user_data = response.json()
                
                if "errcode" in user_data:
                    raise HTTPException(
                        status_code=500,
                        detail=f"获取微信用户信息失败: {user_data.get('errmsg', '未知错误')}"
                    )
                
                return {
                    "nickname": user_data.get("nickname", ""),
                    "avatar_url": user_data.get("headimgurl", ""),
                    "openid": openid
                }
                
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"调用微信API失败: {str(e)}"
            ) 