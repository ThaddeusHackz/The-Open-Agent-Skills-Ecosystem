---
name: pdf-ocr-reader
description: "Leitura de PDF com Python usando pypdf + OCR com fallback automatico. Use quando pedir: ler pdf, extrair texto de pdf, OCR, digitalizar PDF, converter PDF para TXT, resumir PDF escaneado, processar documentos PDF em lote."
argument-hint: "pdf=<caminho do pdf> out_dir=<pasta opcional> ttl_hours=<horas para limpeza> lang=<idioma OCR ex: por+eng>"
user-invocable: true
disable-model-invocation: false
---

# PDF OCR Reader

## Objetivo
Padronizar a leitura de PDFs no workspace com Python:
1. Tenta extrair texto com pypdf.
2. Se o PDF estiver escaneado ou com pouco texto, aplica OCR.
3. Salva resultado em TXT numa pasta temporaria.
4. Remove arquivos temporarios antigos por TTL.

## Quando usar
- Pedido de leitura de PDF.
- Pedido de extracao de texto de PDF.
- PDF escaneado, imagem, ou sem camada de texto.
- Pipeline para gerar TXT para analise posterior.

## Regras de decisao
1. Se o texto extraido por pypdf for suficiente, manter esse resultado.
2. Se o texto for vazio ou muito curto, usar OCR pagina a pagina.
3. Se o usuario pedir OCR explicitamente, pular pypdf e ir direto para OCR.
4. Sempre salvar em TXT no diretorio temporario configurado.
5. Sempre rodar limpeza de arquivos antigos apos gerar novo TXT.

## Procedimento padrao
1. Executar [script principal](./scripts/pdf_to_txt.py).
2. Conferir caminho do TXT gerado no output.
3. Validar qualidade minima:
   - Arquivo TXT existe.
   - Conteudo nao esta vazio.
   - Se OCR foi usado, idioma OCR esta correto para o documento.
4. Prosseguir com resumo, analise ou indexacao usando o TXT gerado.

## Comandos exemplo
- Extracao normal:
  - python .github/skills/pdf-ocr-reader/scripts/pdf_to_txt.py --pdf "caminho/arquivo.pdf"
- Forcar OCR:
  - python .github/skills/pdf-ocr-reader/scripts/pdf_to_txt.py --pdf "caminho/arquivo.pdf" --force-ocr
- Ajustar retencao:
  - python .github/skills/pdf-ocr-reader/scripts/pdf_to_txt.py --pdf "caminho/arquivo.pdf" --ttl-hours 72

## Dependencias Python
- pypdf
- pytesseract
- pdf2image
- pillow

Observacao:
- OCR depende do binario Tesseract instalado no sistema.
- Em Windows, pode ser necessario apontar pytesseract.pytesseract.tesseract_cmd para o executavel.

## Criterios de conclusao
- TXT salvo com sucesso.
- Limpeza de temporarios executada.
- Metodo usado (pypdf ou OCR) reportado no output.
- Caminho final do TXT informado.
