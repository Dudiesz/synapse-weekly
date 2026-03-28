#!/usr/bin/env python
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Importamos a Crew e a ferramenta de PDF
from src.crew import SynapseWeeklyCrew
from src.tools.pdf_tool import PDFGenerator

# Carrega as chaves (.env deve conter GEMINI_API_KEY e SERPER_API_KEY)
load_dotenv()

def run():
    """
    Executa a Crew do Synapse Weekly e gera o output final em PDF.
    """
    # Define a data atual para o Scout e para o nome do ficheiro
    current_date = datetime.now().strftime("%d/%m/%Y")
    
    # Caminhos de output
    report_path = 'outputs/reports/jornal_da_semana.md'
    pdf_path = 'outputs/pdfs/jornal_da_semana.pdf'

    # Inputs para os agentes (Scout e Monitor Veterano)
    inputs = {
        'topic': 'Inteligência Artificial, Generative AI, Cloud Computing e Ferramentas para Devs',
        'current_date': current_date,
        'target_audience': 'Estudantes calouros e veteranos de tecnologia'
    }

    print(f"\n{'='*50}")
    print(f"--- INICIANDO SYNAPSE WEEKLY: {current_date} ---")
    print(f"{'='*50}\n")
    
    try:
        # 1. Execução da Crew (Pesquisa + Redação)
        print("[1/2] Agentes em ação (Pesquisando e Redigindo)...")
        SynapseWeeklyCrew().crew().kickoff(inputs=inputs)
        
        # 2. Geração do PDF
        print("\n[2/2] Transformando o jornal em PDF...")
        if os.path.exists(report_path):
            generator = PDFGenerator(report_path, pdf_path)
            generator.generate()
            print(f"\nSUCESSO: Jornal pronto em {pdf_path}")
        else:
            print(f"\nERRO: O ficheiro Markdown não foi encontrado em {report_path}")
        
        print(f"\n{'='*50}")
        print("--- PROCESSO CONCLUÍDO COM SUCESSO ---")
        print(f"{'='*50}")
        
    except Exception as e:
        print(f"\n[ERRO CRÍTICO]: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()