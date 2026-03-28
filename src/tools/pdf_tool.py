from fpdf import FPDF
import os

class PDFGenerator:
    def __init__(self, input_markdown, output_pdf):
        self.input_markdown = input_markdown
        self.output_pdf = output_pdf

    def generate(self):
        """Lê o arquivo Markdown e gera um PDF formatado."""
        if not os.path.exists(self.input_markdown):
            print(f"Erro: Arquivo {self.input_markdown} não encontrado para conversão.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Título do Jornal
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 15, "Synapse Weekly - Edição de IA", ln=True, align='C')
        pdf.ln(5)

        with open(self.input_markdown, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    pdf.ln(2)
                    continue

                # Formatação simples baseada em Markdown
                if line.startswith("# "):
                    pdf.set_font("Arial", 'B', 16)
                    pdf.multi_cell(0, 10, line.replace("# ", ""))
                elif line.startswith("## "):
                    pdf.set_font("Arial", 'B', 14)
                    pdf.ln(2)
                    pdf.multi_cell(0, 10, line.replace("## ", ""))
                elif line.startswith("### "):
                    pdf.set_font("Arial", 'B', 12)
                    pdf.multi_cell(0, 8, line.replace("### ", ""))
                elif line.startswith("* ") or line.startswith("- "):
                    pdf.set_font("Arial", size=11)
                    pdf.multi_cell(0, 7, f"  {line}")
                else:
                    pdf.set_font("Arial", size=11)
                    pdf.multi_cell(0, 7, line)
        
        pdf.output(self.output_pdf)
        print(f"--- PDF Gerado com Sucesso: {self.output_pdf} ---")