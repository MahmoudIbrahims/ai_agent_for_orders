## Project Structure

```plaintext
ai_agent_project/
├── app/                              # Main FastAPI application
│   ├── __init__.py
│   ├── main.py                       # Entry point of the FastAPI app
│   ├── models/                       # Models (part of MVC)
│   │   ├── __init__.py
│   │   ├── order_model.py
│   │   └── customer_model.py
│   ├── views/                        # Views (API endpoints, templates)
│   │   ├── __init__.py
│   │   ├── api_views.py
│   │   └── templates/                # Jinja2 HTML templates (if used)
│   ├── controllers/                  # Controllers (business logic)
│   │   ├── __init__.py
│   │   ├── order_controller.py
│   │   └── agent_controller.py
│   ├── services/                     # Service layer (LLMs, APIs, etc.)
│   │   ├── __init__.py
│   │   ├── google_sheets_service.py
│   │   ├── llm_service.py
│   │   └── crew_service.py
│   └── config/                       # Configuration settings
│       ├── __init__.py
│       └── settings.py
├── agents/                           # CrewAI Agents
│   ├── __init__.py
│   ├── customer_service_agent.py
│   ├── order_processing_agent.py
│   └── data_entry_agent.py
├── tools/                            # Custom tools
│   ├── __init__.py
│   ├── google_sheets_tool.py
│   └── validation_tool.py
├── .env                              # Environment variables
├── .env.example                      # Example .env for reference
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

## Create a new environment and activate :
```
sudo conda create -n ai_Agent python=3.10
conda activate ai_Agent
```

