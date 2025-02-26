# **One2x-sdk**

SDK for One2x Developer

---

## **快速开始**

### **初始化客户端**

```python
from one2x_sdk import CoreApiClient

client = CoreApiClient(
    base_url="https://api.example.com",  # API 基础 URL（可选）
    token="your-token",                 # 认证 Token（可选）
    enable_requests=True                # 是否启用请求（可选，默认 False）
)
```

默认配置  
1. base_url：http://localhost:3000
2. token：default-token 
3. enable_requests：False
4. 
可通过以下环境变量覆盖默认配置：
1. MEDEO_CORE_API_BASE_URL：API 基础 URL 
2. MEDEO_CORE_API_AUTH_TOKEN：认证 Token 
3. MEDEO_CORE_API_ENABLE_REQUESTS：是否启用请求（"true" 或 "false"）