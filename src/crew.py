import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from langchain_groq import ChatGroq

@CrewBase
class SynapseWeeklyCrew():
    """Orquestrador do Synapse Weekly - Edição Estável Groq"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:
        # Configuramos o Llama 3.3 via Groq como o cérebro do sistema
        # Este modelo é rápido e lida bem com textos didáticos
        self.groq_llm = ChatGroq(
            temperature=0.5,
            model_name="llama-3.3-70b-versatile",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    @agent
    def scout_tecnico(self) -> Agent:
        return Agent(
            config=self.agents_config['scout_tecnico'],
            tools=[SerperDevTool()],
            llm=self.groq_llm,
            verbose=True,
            allow_delegation=False, # Impede loops de conversa indevidos
            memory=True,
            max_iter=3 # Protege sua cota de tokens (TPM)
        )

    @agent
    def monitor_veterano(self) -> Agent:
        return Agent(
            config=self.agents_config['monitor_veterano'],
            llm=self.groq_llm,
            verbose=True,
            allow_delegation=False # Impede o erro de 'Co-worker not found'
        )

    @task
    def tarefa_pesquisa(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_pesquisa'],
            agent=self.scout_tecnico()
        )

    @task
    def tarefa_redacao_jornal(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_redacao_jornal'],
            agent=self.monitor_veterano(),
            context=[self.tarefa_pesquisa()], # Passa os dados da busca para a redação
            output_file='outputs/reports/jornal_da_semana.md'
        )

    @crew
    def crew(self) -> Crew:
        """Cria a equipe Synapse Weekly"""
        return Crew(
            agents=self.agents, # Criado automaticamente pelos decoradores @agent
            tasks=self.tasks,   # Criado automaticamente pelos decoradores @task
            process=Process.sequential,
            verbose=True
        )