#!/usr/bin/env python3
"""
Script para converter os arquivos .md da pasta md/ (formato MediaWiki original)
para docs/ com sintaxe Markdown compatível com o tema Just the Docs do Jekyll.

Conversões aplicadas:
1. Frontmatter: layout, nav_order, parent, has_children corretos
2. Imagens MediaWiki [[File:x.png|30px]] → <img src="/images/x.png" width="30" />
3. Links internos [[:Categoria:X|text]] → text
4. Links externos [[url|text]] → [text](url)
5. Formatação '''bold''', ''italic''
6. Headings ==h== → ## h, ===h=== → ### h
7. Tabelas wiki → tabelas Markdown
8. HTML entities → texto limpo
9. Remoção de lixo (imagens junk, divs, etc.)
"""

import os
import re
import html as html_module

DOCS_DIR = "/home/otavioaugust/Documentos/GitHub/manual_SISREG3/docs"
MD_DIR = "/home/otavioaugust/Documentos/GitHub/manual_SISREG3/md"
ROOT_DIR = "/home/otavioaugust/Documentos/GitHub/manual_SISREG3"

# Estrutura de navegação: pasta -> {title, nav_order, files: [(filename, nav_order)]}
NAV_CONFIG = {
    "01_ADMINISTRACAO": {
        "title": "Administração",
        "nav_order": 1,
        "description": "Perfis de administração do SISREG",
        "files": [
            ("Administrador_Estadual.md", 1),
            ("Administrador_Municipal.md", 2),
        ]
    },
    "02_CAPACITACAO": {
        "title": "Capacitação",
        "nav_order": 2,
        "description": "Informações sobre capacitação no SISREG",
        "files": [
            ("ALVO_DO_CAPACITAÇÃO_DO_SISREG.md", 1),
            ("SISREG_CAPACITAÇÃO.md", 2),
        ]
    },
    "03_ERROS": {
        "title": "Erros e Soluções",
        "nav_order": 3,
        "description": "Resolução de erros comuns no SISREG",
        "files": [
            ("CRIAR_ROTEIRO_ERRO_PASSO-A-PASSO.md", 1),
            ("Erros_de_Exportação_BPA.md", 2),
            ("SISREG_NÃO_ESTA_CARREGANDO_A_PAGINA_(ERRO_NO_COOKIES).md", 3),
        ]
    },
    "04_SISREG": {
        "title": "SISREG",
        "nav_order": 4,
        "description": "Informações gerais e configuração do SISREG",
        "files": [
            ("SISREG_DEFINIÇÃO.md", 1),
            ("SISREG_ADESÃO.md", 2),
            ("ATUALIZAÇÃO_DO_SISREG.md", 3),
            ("CENTRAIS_SISREG.md", 4),
            ("DADOS_PARA_A_CONFIGURAÇÃO_E_IMPLANTAÇÃO_DO_SISREG.md", 5),
            ("IMPORTAÇÃO_DE_NOVOS_PROCEDIMENTOS_NO_SISREG.md", 6),
            ("MENSAGEM_DE_CAPTCHA_(VOCÊ_É_UM_ROBÔ)_NO_SISREG.md", 7),
            ("REAPROVEITAMENTO_DE_SENHA_NO_SISREG.md", 8),
            ("SOLICITAÇÃO_DE_ACESSO_AO_BI-SISREG.md", 9),
            ("SOLICITAÇÃO_DE_SENHA_PARA_O_SISREG.md", 10),
            ("Termo_de_uso_SISREG.md", 11),
        ]
    },
    "05_SOLICITACAO": {
        "title": "Solicitação",
        "nav_order": 5,
        "description": "Perfil e funcionalidades do Solicitante",
        "files": [
            ("Solicitante.md", 1),
            ("Estatísticas_de_Acesso.md", 2),
        ]
    },
    "99_OUTROS": {
        "title": "Outros",
        "nav_order": 9,
        "description": "Perfis adicionais, glossário e informações complementares",
        "files": [
            ("Página_principal.md", 1),
            ("Auditor.md", 2),
            ("CGRA.md", 3),
            ("Coordenador_de_Unidade.md", 4),
            ("DRAC.md", 5),
            ("Executante.md", 6),
            ("Executante_Int.md", 7),
            ("Glossário.md", 8),
            ("GUIA_DE_PORTARIA,_DECRETO_E_LEI_PARA_CENTRAIS.md", 9),
            ("Ministerio_da_Saúde.md", 10),
            ("NOVIDADES.md", 11),
            ("PASSO_A_PASSO_–_PRINT_DA_TELA_DO_COMPUTADOR_À_PARTIR_DO_TECLADO.md", 12),
            ("Regulador_Autorizador.md", 13),
            ("RELAÇÃO_DOS_INSCRITOS.md", 14),
            ("SAS.md", 15),
            ("Videofonista.md", 16),
        ]
    }
}


