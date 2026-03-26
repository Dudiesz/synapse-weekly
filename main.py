#!/usr/bin/env python
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from src.crew import SynapseWeeklyCrew

# Carrega as chaves do arquivo .env
load_dotenv()

def run():
    """
    Executa a Crew do Synapse Weekly.
    """
    # Crítica do Arquiteto: Nunca deixe a data "hardcoded". 
    # Precisamos que o Scout saiba EXATAMENTE que dia é hoje.
    current_date = datetime.now().strftime("%d/%m/%Y")
    
    inputs = {
        'topic': 'Inteligência Artificial, Generative AI, Cloud Computing (AWS/Azure/GCP) e Ferramentas para Desenvolvedores',
        'current_date': current_date,
        'target_audience': 'Estudantes calouros e veteranos de tecnologia'
    }

    print(f"--- Iniciando Synapse Weekly para a data: {current_date} ---")
    
    try:
        # Inicializa e executa
        SynapseWeeklyCrew().crew().kickoff(inputs=inputs)
        
        print("\n--- Processo concluído com sucesso! ---")
        print("O arquivo Markdown foi gerado em: outputs/reports/jornal_da_semana.md")
        
    except Exception as e:
        print(f"Erro crítico na execução da Crew: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()