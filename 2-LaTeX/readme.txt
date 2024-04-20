Modelo LaTeX de dissertação/tese do PPGInf/UFPR
Autor: prof. Carlos A. Maziero (maziero@inf.ufpr.br)
http://wiki.inf.ufpr.br/maziero/doku.php?id=software:latex
https://gitlab.c3sl.ufpr.br/maziero/tese

Descrição:

Modelo LaTeX para dissertações, teses, qualificações, trabalhos finais de graduação
e outros documentos similares. Previamente configurado para o PPGInf/UFPR, mas pode
ser facilmente ajustado para outros programas, cursos e universidades.

Conteúdo:

  ppginf.cls		: classe com as principais características do modelo
  main.tex		: fonte principal, que inclui os demais
  packages.tex		: inclusão de packages úteis para a redação
  referencias.bib	: referências bibliográficas (BibTeX)
  0-iniciais/		: diretório com as páginas iniciais
      resumo.tex	: resumo e palavras-chave
      abstract.tex	: abstract and keywords
      agradece.tex	: agradecimentos
      dedica.tex	: dedicatória
      aprovacao.tex	: inclusão da folha de aprovação
      aprovacao.pdf	: folha de aprovação "fake"
      catalografica.tex	: inclusão da ficha catalográfica
      catalografica.pdf	: ficha catalográfica "fake"
      acronimos.tex	: lista de acrônimos (siglas)
      simbolos.tex	: lista de símbolos
      fundo-capa.jpg	: imagem de fundo da capa
  1-intro/		: diretório do capítulo 1 (Introdução)
      texto.tex		: texto do capítulo 1
      figuras/		: figuras do capítulo 1
  2-fundam/		: ... (idem)
  a1-exemplo/		: Anexo 1
  Makefile		: usado para construir o PDF ;-)

Para compilar, digite "make".

Pendências:

- incluir \interfootnotelinepenalty=1000 para inibir a quebra de footnotes
- automatizar a geração das lista de símbolos e abreviações
- automatizar geração da ficha catalográfica
- posicionar ficha catalográfica no verso da 2a capa
- opção de inglês ou português (capa e rosto sempre em português)
- criar capítulos com conteúdo básico de uma dissertação ou tese
- distribuir melhor os pacotes entre ppginf.cls e packages.tex
- analisar uso de \backmatter
- separar apêndices de anexos?
- unificar versões em português e inglês, como opção no main.tex
- diferenciar tabelas de quadros?

