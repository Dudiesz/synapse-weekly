import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI #

@CrewBase
class SynapseWeeklyCrew():
    """Orquestrador do Synapse Weekly - Edição Gemini"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # No seu src/crew.py
        self.gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", # Troque o 1.5 por 2.0 ou 3-flash
            verbose=True,
            temperature=0.5,
            google_api_key=os.getenv("GEMINI_API_KEY")
)

    @agent
    def scout_tecnico(self) -> Agent:
        return Agent(
            config=self.agents_config['scout_tecnico'],
            tools=[SerperDevTool()],
            llm=self.gemini_llm,
            verbose=True,
            allow_delegation=False,
            memory=True,
            max_iter=10
        )

    @agent
    def monitor_veterano(self) -> Agent:
        return Agent(
            config=self.agents_config['monitor_veterano'],
            llm=self.gemini_llm,
            verbose=True,
            allow_delegation=True
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
            context=[self.tarefa_pesquisa()],
            output_file='outputs/reports/jornal_da_semana.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )