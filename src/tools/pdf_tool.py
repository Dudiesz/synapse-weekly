from fpdf import FPDF
import os
import re

class PDFGenerator:
    def __init__(self, input_markdown, output_pdf):
        self.input_markdown = input_markdown
        self.output_pdf = output_pdf

    def clean_markdown(self, text):
        """
        Remove a 'sujeira' do Markdown para deixar o PDF limpo.
        Transforma [Texto](URL) em 'Texto (Fonte: URL)' e remove asteriscos/hashes.
        """
        # 1. Converte links Markdown para formato legível em texto
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1 (Fonte: \2)', text)
        
        # 2. Remove negritos (**), itálicos (_), backticks (`) e símbolos de títulos (#)
        text = re.sub(r'\*\*|__|_|`|####|###|##|#', '', text)
        
        return text

    def generate(self):
        """Lê o Markdown, limpa o conteúdo e gera um PDF profissional."""
        if not os.path.exists(self.input_markdown):
            print(f"Erro: Arquivo fonte {self.input_markdown} não encontrado.")
            return

        # Tentativa de leitura com tratamento de encoding para evitar erros de 'byte 0xe7'
        content = []
        try:
            with open(self.input_markdown, "r", encoding="utf-8") as f:
                content = f.readlines()
        except UnicodeDecodeError:
            with open(self.input_markdown, "r", encoding="latin-1") as f:
                content = f.readlines()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        w = pdf.epw # Largura efetiva da página

        # --- CABEÇALHO ---
        pdf.set_font("helvetica", 'B', 24)
        pdf.set_text_color(0, 51, 102) # Azul escuro profissional
        pdf.cell(w, 20, "SYNAPSE WEEKLY", align='C', new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("helvetica", 'I', 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(w, 5, "Analise Tecnica Semanal para Estudantes de Tecnologia", align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)

        # --- PROCESSAMENTO DO CONTEÚDO ---
        for line in content:
            line = line.strip()
            if not line:
                pdf.ln(4)
                continue

            # Limpa o Markdown e trata caracteres especiais para Latin-1 (padrão FPDF)
            line = self.clean_markdown(line)
            try:
                line = line.encode('latin-1', 'replace').decode('latin-1')
            except Exception:
                line = line.replace('?', '') # Remove caracteres impossíveis de converter

            # Lógica de Estilização
            if "Edicao" in line or "/2026" in line:
                pdf.set_font("helvetica", 'B', 12)
                pdf.set_text_color(128, 128, 128)
                pdf.multi_cell(w, 8, line, align='C', new_x="LMARGIN", new_y="NEXT")
                pdf.ln(5)
            
            elif any(keyword in line.upper() for keyword in ["AVANCOS", "IMPACTO", "RISCOS", "ETICA", "DESTAQUES"]):
                # Títulos de Seção
                pdf.set_font("helvetica", 'B', 14)
                pdf.set_text_color(0, 51, 102)
                pdf.ln(2)
                pdf.multi_cell(w, 10, line.upper(), new_x="LMARGIN", new_y="NEXT")
                # Linha decorativa abaixo do título
                pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 40, pdf.get_y())
                pdf.ln(2)
            
            elif line.startswith(("1.", "2.", "3.", "4.", "5.")):
                # Títulos de Notícias
                pdf.set_font("helvetica", 'B', 12)
                pdf.set_text_color(0, 102, 204) # Azul mais claro
                pdf.multi_cell(w, 8, line, new_x="LMARGIN", new_y="NEXT")
            
            else:
                # Texto de Corpo
                pdf.set_font("helvetica", size=11)
                pdf.set_text_color(30, 30, 30)
                pdf.multi_cell(w, 7, line, new_x="LMARGIN", new_y="NEXT")

        # Cria a pasta de destino caso não exista
        os.makedirs(os.path.dirname(self.output_pdf), exist_ok=True)
        
        pdf.output(self.output_pdf)
        print(f"\n[SUCESSO] Jornal formatado gerado em: {self.output_pdf}")