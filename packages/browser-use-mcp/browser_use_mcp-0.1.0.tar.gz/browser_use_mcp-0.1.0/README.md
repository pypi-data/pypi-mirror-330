# ブラウザMCPサーバー

MCPの仕様に準じ、LLMからのブラウザ操作命令に従うMCPサーバー。

## 前提
ローカル環境(PC)にChromeブラウザがインストールされていること。

## サーバーのインストール手順
pythonパッケージ管理ソフトであるuvをPCにインストール（入っていない場合）
```bash
 curl -LsSf https://astral.sh/uv/install.sh | sh
```

python環境構築
```bash
 uv venv
 uv python install 3.11.7
 uv python pin 3.11.7
 source .venv/bin/activate
```

必要なpythonモジュールのインストール
```bash
 uv add -r requirements.txt
 uv sync
```

## 起動確認
```bash
 uv run main.py
 または
 mcp dev main.py # MCP Inspectorによる確認
```
これで正常に起動できていれば環境構築は成功してる。

## MCPクライアント側の設定
(Claude等のMCPクライアント側の設定)
```json
{
  "browser_use_mcp": {
    "command": "path/to/your/uv",
    "args": [
      "--directory",
      "/path/to/your/browser_use_mcp/",
      "run",
      "main.py"
    ],
    "env": {
      "OPENAI_API_KEY": "your OPENAI_API_KEY",
      "OPENAI_MODEL_NAME": "your OPENAI_MODEL_NAME"
    }
  }
}
```

```json
{
  "browser_use_mcp": {
    "command": "/Users/takeshi.fujita/.local/bin/uv",
    "args": [
      "--directory",
      "/Users/takeshi.fujita/browser_use_mcp/",
      "run",
      "main.py"
    ],
    "env": {
      "OPENAI_API_KEY": "#######",
      "OPENAI_MODEL_NAME": "#######"
    }
  }
}
```
本MCPがClaude等のMCPクライアントから正常に使えるかどうかの確認は、クライアントソフトごとに異なる。