def convert_wiki_table(table_text):
    """Converte uma tabela MediaWiki para Markdown."""
    lines = table_text.strip().splitlines()
    headers = []
    rows = []
    current_row = []
    in_header = False

    for line in lines:
        line = line.strip()
        if line.startswith('{|') or line.startswith('|}'):
            continue
        elif line == '|-':
            if current_row:
                rows.append(current_row)
                current_row = []
        elif line.startswith('!'):
            # Header cell
            cell = line.lstrip('!').strip()
            headers.append(cell)
        elif line.startswith('|'):
            # Data cell
            cell = line.lstrip('|').strip()
            current_row.append(cell)

    if current_row:
        rows.append(current_row)

    if not headers and not rows:
        return ''

    # Normalizar número de colunas
    num_cols = max(len(headers), max((len(r) for r in rows), default=0))
    if num_cols == 0:
        return ''

    # Se não tem headers, criar genéricos
    if not headers:
        headers = [f'Coluna {i+1}' for i in range(num_cols)]

    # Preencher com colunas ausentes
    while len(headers) < num_cols:
        headers.append('Observação')

    # Construir tabela Markdown
    md_lines = []
    header_row = '| ' + ' | '.join(headers) + ' |'
    sep_row = '| ' + ' | '.join(['---'] * len(headers)) + ' |'
    md_lines.append(header_row)
    md_lines.append(sep_row)

    for row in rows:
        # Preencher células ausentes
        while len(row) < len(headers):
            row.append('')
        # Truncar células extras
        row = row[:len(headers)]
        # Escapar pipes nas células
        row = [c.replace('|', '\\|') for c in row]
        md_lines.append('| ' + ' | '.join(row) + ' |')

    return '\n'.join(md_lines)


def fix_wiki_tables(content):
    """Encontra e converte todas as tabelas wiki no conteúdo."""
    # Padrão para encontrar tabelas wiki: {| ... |}
    def replace_table(m):
        return '\n' + convert_wiki_table(m.group(0)) + '\n'

    # Tabelas com atributos HTML-encoded (&quot;)
    content = re.sub(
        r'\{\|[^\n]*\n(?:(?!\|\})[\s\S])*?\|\}',
        replace_table,
        content
    )
    return content


def fix_image_path(filename):
    """
    Converte nome de arquivo de imagem (com underscores) para path correto.
    Arquivos no /images/ têm espaços, referências usam underscores.
    """
    # Substituir underscores por espaços e URL-encodar espaços
    name = filename.replace('_', ' ')
    # URL-encodar caracteres especiais
    name = name.replace(' ', '%20')
    return f'/images/{name}'


def fix_wiki_syntax(content):
    """Aplica todas as correções de sintaxe wiki ao conteúdo."""

    # 1. Decodificar entidades HTML (para arquivos exportados diretamente do wiki)
    content = html_module.unescape(content)

    # 2. Converter tabelas ANTES de processar outros padrões
    content = fix_wiki_tables(content)

    # 3. Remover tags div escapadas (pandoc-style: \<div...\>)
    content = re.sub(r'\\<div[^>]*\\>', '', content)
    content = re.sub(r'\\</div\\>', '', content)

    # 4. Remover tags div regulares (do wiki)
    content = re.sub(r'<div[^>]*>', '', content)
    content = re.sub(r'</div>', '', content)

    # 5. Remover nowiki escapado e regular
    content = re.sub(r'\\<nowiki/?\\>', '', content)
    content = re.sub(r'<nowiki/?>', '', content)

    # 6. Converter imagens wiki - padrão pandoc com link duplo:
    # [![](/images/X) Y.png](![](/images/X_Y.png) "wikilink")
    # O alvo da âncora é outra imagem markdown - converter para img simples
    content = re.sub(
        r'\[!\[\]\([^)]+\)[^\]]*\]\(!\[\]\(/images/([^)]+)\)\s*"wikilink"\)',
        lambda m: f'![](/images/{m.group(1)})',
        content
    )

    # 7. Imagens wiki com prefixo arquivo: (não existem no nosso sistema)
    # [frame](arquivo:logo.png "wikilink") → remover
    content = re.sub(r'\[frame\]\(arquivo:[^)]+\s*"wikilink"\)', '', content)

    # 8. [thumb\|...\|...](arquivo:image.png "wikilink") → remover
    content = re.sub(r'\[thumb[^\]]*\]\(arquivo:[^)]+\s*"wikilink"\)', '', content)

    # 9. Imagens wiki com dimensões e link target sendo imagem:
    # [left\|100px](![](/images/Logo.png) "wikilink")
    # [frame\|FONTE:...](![](/images/X.png) "wikilink")
    # [30px](![](/images/X.png) "wikilink")
    content = re.sub(
        r'\[[^\]]*\]\(!\[\]\(/images/([^)]+)\)\s*"wikilink"\)',
        lambda m: f'![](/images/{m.group(1)})',
        content
    )

    # 10. Links wiki internos com namespace: [text](:Categoria:X "wikilink")
    content = re.sub(r'\[([^\]]+)\]\(:[^)]+\s*"wikilink"\)', r'\1', content)

    # 11. Links wiki internos de páginas: [text](PageName "wikilink")
    # e também [text](Page#Anchor "wikilink")
    content = re.sub(r'\[([^\]]+)\]\([^:)]+(?:#[^)]+)?\s*"wikilink"\)', r'\1', content)

    # 12. Links wiki double-bracket com pipe: [[:Page|text]] → text
    content = re.sub(r'\[\[:?[^\]|]+\|([^\]]+)\]\]', r'\1', content)

    # 13. Links wiki double-bracket sem pipe: [[Page]] → Page
    content = re.sub(r'\[\[:?([^\]|]+)\]\]', r'\1', content)

    # 14. Links wiki externos: [[url | text]] → [text](url)
    content = re.sub(
        r'\[\[([^|\]]+)\s*\|\s*([^\]]+)\]\]',
        lambda m: f'[{m.group(2).strip()}]({m.group(1).strip()})',
        content
    )

    # 15. Wiki bold: '''text''' → **text**
    content = re.sub(r"'''(.+?)'''", r'**\1**', content)

    # 16. Wiki italic: ''text'' → *text*
    content = re.sub(r"''(.+?)''", r'*\1*', content)

    # 17. Wiki headings: ===heading=== → ### heading
    content = re.sub(r'^===\s*([^=]+?)\s*===\s*$', r'### \1', content, flags=re.MULTILINE)
    # ==heading== → ## heading
    content = re.sub(r'^==\s*([^=]+?)\s*==\s*$', r'## \1', content, flags=re.MULTILINE)

    # 18. Corrigir img tags com src sem path (arquivos locais sem /images/)
    # <img src="Task.png" ...> → <img src="/images/Task.png" ...>
    def fix_img_src(m):
        src = m.group(1)
        rest = m.group(2)
        # Se não começa com / ou http, adicionar /images/
        if not src.startswith('/') and not src.startswith('http'):
            # Substituir underscores por espaços e URL-encodar
            src_fixed = '/images/' + src.replace(' ', '%20')
            return f'<img src="{src_fixed}"{rest}'
        return m.group(0)

    content = re.sub(
        r'<img\s+src="([^"]+)"([^>]*>)',
        fix_img_src,
        content
    )

    # 19. Corrigir referências de imagem markdown sem path
    # ![](ADM_MENU.png "ADM_MENU.png") → ![ADM MENU](/images/ADM%20MENU.png)
    def fix_md_img(m):
        alt = m.group(1)
        src = m.group(2)
        # Se src não tem / e não começa com http
        if not src.startswith('/') and not src.startswith('http'):
            # Limpar underscores e criar path correto
            display = alt or src.replace('_', ' ').split('"')[0].strip()
            src_fixed = '/images/' + src.replace(' ', '%20').replace('"', '').strip()
            return f'![{display}]({src_fixed})'
        return m.group(0)

    content = re.sub(
        r'!\[([^\]]*)\]\(([^/h][^)]*\.(?:png|jpg|gif|jpeg|webp))[^)]*\)',
        fix_md_img,
        content,
        flags=re.IGNORECASE
    )

    # 20. Imagens com /images/ já corretas mas com underscore no nome
    # /images/MENU_SOLICITANTE_1.png → /images/MENU%20SOLICITANTE%201.png
    # Não fazer essa substituição pois pode quebrar coisas corretas

    # 21. Remover separadores wiki de bullet: · seguido de espaços
    # Manter como está pois é válido em Markdown

    # 22. Remover linhas vazias excessivas (mais de 2 seguidas)
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    # 23. Remover "..." como conteúdo único
    # Deixar como está

    return content


