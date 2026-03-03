import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件中的 API Keys
load_dotenv()

def get_cloudflare_response(user_prompt):
    """
    获取 Cloudflare Workers AI (DeepSeek-R1) 的模型回复
    """
    try:
        account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        api_token = os.getenv("CLOUDFLARE_API_TOKEN")

        base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1"

        client_cf = OpenAI(
            api_key=api_token,
            base_url=base_url
        )

# 核心修复：更换为 Cloudflare 官方文档目前最稳定的 R1 ID
        response = client_cf.chat.completions.create(
            model="@cf/deepseek-ai/deepseek-r1-distill-qwen-32b",
            messages=[{"role": "user", "content": user_prompt}],
            timeout=25
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Cloudflare 连接失败: {str(e)}\n请检查 Account ID 和 Token 是否正确。"

def get_groq_response(user_prompt):
    """
    获取 Groq (Llama) 的模型回复
    """
    try:
        client_gr = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )

        response = client_gr.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": user_prompt}],
            timeout=15
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Groq 连接失败: {str(e)}\n请确保终端已运行代理设置命令。"