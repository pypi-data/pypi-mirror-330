USTB-OpenAI-Py
==========
OpenAI style API for accessing the USTB hosted LLM  
北京科技大学 LLM 平台的客户端 API 库（基于 OpenAI 样式封装）

<sup> This project only supports Chinese docs. If you are an English user, feel free to contact us. </sup>

## 介绍 <sub>Intro</sub>

本项目旨在实现一个可以直接与“北京科技大学 LLM 平台”进行交互的客户端 API 库，并且在接口调用上与 [openai-python](https://github.com/openai/openai-python) 保持最大的一致性。

北京科技大学 LLM 平台（内网访问 http://chat.ustb.edu.cn ），其官方名称是“北科大 AI 助手”，它提供北科大本地部署的 LLM 的网页版对话服务。

## 使用方法 <sub>Usage</sub>

### 要求

1. 安装 [Python](https://www.python.org) >= 3.8
2. 安装以下依赖库：
   ```txt
   httpx>=0.28
   httpx-sse>=0.4
   pydantic>=2.10
   ```
3. 接入北科大的校园网。

### 准备令牌

> 自 2025 年 2 月 28 日起，服务器已经不允许游客登录（使用 `easy_session` Cookie），取而代之的是北科大 SSO 认证登录（使用 `cookie_vjuid_login` Cookie）。

在进行任何操作前，您需要通过北科大 SSO 认证，获得一个 `cookie_vjuid_login` Cookie 令牌。

您可以在网页版的开发人员工具中，直接复制此 Cookie 令牌的值。或者，您也可以通过我们的 [USTB-SSO](https://github.com/isHarryh/USTB-SSO) 库来进行认证：

1. 安装 `ustb-sso` 库；
2. 运行以下代码：
   ```python
   from ustb_sso import HttpxAuthSession, prefabs

   auth = HttpxAuthSession(**prefabs.CHAT_USTB_EDU_CN)

   print("Starting authentication...")
   auth.open_auth().use_wechat_auth().use_qr_code()

   with open("qr.png", "wb") as f:
       f.write(auth.get_qr_image())

   print("Waiting for confirmation... Please scan the QR code")
   pass_code = auth.wait_for_pass_code()

   print("Validating...")
   rsp = auth.complete_auth(pass_code)

   cookie_name = "cookie_vjuid_login"
   cookie_value = auth.client.cookies[cookie_name]
   print("Cookie:", cookie_name, "=", cookie_value)
   ```
 3. 在代码运行期间，会在本地生成 `qr.png` 图片文件。请使用微信扫描此图片中的二维码，从而完成认证；
 4. 顺利完成认证后，Cookie 令牌将被保存在 `cookie_value` 变量中。

> 可以将此令牌的值保存到本地，以便下次使用。需要注意，令牌可能具有有效时间限制。

### 快速上手

安装 `ustb-openai` 库：

```bash
pip install ustb-openai
```

以下示例代码实现了一个最简单的对话功能：

```python
from ustb_openai import USTBOpenAI

client = USTBOpenAI(vjuid_login=cookie_value)

print("Your user number:", client.info.get_user_info().user_number)

stream = client.chat.completions.create(
    messages=[
        { "role": "user", "content": "请介绍你自己。" },
    ],
    model="DeepSeek",
    stream=True
)

print("\nResponse:")
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

### 功能详解

#### 客户端与令牌

在客户端对象 `USTBOpenAI` 被实例化时，如果没有提供 `easy_session`（令牌）参数，那么服务器会自动授予一个新的游客令牌。

为避免创建过多的游客令牌，您可以保存现有的令牌到本地，以便下次使用。示例代码如下：

```python
from ustb_openai import USTBOpenAI

client = USTBOpenAI()

with open("my_session.txt", "w") as f:
    f.write(client.easy_session)

with open("my_session.txt", "r") as f:
    my_session = f.read()

new_client = USTBOpenAI(easy_session=my_session)
```

#### 对话接口（Chat Completion API）

通过调用客户端对象的 `chat.completion.create()` 方法，您可以向服务器发送一个对话请求。该方法定义如下：

```python
def create(
    self,
    *,
    messages: Iterable[Mapping[str, str]],
    model: str,
    stream: Optional[bool] = None,
    **kwargs_ignored
) -> Union[ChatCompletion, Generator[ChatCompletion, Any, None]]:
    ...
```

其中，如果 `stream`（流式）参数为 `True`，那么该方法会返回一个生成器对象（生成 `ChatCompletion`），可以使用 `for` 语句进行迭代。每次迭代会返回一个 `ChatCompletion` 对象，并且在该对象的 `choices[0].delta.content` 字段中存储新获得的消息片段。

如果 `stream` 参数为 `False` 或缺省，那么该方法会直接返回一个 `ChatCompletion` 对象，并且在该对象的 `choices[0].message.content` 字段中存储完整的响应消息。

## 许可证 <sub>Licensing</sub>

本项目基于 **MIT 开源许可证**，详情参见 [License](https://github.com/isHarryh/USTB-OpenAI-Py/blob/main/LICENSE) 页面。
