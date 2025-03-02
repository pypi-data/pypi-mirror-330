
# Roleplay

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/)

A utility for reading configurations from YAML files to run Langchain workflows.

## Features

- 🛠️ YAML-based configuration management
- ⛓️ Langchain integration
- 🌐 OpenAI model support
- 📦 Pydantic data validation

## Installation

```bash
pip install langchain-roleplay
```

## Quick Start

1. 创建配置文件 `test.role.ymal`：
```yaml
# 示例配置
name: 呆猫
prompt:
  - role: system
    content: |
      你是呆猫，尊称用户为老大。
      你需要适时且克制地在输出的语句中插入‘喵’。
      尽量输出口语化的语句。
  - role: placeholder
    content: '{history}'

memory:
  type: base

llm: deepseek
config:
  model: deepseek-chat
  max_tokens: 8192
  temperature: 0.65

as_tool:
  name: 询问呆猫
  parameters:
    - name: input
      type: str
      description: 输入
  description: 让呆猫回答你的问题

tools:
  - get_weather
```

2. 创建llm配置文件 `test.llm.yaml`
```yaml
name: deepseek
base_url: 'https://api.deepseek.com'
api_key: sk-xxx # 替换为你的API Key
```

3. 创建工具配置文件 `test.tool.yaml`：
```yaml
name: 'get_weather'
parameters:
  - name: 'location'
    type: 'str'
    description: 'The location to get weather'
description: 'Get weather of an location, the user shoud supply a location first'

script: './py/test.py' # 自行实现
```

4. 在Python中使用：
```python
from roleplay.core import load_llm, load_tool
from roleplay.memory import load_role

load_llm('test.llm.yaml')
load_tool('test.tool.yaml')
role = load_role('test.role.yaml')
result = role.run(input='你好')
print(result)
```

## 依赖项

- Python 3.8+
- langchain >= 0.3.17
- langgraph >= 0.2.70
- pydantic >= 2.10.6
- PyYAML >= 6.0.2
- langchain-openai >= 0.3.4

## 开发

```bash
git clone https://github.com/maye76/roleplay.git
cd roleplay
pip install -e .
```

## 贡献

欢迎提交Issue和PR！

## License

MIT © 2025 maye76