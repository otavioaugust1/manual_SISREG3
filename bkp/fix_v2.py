#!/usr/bin/env python3
"""
Script v2 – Converte arquivos MediaWiki da pasta md/ para docs/
com sintaxe Markdown compatível com o tema Just the Docs do Jekyll.
"""

import os
import re
import html as html_module

MD_DIR = "/home/otavioaugust/Documentos/GitHub/manual_SISREG3/md"
DOCS_DIR = "/home/otavioaugust/Documentos/GitHub/manual_SISREG3/docs"
ROOT_DIR = "/home/otavioaugust/Documentos/GitHub/manual_SISREG3"

# Estrutura de navegação
NAV_CONFIG = {
    "01_ADMINISTRACAO": {
        "title": "Administração",
        "nav_order": 1,
        "description": "Perfis de administração estadual e municipal do SISREG.",
        "files": [
            ("Administrador_Estadual.md", 1),
            ("Administrador_Municipal.md", 2),
        ]
    },
    "02_CAPACITACAO": {
        "title": "Capacitação",
        "nav_order": 2,
        "description": "Informações sobre treinamentos e capacitações no SISREG.",
        "files": [
            ("ALVO_DO_CAPACITAÇÃO_DO_SISREG.md", 1),
            ("SISREG_CAPACITAÇÃO.md", 2),
        ]
    },
    "03_ERROS": {
        "title": "Erros e Soluções",
        "nav_order": 3,
        "description": "Resolução de erros comuns no SISREG.",
        "files": [
            ("CRIAR_ROTEIRO_ERRO_PASSO-A-PASSO.md", 1),
            ("Erros_de_Exportação_BPA.md", 2),
            ("SISREG_NÃO_ESTA_CARREGANDO_A_PAGINA_(ERRO_NO_COOKIES).md", 3),
        ]
    },
    "04_SISREG": {
        "title": "SISREG",
        "nav_order": 4,
        "description": "Definição, adesão, configuração e atualizações do SISREG.",
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
        "description": "Perfil e funcionalidades do Solicitante no SISREG.",
        "files": [
            ("Solicitante.md", 1),
            ("Estatísticas_de_Acesso.md", 2),
        ]
    },
    "99_OUTROS": {
        "title": "Outros",
        "nav_order": 9,
        "description": "Perfis adicionais, glossário e informações complementares.",
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


def img_path(filename):
    """Gera o path correto para uma imagem, com URL encoding de espaços."""
    # Remove quaisquer prefixos /images/ duplicados
    name = filename.strip()
    if name.startswith('/images/'):
        name = name[8:]
    elif name.startswith('images/'):
        name = name[7:]
    # URL-encodar espaços
    name = name.replace(' ', '%20')
    return f'/images/{name}'


def convert_wiki_table(table_text):
    """Converte tabela MediaWiki para tabela Markdown."""
    lines = table_text.strip().splitlines()
    headers = []
    rows = []
    current_row = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith('{|') or line == '|}':
            continue
        elif line.startswith('|-'):
            if current_row:
                rows.append(current_row[:])
                current_row = []
        elif line.startswith('!'):
            # Cabeçalho - pode ter múltiplos com !! separador
            cells = re.split(r'\s*!!\s*', line.lstrip('!').strip())
            headers.extend(c.strip() for c in cells)
        elif line.startswith('|'):
            # Célula de dados - pode ter múltiplas com || separador
            cells = re.split(r'\s*\|\|\s*', line.lstrip('|').strip())
            current_row.extend(c.strip() for c in cells)
        else:
            # Continuação de célula anterior
            if current_row:
                current_row[-1] = current_row[-1] + ' ' + line.strip()

    if current_row:
        rows.append(current_row[:])

    if not headers and not rows:
        return ''

    # Determinar número de colunas
    num_cols = max(len(headers), max((len(r) for r in rows), default=0))
    if num_cols == 0:
        return ''

    # Completar cabeçalhos se necessário
    while len(headers) < num_cols:
        headers.append(f'Coluna {len(headers)+1}')

    # Construir tabela Markdown
    result = []
    result.append('| ' + ' | '.join(h.replace('|', '\\|') for h in headers) + ' |')
    result.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')

    for row in rows:
        # Normalizar número de células
        while len(row) < len(headers):
            row.append('')
        row = row[:len(headers)]
        # Escapar pipes e remover quebras de linha internas
        cells = [c.replace('\n', ' ').replace('|', '\\|').strip() for c in row]
        result.append('| ' + ' | '.join(cells) + ' |')

    return '\n'.join(result)


def fix_wiki_tables(content):
    """Substitui todas as tabelas wiki no conteúdo."""
    def replace_table(m):
        converted = convert_wiki_table(m.group(0))
        return '\n\n' + converted + '\n\n' if converted else '\n\n'

    return re.sub(
        r'\{\|[\s\S]*?\|\}',
        replace_table,
        content
    )


def convert_body(content):
    """Converte o corpo do documento MediaWiki para Markdown."""

    # 1. Decodificar entidades HTML duplo-encoded (&amp;quot; → &quot; → ")
    content = html_module.unescape(html_module.unescape(content))

    # 2. Converter tabelas wiki ANTES de outros processamentos
    content = fix_wiki_tables(content)

    # 3. Remover imagens lixo do pandoc (RackMultipart...)
    content = re.sub(r'!\[[^\]]*\]\(RackMultipart[^)]+\)', '', content)

    # 4. Remover div tags (wiki e html)
    content = re.sub(r'</?div[^>]*>', '', content)

    # 5. Remover nowiki
    content = re.sub(r'<nowiki\s*/?>', '', content)

    # 6. ===heading=== → ### heading (antes de ==)
    content = re.sub(r'^===\s*(.+?)\s*===\s*$', r'### \1', content, flags=re.MULTILINE)
    # 7. ==heading== → ## heading
    content = re.sub(r'^==\s*(.+?)\s*==\s*$', r'## \1', content, flags=re.MULTILINE)

    # 8. Wiki bold '''text''' → **text**
    content = re.sub(r"'''(.+?)'''", r'**\1**', content)
    # 9. Wiki italic ''text'' → *text*
    content = re.sub(r"''(.+?)''", r'*\1*', content)

    # 10. [[arquivo:name.ext|...]] → remover (arquivo=namespace File, não existe)
    content = re.sub(r'\[\[arquivo:[^\]]*\]\]', '', content, flags=re.IGNORECASE)

    # 11. Imagens com caminho /images/ já definido e dimensão:
    # [[/images/name.ext|30px]] → <img src="/images/name.ext" width="30" />
    def img_with_path_and_size(m):
        path = m.group(1).strip()
        size = re.search(r'(\d+)px', m.group(2) or '')
        if size:
            return f'<img src="{path}" width="{size.group(1)}" />'
        else:
            name = os.path.basename(path)
            return f'![{name}]({path})'

    content = re.sub(
        r'\[\[(/images/[^\|\n]+)\|([^\]\n]+)\]\]',
        img_with_path_and_size,
        content
    )

    # 12. Imagens com caminho /images/ sem opções extras:
    # [[/images/name.ext]] → ![name](/images/name.ext)
    content = re.sub(
        r'\[\[(/images/([^\]\n]+))\]\]',
        lambda m: f'![{os.path.basename(m.group(2))}]({img_path(m.group(2))})',
        content
    )

    # 13. [[File:name.ext|NNpx|alt]] → <img src="/images/name.ext" width="NN" alt="alt" />
    def file_tag_full(m):
        fname = m.group(1).strip()
        opts = [x.strip() for x in m.group(2).split('|')]
        size = next((re.search(r'(\d+)px', o) for o in opts), None)
        alt_candidates = [o for o in opts if not re.match(r'\d+px$', o) and o.lower() not in ('frame', 'thumb', 'left', 'right', 'center', 'none')]
        alt = alt_candidates[0] if alt_candidates else fname
        path = img_path(fname)
        if size:
            return f'<img src="{path}" width="{size.group(1)}" alt="{alt}" />'
        else:
            return f'![{alt}]({path})'

    content = re.sub(
        r'\[\[File:([^\|\]\n]+)\|([^\]\n]+)\]\]',
        file_tag_full,
        content,
        flags=re.IGNORECASE
    )

    # 14. [[File:name.ext]] → ![name](/images/name.ext)
    content = re.sub(
        r'\[\[File:([^\]\n]+)\]\]',
        lambda m: f'![{m.group(1).strip()}]({img_path(m.group(1).strip())})',
        content,
        flags=re.IGNORECASE
    )

    # 15. Links externos: [[http://url|text]] → [text](url)
    content = re.sub(
        r'\[\[(https?://[^\|\]\n]+)\|([^\]\n]+)\]\]',
        lambda m: f'[{m.group(2).strip()}]({m.group(1).strip()})',
        content
    )

    # 16. Links externos sem texto: [[http://url]] → <url>
    content = re.sub(
        r'\[\[(https?://[^\]\n]+)\]\]',
        lambda m: f'<{m.group(1).strip()}>',
        content
    )

    # 17. Links internos com texto: [[:Categoria:X|text]], [[:Page|text]] → text
    content = re.sub(r'\[\[:?[^\|\]\n]+\|([^\]\n]+)\]\]', r'\1', content)

    # 18. Links internos sem texto: [[:Page]] → Page
    content = re.sub(r'\[\[:?([^\]\n]+)\]\]', r'\1', content)

    # 19. img tags com src sem path → adicionar /images/
    def fix_img_tag(m):
        src = m.group(1)
        rest = m.group(2)
        if not src.startswith('/') and not src.startswith('http'):
            src = '/images/' + src.replace(' ', '%20')
        return f'<img src="{src}"{rest}'

    content = re.sub(r'<img\s+src="([^"]+)"([^>]*>)', fix_img_tag, content)

    # 20. Markdown imagens com src local (sem /) → adicionar /images/
    def fix_md_img(m):
        alt = m.group(1)
        src = m.group(2).strip()
        if not src.startswith('/') and not src.startswith('http'):
            src_fixed = '/images/' + src.replace(' ', '%20')
            return f'![{alt}]({src_fixed})'
        return m.group(0)

    content = re.sub(
        r'!\[([^\]]*)\]\(([^/h][^\s)]*\.(?:png|jpg|gif|jpeg|webp))\)',
        fix_md_img,
        content,
        flags=re.IGNORECASE
    )

    # 21. Remover linhas vazias excessivas (mais de 2 seguidas)
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    return content


def build_frontmatter(original_fm, layout, nav_order, parent=None, has_children=False):
    """Reconstrói o frontmatter YAML com os valores corretos."""
    # Remover campos controlados do frontmatter original
    fm = original_fm
    for key in ('layout', 'nav_order', 'parent', 'has_children'):
        fm = re.sub(rf'^\s*{key}\s*:.*$\n?', '', fm, flags=re.MULTILINE)

    # Limpar linhas vazias extras
    fm = re.sub(r'\n{3,}', '\n\n', fm)
    fm = fm.strip()

    # Montar novos campos
    new_fields = [
        f'layout: {layout}',
        f'nav_order: {nav_order}',
    ]
    if parent:
        new_fields.append(f'parent: "{parent}"')
    if has_children:
        new_fields.append('has_children: true')

    if fm:
        return fm + '\n' + '\n'.join(new_fields) + '\n'
    else:
        return '\n'.join(new_fields) + '\n'


def process_file(src_path, dest_path, nav_order, parent_title):
    """Lê arquivo fonte (md/), converte e salva em dest (docs/)."""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Separar frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            original_fm = parts[1]
            body = parts[2]
        else:
            original_fm = parts[1] if len(parts) > 1 else ''
            body = ''
    else:
        original_fm = ''
        body = content

    # Construir frontmatter correto
    new_fm = build_frontmatter(original_fm, 'default', nav_order, parent_title)

    # Converter corpo
    new_body = convert_body(body)

    # Garantir que o diretório destino existe
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Escrever arquivo
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(f'---\n{new_fm}---\n{new_body}')

    print(f'  ✓ {os.path.basename(src_path)}')


def create_section_index(section_dir, title, nav_order, description):
    """Cria index.md para a seção."""
    content = (
        f'---\n'
        f'layout: default\n'
        f'title: "{title}"\n'
        f'nav_order: {nav_order}\n'
        f'has_children: true\n'
        f'permalink: /docs/{os.path.basename(section_dir)}/\n'
        f'---\n\n'
        f'# {title}\n\n'
        f'{description}\n'
    )
    index_path = os.path.join(section_dir, 'index.md')
    os.makedirs(section_dir, exist_ok=True)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  ✓ index.md → "{title}"')


def create_root_index():
    """Cria/substitui o index.md raiz."""
    content = (
        '---\n'
        'layout: default\n'
        'title: Início\n'
        'nav_order: 0\n'
        f'last_modified_date: "15/04/2025"\n'
        '---\n\n'
        '# Manual SISREG\n\n'
        'Bem-vindo ao manual online do **Sistema de Regulação – SISREG**.\n\n'
        'O SISREG é um sistema web desenvolvido pelo DATASUS/MS, disponibilizado '
        'gratuitamente para estados e municípios, destinado à gestão de todo o '
        'Complexo Regulador.\n\n'
        '<img src="{{ site.baseurl }}/images/Logo_sisreg.png" alt="Logo SISREG" '
        'style="max-width:200px;" />\n\n'
        '---\n\n'
        '*Elaboração, distribuição e informações*\n\n'
        '**MINISTÉRIO DA SAÚDE**  \n'
        'Secretaria de Atenção Especializada à Saúde - SAES  \n'
        'Departamento de Regulação Assistencial e Controle - DRAC\n\n'
        '---\n\n'
        '## Navegação\n\n'
        'Use o menu lateral para navegar pelas seções:\n\n'
        '- **Administração** — Administrador estadual e municipal\n'
        '- **Capacitação** — Treinamentos e capacitações\n'
        '- **Erros e Soluções** — Resolução de problemas comuns\n'
        '- **SISREG** — Definição, adesão, configuração e atualizações\n'
        '- **Solicitação** — Perfil solicitante\n'
        '- **Outros** — Demais perfis, glossário e referências\n'
    )
    with open(os.path.join(ROOT_DIR, 'index.md'), 'w', encoding='utf-8') as f:
        f.write(content)
    print('  ✓ index.md raiz')


def main():
    print('=== Conversão MediaWiki → Just the Docs (v2) ===\n')

    # 1. index.md raiz
    print('[1] Criando index.md raiz...')
    create_root_index()

    # 2. Processar seções
    print('\n[2] Processando seções e arquivos...')
    for section_dir_name, config in NAV_CONFIG.items():
        section_dest = os.path.join(DOCS_DIR, section_dir_name)
        print(f'\nSeção: {config["title"]}')

        create_section_index(section_dest, config['title'], config['nav_order'], config['description'])

        for filename, nav_order in config['files']:
            src = os.path.join(MD_DIR, filename)
            dest = os.path.join(section_dest, filename)
            if os.path.exists(src):
                process_file(src, dest, nav_order, config['title'])
            else:
                print(f'  ✗ NÃO ENCONTRADO em md/: {filename}')

    # 3. Verificar arquivos orphan em docs/
    print('\n[3] Verificando arquivos não mapeados em docs/...')
    mapped = set()
    for sd, cfg in NAV_CONFIG.items():
        for fn, _ in cfg['files']:
            mapped.add(os.path.join(DOCS_DIR, sd, fn))

    for root, dirs, files in os.walk(DOCS_DIR):
        for f in files:
            if f.endswith('.md') and f != 'index.md':
                fp = os.path.join(root, f)
                if fp not in mapped:
                    print(f'  ⚠ Não mapeado: {fp.replace(DOCS_DIR, "docs/")}')

    print('\n=== Concluído! ===')


if __name__ == '__main__':
    main()
