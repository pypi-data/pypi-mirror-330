# Browser Control MCP Server

The MCP Server to control the Chrome Browser using LLM

## System Requirements
- Chrome browser was installed in you PC.
- Python >= 3.11.7
- uv which is python packaging tool was installed

## Claude Setting

```json
{
  "mcpServers": {
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
}
```