def update_frontmatter(frontmatter, layout, nav_order, parent=None, has_children=False):
    """Atualiza o frontmatter YAML com os valores corretos."""
    # Remover campos que vamos sobrescrever
    fm = re.sub(r'^\s*layout\s*:.*$', '', frontmatter, flags=re.MULTILINE)
    fm = re.sub(r'^\s*nav_order\s*:.*$', '', frontmatter, flags=re.MULTILINE)
    fm = re.sub(r'^\s*parent\s*:.*$', '', frontmatter, flags=re.MULTILINE)
    fm = re.sub(r'^\s*has_children\s*:.*$', '', frontmatter, flags=re.MULTILINE)

    # Remover linhas vazias extras
    fm = re.sub(r'\n{3,}', '\n', fm)
    fm = fm.strip()

    # Adicionar novos campos
    new_fields = f'\nlayout: {layout}\nnav_order: {nav_order}'
    if parent:
        new_fields += f'\nparent: "{parent}"'
    if has_children:
        new_fields += '\nhas_children: true'

    return fm + new_fields + '\n'


def process_file(filepath, nav_order, parent_title):
    """Processa um arquivo markdown individual."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Separar frontmatter do corpo
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
        else:
            frontmatter = parts[1] if len(parts) > 1 else ''
            body = ''
    else:
        frontmatter = ''
        body = content

    # Atualizar frontmatter
    frontmatter = update_frontmatter(frontmatter, 'default', nav_order, parent_title)

    # Corrigir sintaxe wiki no corpo
    body = fix_wiki_syntax(body)

    # Reconstruir arquivo
    new_content = f'---\n{frontmatter}---\n{body}'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f'  ✓ Corrigido: {os.path.basename(filepath)}')


def create_section_index(section_path, title, nav_order, description):
    """Cria o arquivo index.md para uma seção."""
    content = f"""---
layout: default
title: "{title}"
nav_order: {nav_order}
has_children: true
permalink: /docs/{os.path.basename(section_path)}/
---

# {title}

{description}
"""
    index_path = os.path.join(section_path, 'index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  ✓ Criado index: {title}')


def fix_root_index():
    """Corrige o index.md principal."""
    index_path = os.path.join(ROOT_DIR, 'index.md')
    content = """---
layout: default
title: Início
nav_order: 0
last_modified_date: "15/04/2025"
---

# Manual SISREG

Bem-vindo ao manual online do **Sistema de Regulação – SISREG**.

O SISREG é um sistema web desenvolvido pelo DATASUS/MS, disponibilizado gratuitamente para estados e municípios, destinado à gestão de todo o Complexo Regulador.

<img src="{{ site.baseurl }}/images/Logo_sisreg.png" alt="Logo SISREG" style="max-width:200px;" />

---

*Elaboração, distribuição e informações*

**MINISTÉRIO DA SAÚDE**  
Secretaria de Atenção Especializada à Saúde - SAES  
Departamento de Regulação Assistencial e Controle - DRAC

---

## Navegação

Use o menu lateral para navegar pelas seções do manual:

- **Administração** — Perfis de administrador estadual e municipal
- **Capacitação** — Informações sobre treinamentos e capacitações
- **Erros e Soluções** — Resolução de problemas comuns
- **SISREG** — Definição, adesão, configuração e atualizações
- **Solicitação** — Perfil e funcionalidades do solicitante
- **Outros** — Demais perfis, glossário e referências
"""
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('  ✓ index.md principal corrigido')


def main():
    print('=== Iniciando correção do projeto manual_SISREG3 para Just the Docs ===\n')

    # Corrigir index.md principal
    print('[1/3] Corrigindo index.md principal...')
    fix_root_index()

    # Processar cada seção
    print('\n[2/3] Criando índices de seção e corrigindo arquivos...')
    for section_dir, config in NAV_CONFIG.items():
        section_path = os.path.join(DOCS_DIR, section_dir)
        print(f'\nSeção: {config["title"]} ({section_dir})')

        # Criar index.md da seção
        create_section_index(
            section_path,
            config['title'],
            config['nav_order'],
            config['description']
        )

        # Processar arquivos filhos
        for filename, nav_order in config['files']:
            filepath = os.path.join(section_path, filename)
            if os.path.exists(filepath):
                process_file(filepath, nav_order, config['title'])
            else:
                print(f'  ✗ AVISO: Arquivo não encontrado: {filename}')

    # Verificar arquivos não mapeados
    print('\n[3/3] Verificando arquivos não mapeados...')
    mapped_files = set()
    for section_dir, config in NAV_CONFIG.items():
        for filename, _ in config['files']:
            mapped_files.add(os.path.join(DOCS_DIR, section_dir, filename))

    for root, dirs, files in os.walk(DOCS_DIR):
        for f in files:
            if f.endswith('.md') and f != 'index.md':
                fp = os.path.join(root, f)
                if fp not in mapped_files:
                    print(f'  ⚠ Não mapeado: {fp}')

    print('\n=== Correção concluída! ===')


if __name__ == '__main__':
    main()
