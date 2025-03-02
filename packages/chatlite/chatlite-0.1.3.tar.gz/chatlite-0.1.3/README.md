# ChatLite 🤖

A lightweight, extensible chat application framework for building AI-powered chat interfaces. ChatLite provides an easy-to-use platform for integrating various language models with web-based chat applications.

## ✨ Features

- 🔄 Real-time WebSocket communication
- 🎯 Multi-model support (Llama, Qwen, etc.)
- 🌐 Web search integration
- 🎨 Customizable UI with modern design
- 🔌 Plugin architecture for easy extensions
- 💬 Chat history management
- 🎭 Multiple agent types support
- 📱 Responsive design

## 🚀 Quick Start

### Installation

```bash
pip install chatlite
```

### Basic Usage

```python
import chatlite

# Start a simple chat server with Llama 3.2
chatlite.local_llama3p2()

# Or use Qwen 2.5
chatlite.local_qwen2p5()

# Custom configuration
server = chatlite.create_server(
    model_type="local",
    model_name="llama3.2:latest",
    temperature=0.7,
    max_tokens=4000
)
server.run()
```

### Pre-configured Models

ChatLite comes with several pre-configured models:

```python
# Use different models directly
from chatlite import mistral_7b_v3, mixtral_8x7b, qwen_72b

# Start Mistral 7B server
mistral_7b_v3()

# Start Mixtral 8x7B server
mixtral_8x7b()

# Start Qwen 72B server
qwen_72b()
```

## 💻 Frontend Integration

ChatLite includes a Flutter-based frontend that can be easily customized. Here's a basic example of connecting to the ChatLite server:

```dart
final channel = WebSocketChannel.connect(
  Uri.parse('ws://localhost:8143/ws/$clientId'),
);

// Send message
channel.sink.add(json.encode({
  'message': 'Hello!',
  'model': 'llama3.2:latest',
  'system_prompt': 'You are a helpful assistant',
  'agent_type': 'WebSearchAgent',
  'is_websearch_chat': true
}));

// Listen for responses
channel.stream.listen(
  (message) {
    final data = jsonDecode(message);
    if (data['type'] == 'stream') {
      print(data['message']);
    }
  },
  onError: (error) => print('Error: $error'),
  onDone: () => print('Connection closed'),
);
```

## 🔧 Configuration

ChatLite supports various configuration options:

```python
from chatlite import create_server

server = create_server(
    model_type="local",          # local, huggingface, etc.
    model_name="llama3.2:latest",
    api_key="your-api-key",      # if needed
    temperature=0.7,             # model temperature
    max_tokens=4000,             # max response length
    base_url="http://localhost:11434/v1",  # model API endpoint
)
```

## 🧩 Available Agents

ChatLite supports different agent types for specialized tasks:

- `WebSearchAgent`: Internet-enabled chat with web search capabilities
- `RawWebSearchAgent`: Direct web search results without summarization
- `EmailAssistantFeature`: Email composition and analysis
- `DefaultChatFeature`: Standard chat functionality

Example usage:

```python
# Client-side configuration
message_data = {
    "message": "What's the latest news about AI?",
    "model": "llama3.2:latest",
    "agent_type": "WebSearchAgent",
    "is_websearch_chat": True
}
```

## 🎨 UI Customization

The included Flutter frontend supports extensive customization:

```dart
ThemeData(
  brightness: Brightness.dark,
  scaffoldBackgroundColor: const Color(0xFF1C1C1E),
  primaryColor: const Color(0xFF1C1C1E),
  colorScheme: const ColorScheme.dark(
    primary: Color(0xFFFF7762),
    secondary: Color(0xFFFF7762),
  ),
)
```

## 📦 Project Structure

```
chatlite/
├── __init__.py          # Main package initialization
├── core/               # Core functionality
│   ├── config.py       # Configuration handling
│   ├── model_service.py # Model interaction
│   └── features/       # Feature implementations
├── ui/                 # Flutter frontend
└── examples/           # Usage examples
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with FastAPI and Flutter
- Inspired by modern chat applications
- Uses various open-source language models

## ⚠️ Disclaimer

This is an open-source project and should be used responsibly. Please ensure compliance with all model licenses and usage terms.