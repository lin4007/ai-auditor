import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载配置
load_dotenv()

# 初始化不同平台的客户端 (它们都兼容 OpenAI 格式)
client_sf = OpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"), 
    base_url="https://api.siliconflow.cn/v1"
)

client_groq = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"), 
    base_url="https://api.groq.com/openai/v1"
)

def get_ai_response(client, model, prompt):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3 # 降低随机性，利于逻辑测试
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error with {model}: {str(e)}"

# 设计一个“逻辑陷阱”任务 (结合你的专业背景)
test_prompt = """
[Context]
A batch of heat-sensitive medication arrived at the warehouse. 
The standard storage temperature is 2°C to 8°C. 
The log shows: 14:00 (4°C), 15:00 (12°C for 45 mins), 16:00 (5°C).

[Task]
1. Based on GSP (Good Supply Practice) principles, is this batch acceptable?
2. If the total value is $50,000 and the current exchange rate is 1 USD = 7.23 CNY, 
   but the auditor mistakenly used 1 USD = 6.5 CNY, calculate the 'Hidden Financial Gap' 
   caused by this exchange rate error in CNY.
3. Provide a 3-step action plan for the Quality Manager.
"""

print("🚀 Starting Logic Audit...")

# 运行对比
models = [
    {"client": client_sf, "name": "DeepSeek-V3", "id": "deepseek-ai/DeepSeek-V3"},
    {"client": client_groq, "name": "Llama-3.3-70b", "id": "llama-3.3-70b-versatile"}
]

results = {}
for m in models:
    print(f"--- Querying {m['name']} ---")
    results[m['name']] = get_ai_response(m['client'], m['id'], test_prompt)

# 保存结果到本地文件，方便以后上传 GitHub 展示
with open("audit_report.txt", "w", encoding="utf-8") as f:
    for name, content in results.items():
        f.write(f"=== MODEL: {name} ===\n{content}\n\n")

print("✅ Audit complete! Results saved to audit_report.txt")