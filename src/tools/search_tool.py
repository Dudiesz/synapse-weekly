from crewai_tools import SerperDevTool
import os

def get_tech_search_tool():
    """
    Retorna a ferramenta de busca configurada.
    Exige a variável de ambiente SERPER_API_KEY.
    """
    if not os.getenv("SERPER_API_KEY"):
        raise ValueError("Atenção: Você esqueceu de configurar a SERPER_API_KEY no arquivo .env")
        
    # Instanciamos a ferramenta oficial do CrewAI para Serper
    return SerperDevTool()