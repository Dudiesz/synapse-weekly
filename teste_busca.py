import os
from dotenv import load_dotenv
from crewai_tools import SerperDevTool

load_dotenv()

try:
    search = SerperDevTool()
    # Tenta fazer uma busca simples
    resultado = search._run(search_query="Lançamento modelos IA março 2026")
    print("Sucesso! O motor de busca retornou dados.")
except Exception as e:
    print(f"Erro na configuração: {e}")