# 🚨 Incident AI Agent

A production-grade multi-agent AI incident commander with RAG-ready architecture, observability tracing, SLA-aware diagnostics, and intelligent remediation workflows.

## Overview

This project implements an intelligent incident management system powered by **LangGraph** and **Ollama**. It automates incident investigation and resolution by orchestrating multiple specialized AI agents that work collaboratively to diagnose system failures and recommend fixes.

### Key Features

- **Multi-Agent Architecture**: Seven specialized agents handling different aspects of incident analysis
- **RAG-Ready**: Designed to integrate with retrieval-augmented generation for historical incident context
- **Observability Tracing**: Full trace logging for debugging agent workflows and decisions
- **SLA-Aware Diagnostics**: Evaluates impact on service level agreements
- **Intelligent Remediation**: Generates context-aware fix recommendations
- **Web UI**: Streamlit-based interface for incident analysis
- **Confidence Scoring**: Provides confidence metrics for recommendations
- **Human-in-the-Loop**: Flags incidents requiring human approval

## Architecture

### Agent Workflow

The system orchestrates 7 specialized agents in sequence:

1. **Log Collector Agent** - Aggregates and parses application logs
2. **Error Classification Agent** - Categorizes error types and patterns
3. **Severity Analyzer Agent** - Evaluates incident severity levels
4. **Similar Incident Retrieval Agent** - Retrieves historical incident context (RAG-ready)
5. **Root Cause Agent** - Determines root cause of failures
6. **Fix Recommendation Agent** - Generates remediation strategies
7. **Human Review Agent** - Flags high-risk incidents for approval

### Supported Services

The system includes incident analysis templates for:
- `payment-api`
- `order-api`
- `auth-service`
- `inventory-service`
- `deployment-service`

### State Management

Each incident investigation tracks:
- User query and service context
- Logs and error information
- Severity and error classification
- SLA impact assessment
- Circuit breaker status
- Root cause analysis
- Fix recommendations
- Confidence scoring and human review requirements
- Complete execution trace

## Installation

### Prerequisites

- Python 3.9+
- Ollama (for local LLM inference)
- pip

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/bogsanthosh/incident_ai_agent.git
cd incident_ai_agent
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
Create a `.env` file in the project root:
```env
OLLAMA_MODEL=mistral
OLLAMA_BASE_URL=http://localhost:11434
```

## Usage

### Running the Web UI

```bash
streamlit run ui.py
```

The application will open at `http://localhost:8501`

### Workflow

1. **Select Incident Scenario**: Choose from predefined services
2. **Ask Incident Question**: Describe the issue or use the auto-generated template
3. **Analyze**: Click "Analyze Incident" to trigger the multi-agent workflow
4. **Review Results**: 
   - View severity, error type, and confidence score
   - Read root cause analysis
   - Check fix recommendations
   - Review SLA impact and ownership
   - Track agent execution in real-time

## Project Structure

```
incident_ai_agent/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── ui.py                        # Streamlit web interface
├── app.py                       # Main application entry point
├── graph/
│   └── workflow.py              # LangGraph workflow definition
└── tools/                       # Agent tools and utilities
```

## Dependencies

- **langgraph**: Agent orchestration and state management
- **langchain**: LLM framework and tools
- **langchain-ollama**: Ollama integration
- **streamlit**: Web interface
- **python-dotenv**: Environment configuration

See `requirements.txt` for complete details.

## Configuration

### Environment Variables

```env
# Ollama Configuration
OLLAMA_MODEL=mistral              # Model to use
OLLAMA_BASE_URL=http://localhost:11434
```

### Customization

- **Add New Agents**: Extend the workflow in `graph/workflow.py`
- **Add Service Templates**: Update service selection in `ui.py`
- **Modify State Schema**: Adjust incident tracking fields in the initial state
- **Custom Tools**: Add new tools in the `tools/` directory

## API Response Format

The incident analysis returns:

```json
{
  "user_question": "Why is payment-api failing?",
  "service_name": "payment-api",
  "severity": "HIGH",
  "error_type": "Database Connection Error",
  "root_cause": "Connection pool exhaustion",
  "fix_recommendation": "Increase pool size and implement retry logic",
  "confidence_score": 0.92,
  "sla_impact": "Critical - Payment processing blocked",
  "circuit_breaker_status": "OPEN",
  "recommended_owner": "Backend Platform Team",
  "requires_human": false,
  "trace": [...],
  "logs": [...]
}
```

## Development

### Running Tests

```bash
# Add test suite as project grows
```

### Local Development with Ollama

Ensure Ollama is running:
```bash
ollama serve
```

Pull a model:
```bash
ollama pull mistral
```

## Best Practices

1. **Log Management**: Ensure application logs are accessible and properly formatted
2. **SLA Configuration**: Configure service SLAs for accurate impact assessment
3. **Model Selection**: Start with `mistral` or `neural-chat` for balanced performance
4. **Rate Limiting**: Implement rate limiting for production deployments
5. **Monitoring**: Track agent execution times and confidence scores

## Performance Considerations

- **Inference Time**: Depends on Ollama model and hardware
- **Token Limits**: Monitor context window usage for large logs
- **Concurrent Incidents**: Scale Ollama instances for parallel processing
- **Memory**: Allocate sufficient memory for LLM inference

## Troubleshooting

### Ollama Connection Issues
```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# Check Ollama logs
ollama logs
```

### Model Not Found
```bash
# Pull the required model
ollama pull mistral
```

### Streamlit Errors
```bash
# Clear Streamlit cache
streamlit cache clear

# Run with debug flag
streamlit run ui.py --logger.level=debug
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Roadmap

- [ ] Integration with real log aggregation systems
- [ ] Database RAG integration for incident history
- [ ] Multi-tenant support
- [ ] API endpoint for programmatic access
- [ ] Slack/PagerDuty integration
- [ ] Custom LLM fine-tuning on incident data
- [ ] Distributed agent execution
- [ ] Advanced visualization dashboards

---

**Built with**: LangGraph • Ollama • Streamlit • LangChain
