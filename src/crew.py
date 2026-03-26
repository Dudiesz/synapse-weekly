import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class SynapseWeeklyCrew():
    """Orquestrador do Synapse Weekly - Jornal de IA para Estudantes"""

    # Caminhos para os arquivos de configuração (Relativos à raiz ou ao arquivo)
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def scout_tecnico(self) -> Agent:
        """Agente responsável por minerar a web atrás de novidades reais."""
        return Agent(
            config=self.agents_config['scout_tecnico'],
            tools=[SerperDevTool()], # Motor de busca injetado
            verbose=True,
            allow_delegation=False,
            memory=True, # Permite que ele mantenha contexto entre buscas
            max_iter=10  # Limite para não gastar tokens infinitamente se não achar algo
        )

    @agent
    def monitor_veterano(self) -> Agent:
        """Agente responsável pela curadoria e tradução didática para os calouros."""
        return Agent(
            config=self.agents_config['monitor_veterano'],
            verbose=True,
            allow_delegation=True # O monitor pode pedir esclarecimentos ao scout se algo estiver confuso
        )

    @task
    def tarefa_pesquisa(self) -> Task:
        """Task de extração de dados brutos da última semana."""
        return Task(
            config=self.tasks_config['tarefa_pesquisa'],
            agent=self.scout_tecnico()
        )

    @task
    def tarefa_redacao_jornal(self) -> Task:
        """Task de síntese, tradução didática e formatação final."""
        return Task(
            config=self.tasks_config['tarefa_redacao_jornal'],
            agent=self.monitor_veterano(),
            context=[self.tarefa_pesquisa()], # Garante que ele use o output da pesquisa
            output_file='outputs/reports/jornal_da_semana.md' # Persistência do resultado
        )

    @crew
    def crew(self) -> Crew:
        """Define a assembleia dos agentes e a ordem de execução."""
        return Crew(
            agents=self.agents, # Coleta automaticamente os métodos decorados com @agent
            tasks=self.tasks,   # Coleta automaticamente os métodos decorados com @task
            process=Process.sequential, # Ordem lógica: Pesquisa -> Redação
            verbose=True
        )