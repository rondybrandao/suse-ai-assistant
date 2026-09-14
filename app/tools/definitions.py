ERP_TOOL_DEFINITIONS = [
    {
        "name": "count_cancelled_os",
        "description": (
            "Conta quantas ordens de serviço estão canceladas."
        ),
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "count_finalized_os",
        "description": (
            "Conta quantas ordens de serviço estão finalizadas."
        ),
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "count_waiting_approval_os",
        "description": (
            "Conta quantas ordens de serviço estão aguardando aprovação."
        ),
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
]

RAG_TOOL_DEFINITIONS = [
    {
        "name": "search_suse_documentation",
        "description": (
            "Busca informações na documentação do SUSE ERP. "
            "Use esta ferramenta quando a pergunta precisar "
            "de procedimentos, regras, conceitos ou explicações "
            "sobre o funcionamento do sistema."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": (
                        "Pergunta que deve ser pesquisada "
                        "na documentação do SUSE."
                    ),
                },
            },
            "required": ["question"],
        },
    },
]