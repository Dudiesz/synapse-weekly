from src.tools.pdf_tool import PDFGenerator
import os

# Testa apenas a conversão do arquivo que já foi gerado
report_path = 'outputs/reports/jornal_da_semana.md'
pdf_path = 'outputs/pdfs/jornal_da_semana.pdf'

print("Testando conversão de PDF...")
generator = PDFGenerator(report_path, pdf_path)
generator.generate()