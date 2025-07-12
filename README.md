# WhatsApp MCP Bot

A production-ready WhatsApp bot integrated with a Model Context Protocol (MCP) server for cryptocurrency portfolio management and real-time market data.

Project Video:
https://youtu.be/Tmi_fNZ_ex0

### 👨‍💻 Author

---

**Lucas Miyazawa**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/lucasmiyazawa/) [![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:lucasmiyazawa@icloud.com)




## 🚀 Features

- **WhatsApp Integration**: Seamless communication through Evolution API
- **Portfolio Management**: Track cryptocurrency transactions and holdings
- **Real-time Market Data**: Get current prices, Fear & Greed Index, Bitcoin dominance, and fiat exchange rates
- **MCP Server**: Modular architecture with separate market data service
- **Production Ready**: Dockerized with proper logging, error handling, and health checks
- **AI-Powered**: Uses OpenAI GPT-4o for intelligent responses and insights
- **Observability**: Integrated with Logfire for comprehensive monitoring, tracing, and logging of AI agent and API interactions.

## 📋 Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🏗️ Architecture

The system consists of two main components:

### 1. MCP Server (`mcp-server/`)
A Gradio-based server that provides market data tools through the Model Context Protocol:
- **Cryptocurrency Prices**: Real-time price data from CoinGecko API
- **Fear & Greed Index**: Market sentiment indicator
- **Bitcoin Dominance**: BTC market cap percentage
- **Fiat Exchange Rates**: Currency conversion rates

### 2. WhatsApp Bot (`whatsapp-bot/`)
A FastAPI-based bot that handles WhatsApp messages and portfolio management:
- **Message Processing**: Receives webhooks from Evolution API
- **AI Agent**: Uses Pydantic AI with OpenAI GPT-4o
- **Portfolio Database**: SQLite database for transaction storage
- **MCP Integration**: Connects to the MCP server for market data

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   WhatsApp      │    │   Evolution     │    │   WhatsApp      │
│   User          │◄──►│   API           │◄──►│   Bot           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                               ┌─────────────────┐
                                               │   AI Agent      │
                                               │   (GPT-4o)      │
                                               └─────────────────┘
                                                       │
                                                       ▼
                                               ┌─────────────────┐
                                               │   MCP Server    │
                                               │   (Market Data) │
                                               └─────────────────┘
```


## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)
- **Git** (for cloning the repository)

### Required Services

1. **Evolution API Instance**: A running Evolution API server for WhatsApp integration
2. **OpenAI API Key**: For AI-powered responses
3. **WhatsApp Business Account**: Connected to your Evolution API instance

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/whatsapp-mcp-bot.git
cd whatsapp-mcp-bot
```

### 2. Environment Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Evolution API Configuration
EVOLUTION_API_URL="http://host.docker.internal:8081"
EVOLUTION_INSTANCE_NAME=your_instance_name
EVOLUTION_API_KEY=your_evolution_api_key

# WhatsApp Configuration
ALLOWED_WHATSAPP_NUMBER=allows_whatsapp_number

# Optional: Logfire Configuration (for monitoring)
LOGFIRE_TOKEN=your_logfire_token_here
```

### 3. Build and Start Services

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4o | Yes | - |
| `EVOLUTION_API_URL` | Evolution API base URL | Yes | - |
| `EVOLUTION_INSTANCE_NAME` | Evolution API instance name | Yes | - |
| `EVOLUTION_API_KEY` | Evolution API authentication key | Yes | - |
| `ALLOWED_WHATSAPP_NUMBER` | Authorized WhatsApp number | Yes | - |
| `LOGFIRE_TOKEN` | Logfire monitoring token | No | - |
| `HOST` | Server host address | No | `0.0.0.0` |
| `PORT` | WhatsApp bot port | No | `8000` |
| `MCP_SERVER_HOST` | MCP server host | No | `0.0.0.0` |
| `MCP_SERVER_PORT` | MCP server port | No | `7860` |
| `DATABASE_FILE` | SQLite database file path | No | `portfolio.db` |
| `DEBUG` | Enable debug mode | No | `false` |

### Evolution API Setup

1. **Install Evolution API**: Follow the [Evolution API documentation](https://doc.evolution-api.com/) to set up your instance
2. **Create Instance**: Create a new WhatsApp instance in Evolution API
3. **Configure Webhook**: Set the webhook URL to `http://your-server:8000/webhook/messages-upsert`
4. **Get Credentials**: Note down your instance name and API key

### WhatsApp Number Authorization

The bot only responds to messages from the number specified in `ALLOWED_WHATSAPP_NUMBER`. This is a security feature to prevent unauthorized access.

## 🎯 Usage

### Starting a Conversation

Send any message to your WhatsApp bot to begin. The AI will respond intelligently based on your queries.

### Portfolio Management Commands

#### Register a Transaction
```
Buy 0.5 bitcoin at $45000 on Binance
```
or
```
Sell 100 ethereum at $3000 on Coinbase
```

#### Query Portfolio
```
Show my portfolio
```
or
```
What's my bitcoin holdings?
```

### Market Data Queries

#### Get Cryptocurrency Prices
```
What's the current price of bitcoin and ethereum?
```

#### Check Market Sentiment
```
What's the current fear and greed index?
```

#### Bitcoin Dominance
```
What's bitcoin's market dominance?
```

#### Exchange Rates
```
What's the USD to EUR exchange rate?
```

### Example Conversations

**User**: "Buy 0.1 bitcoin at $42000 on Kraken"

**Bot**: "✅ Transaction registered successfully!
📝 ID: 1
🪙 Buy: 0.1 BTC
💰 Price: $42,000.00
🏪 Exchange: Kraken"

**User**: "Show my portfolio value"

**Bot**: "📊 Complete transaction history:

1. BUY: 0.1 bitcoin
   💰 Price: $42,000.00
   🏪 Exchange: Kraken
   📅 Date: 2025-01-15 10:30:00

💼 Current Holdings:
• BTC: 0.100000 (avg: $42,000.00)

📈 Current bitcoin price: $45,230.50
💰 Portfolio value: $4,523.05
📊 Unrealized P&L: +$323.05 (+7.69%)"

## 📚 API Documentation

### WhatsApp Bot Endpoints

#### Health Check
```http
GET /health
```

Response:
```json
{
  "status": "healthy",
  "database": "connected",
  "mcp_server": "http://mcp-server:7860/gradio_api/mcp/sse",
  "evolution_api": "http://host.docker.internal:8081"
}
```

#### Webhook Endpoint
```http
POST /webhook/messages-upsert
```

This endpoint receives webhooks from Evolution API when new messages arrive.

### MCP Server Interface

The MCP server provides a web interface at `http://localhost:7860` where you can:
- Test market data tools directly
- View API responses
- Monitor server status

#### Available Tools

1. **get_crypto_prices(coin_ids: str)**
   - Get current cryptocurrency prices
   - Example: `bitcoin,ethereum,solana`

2. **get_fear_and_greed_index()**
   - Get current market sentiment index

3. **get_bitcoin_dominance()**
   - Get Bitcoin's market cap dominance percentage

4. **get_fiat_exchange_rates(base_currency: str)**
   - Get exchange rates for fiat currencies
   - Example: `USD`, `EUR`, `GBP`

## 🔧 Development

### Local Development Setup

1. **Clone and Setup**:
```bash
git clone https://github.com/yourusername/whatsapp-mcp-bot.git
cd whatsapp-mcp-bot
```

2. **Create Virtual Environment**:
```bash
# For MCP Server
cd mcp-server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# For WhatsApp Bot
cd ../whatsapp-bot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Run Services Locally**:
```bash
# Terminal 1 - MCP Server
cd mcp-server
python app.py

# Terminal 2 - WhatsApp Bot
cd whatsapp-bot
python main.py
```

### Project Structure

```
whatsapp-mcp-bot/
├── mcp-server/
│   ├── app.py              # Main Gradio application
│   ├── tools.py            # Market data tools
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Docker configuration
├── whatsapp-bot/
│   ├── main.py            # FastAPI application
│   ├── agent.py           # AI agent configuration
│   ├── tools.py           # Local tools (portfolio, WhatsApp)
│   ├── database.py        # Database operations
│   ├── config.py          # Configuration management
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile        # Docker configuration
├── docker-compose.yml    # Multi-service orchestration
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── .dockerignore        # Docker ignore rules
└── README.md           # This file
```

### Adding New Features

#### Adding New Market Data Tools

1. **Add tool function** in `mcp-server/tools.py`:
```python
async def get_new_market_data() -> Dict[str, Any]:
    """Your new market data tool."""
    # Implementation here
    pass
```

2. **Update Gradio interface** in `mcp-server/app.py`:
```python
with gr.TabItem("New Data"):
    # Add UI components
    pass
```

#### Adding New Bot Commands

1. **Add tool function** in `whatsapp-bot/tools.py`:
```python
def new_portfolio_command(param: str) -> str:
    """Your new portfolio command."""
    # Implementation here
    pass
```

2. **Register tool** in `whatsapp-bot/agent.py`:
```python
local_tools = [
    register_transaction,
    query_portfolio,
    send_whatsapp_message,
    new_portfolio_command  # Add your new tool
]
```

### Testing

#### Unit Tests
```bash
# Run tests for MCP server
cd mcp-server
python -m pytest tests/

# Run tests for WhatsApp bot
cd whatsapp-bot
python -m pytest tests/
```

#### Integration Tests
```bash
# Test the complete flow
docker-compose up -d
# Send test messages through WhatsApp
# Check logs: docker-compose logs -f
```

## 🚀 Deployment

### Production Deployment

#### 1. Server Requirements
- **CPU**: 2+ cores
- **RAM**: 4GB+ recommended
- **Storage**: 20GB+ for logs and database
- **Network**: Public IP with ports 8000 and 7860 accessible

#### 2. Security Considerations

**Environment Variables**:
- Store sensitive variables in a secure `.env` file
- Never commit `.env` files to version control
- Use strong, unique API keys

**Network Security**:
- Use HTTPS in production (add reverse proxy like Nginx)
- Implement rate limiting
- Monitor for suspicious activity

**Database Security**:
- Regular backups of SQLite database
- Consider PostgreSQL for high-volume deployments


3. Monitoring and Logging

**Health Monitoring**:
```bash
# Check service health
curl http://localhost:8000/
curl http://localhost:7860/

# Monitor logs
docker-compose logs -f --tail=100
```

**Log Management**:
- Logs are automatically rotated (max 10MB, 3 files)
- Monitor disk usage regularly
- Consider centralized logging (ELK stack, Grafana)

**Performance Monitoring**:
- Use Logfire for application monitoring 
- Monitor Docker container resources
- Set up alerts for service failures

### Cloud Deployment Options

#### AWS Deployment
1. **EC2 Instance**: Deploy on Ubuntu 22.04 LTS
2. **ECS**: Use AWS Elastic Container Service
3. **RDS**: Consider PostgreSQL for database

#### Google Cloud Platform
1. **Compute Engine**: VM-based deployment
2. **Cloud Run**: Serverless container deployment
3. **Cloud SQL**: Managed database service

#### DigitalOcean
1. **Droplets**: Simple VM deployment
2. **App Platform**: Platform-as-a-Service option
3. **Managed Databases**: PostgreSQL hosting

## 🔍 Troubleshooting

### Common Issues

#### 1. MCP Server Connection Failed
**Symptoms**: WhatsApp bot can't connect to MCP server
**Solutions**:
```bash
# Check if MCP server is running
docker-compose ps

# Check MCP server logs
docker-compose logs mcp-server

# Test MCP server directly
curl http://localhost:7860/

# Restart services
docker-compose restart
```

#### 2. WhatsApp Messages Not Received
**Symptoms**: Bot doesn't respond to WhatsApp messages
**Solutions**:
- Verify Evolution API webhook configuration
- Check `ALLOWED_WHATSAPP_NUMBER` setting
- Verify Evolution API is running and accessible
- Check WhatsApp bot logs for errors

#### 3. Database Errors
**Symptoms**: Portfolio commands fail
**Solutions**:
```bash
# Check database file permissions
docker-compose exec whatsapp-bot ls -la /app/data/

# Reset database
docker-compose down
docker volume rm whatsapp-mcp-bot_whatsapp-bot-data
docker-compose up -d

# Check database logs
docker-compose logs whatsapp-bot | grep -i database
```

#### 4. OpenAI API Errors
**Symptoms**: AI responses fail or are slow
**Solutions**:
- Verify `OPENAI_API_KEY` is correct
- Check OpenAI API quota and billing
- Monitor rate limits
- Check network connectivity

### Debug Mode

Enable debug mode for detailed logging:

```bash
# In .env file
DEBUG=true

# Restart services
docker-compose restart
```

### Log Analysis

```bash
# View all logs
docker-compose logs

# Filter by service
docker-compose logs whatsapp-bot
docker-compose logs mcp-server

# Follow logs in real-time
docker-compose logs -f

# Search for errors
docker-compose logs | grep -i error
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Code Standards

- **Python**: Follow PEP 8 style guidelines
- **Type Hints**: Use type hints for all functions
- **Documentation**: Add docstrings for all functions and classes
- **Testing**: Write tests for new features
- **Logging**: Use appropriate log levels

### Pull Request Guidelines

- Provide clear description of changes
- Include test results
- Update documentation if needed
- Ensure all checks pass
- Link related issues

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


