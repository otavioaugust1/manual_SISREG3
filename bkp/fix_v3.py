#!/usr/bin/env python3
"""
Script v3 – Converte páginas MediaWiki do XML exportado para docs/
com sintaxe Markdown compatível com o tema Just the Docs do Jekyll.

Novidades em relação à v2:
  - Lê diretamente do XML (md/ não é mais necessário)
  - Corrige links inter-páginas → URLs Jekyll corretas
  - Corrige tabelas com atributos de célula (colspan, rowspan, etc.)
"""

import os
import re
import html as html_module
import xml.etree.ElementTree as ET

XML_FILE  = "/home/otavioaugust/Documentos/GitHub/manual_SISREG3/bkp/SISREG-20260415193614.xml"
DOCS_DIR  = "/home/otavioaugust/Documentos/GitHub/manual_SISREG3/docs"
ROOT_DIR  = "/home/otavioaugust/Documentos/GitHub/manual_SISREG3"

# ---------------------------------------------------------------------------
# Estrutura de navegação — organizada por PERFIL DE USUÁRIO
# Cada arquivo: (nome_do_arquivo.md, wiki_title, nav_order_na_secao)
# ---------------------------------------------------------------------------
NAV_CONFIG = {
    "01_ADMINISTRADOR": {
        "title": "Administrador",
        "nav_order": 1,
        "description": "Perfis de administração estadual e municipal do SISREG.",
        "files": [
            ("Administrador_Estadual.md",  "Administrador Estadual",  1),
            ("Administrador_Municipal.md", "Administrador Municipal", 2),
        ]
    },
    "02_REGULADOR_AUTORIZADOR": {
        "title": "Regulador/Autorizador",
        "nav_order": 2,
        "description": "Perfil regulador e autorizador no SISREG.",
        "files": [
            ("Regulador_Autorizador.md", "Regulador/Autorizador", 1),
        ]
    },
    "03_COORDENADOR_DE_UNIDADE": {
        "title": "Coordenador de Unidade",
        "nav_order": 3,
        "description": "Perfil coordenador de unidade no SISREG.",
        "files": [
            ("Coordenador_de_Unidade.md", "Coordenador de Unidade", 1),
        ]
    },
    "04_SOLICITANTE": {
        "title": "Solicitante",
        "nav_order": 4,
        "description": "Perfil e funcionalidades do Solicitante no SISREG.",
        "files": [
            ("Solicitante.md",            "Solicitante",            1),
            ("Estatísticas_de_Acesso.md", "Estatísticas de Acesso", 2),
        ]
    },
    "05_EXECUTANTE": {
        "title": "Executante",
        "nav_order": 5,
        "description": "Perfil executante ambulatorial no SISREG.",
        "files": [
            ("Executante.md", "Executante", 1),
        ]
    },
    "06_EXECUTANTE_INT": {
        "title": "Executante Int",
        "nav_order": 6,
        "description": "Perfil executante internação (hospitalar) no SISREG.",
        "files": [
            ("Executante_Int.md", "Executante Int", 1),
        ]
    },
    "07_AUDITOR": {
        "title": "Auditor",
        "nav_order": 7,
        "description": "Perfil auditor no SISREG.",
        "files": [
            ("Auditor.md", "Auditor", 1),
        ]
    },
    "08_VIDEOFONISTA": {
        "title": "Videofonista",
        "nav_order": 8,
        "description": "Perfil videofonista no SISREG.",
        "files": [
            ("Videofonista.md", "Videofonista", 1),
        ]
    },
    "09_ERROS": {
        "title": "Erros e Soluções",
        "nav_order": 9,
        "description": "Resolução de erros e problemas comuns no SISREG.",
        "files": [
            ("CRIAR_ROTEIRO_ERRO_PASSO-A-PASSO.md",
             "CRIAR ROTEIRO ERRO PASSO-A-PASSO", 1),
            ("Erros_de_Exportação_BPA.md",
             "Erros de Exportação BPA", 2),
            ("SISREG_NÃO_ESTA_CARREGANDO_A_PAGINA_(ERRO_NO_COOKIES).md",
             "SISREG NÃO ESTA CARREGANDO A PAGINA (ERRO NO COOKIES)", 3),
            ("MENSAGEM_DE_CAPTCHA_(VOCÊ_É_UM_ROBÔ)_NO_SISREG.md",
             "MENSAGEM DE CAPTCHA (VOCÊ É UM ROBÔ) NO SISREG", 4),
            ("REAPROVEITAMENTO_DE_SENHA_NO_SISREG.md",
             "REAPROVEITAMENTO DE SENHA NO SISREG", 5),
            ("PASSO_A_PASSO_–_PRINT_DA_TELA_DO_COMPUTADOR_À_PARTIR_DO_TECLADO.md",
             "PASSO A PASSO – PRINT DA TELA DO COMPUTADOR À PARTIR DO TECLADO", 6),
        ]
    },
    "10_LGPD": {
        "title": "LGPD",
        "nav_order": 10,
        "description": "Lei Geral de Proteção de Dados aplicada ao SISREG.",
        "files": [
            ("Termo_de_uso_SISREG.md", "Termo de uso SISREG", 1),
        ],
        # páginas criadas manualmente (não vêm do XML)
        "extra_pages": [
            {
                "filename": "LGPD.md",
                "title": "LGPD – Lei Geral de Proteção de Dados",
                "nav_order": 2,
                "body": (
                    "A **Lei Geral de Proteção de Dados (LGPD)** – "
                    "Lei nº 13.709/2018 – estabelece regras sobre coleta, armazenamento, "
                    "tratamento e compartilhamento de dados pessoais, com o objetivo de "
                    "proteger os direitos fundamentais de liberdade e privacidade das "
                    "pessoas naturais.\n\n"
                    "## Aplicação no SISREG\n\n"
                    "O SISREG trata dados de saúde classificados como **dados pessoais "
                    "sensíveis** nos termos do art. 5º, inciso II, da LGPD. "
                    "Todos os operadores devem observar:\n\n"
                    "- **Finalidade** — dados utilizados exclusivamente para fins de regulação em saúde.\n"
                    "- **Necessidade** — coletar apenas os dados estritamente necessários.\n"
                    "- **Segurança** — medidas técnicas para proteger os dados de acessos não autorizados.\n"
                    "- **Responsabilização** — gestores e operadores respondem pelo uso correto dos dados.\n\n"
                    "## Bases Legais\n\n"
                    "| Base Legal | Descrição |\n"
                    "| --- | --- |\n"
                    "| Art. 7º, III | Cumprimento de obrigação legal pelo controlador |\n"
                    "| Art. 7º, VI | Exercício regular de direitos em processo administrativo |\n"
                    "| Art. 11, II, b | Tratamento de dados sensíveis para políticas públicas de saúde |\n\n"
                    "## Direitos do Titular\n\n"
                    "- Confirmação da existência de tratamento\n"
                    "- Acesso e correção dos dados\n"
                    "- Anonimização ou eliminação de dados desnecessários\n"
                    "- Portabilidade dos dados\n\n"
                    "## Contato\n\n"
                    "Para dúvidas sobre o tratamento de dados no âmbito do "
                    "Ministério da Saúde, acesse: "
                    "[www.gov.br/saude](https://www.gov.br/saude)\n"
                ),
            }
        ]
    },
    "99_OUTROS": {
        "title": "Outros",
        "nav_order": 11,
        "description": "Informações gerais, glossário, legislação e referências do SISREG.",
        "files": [
            ("Página_principal.md",                                       "Página principal",                                       1),
            ("SISREG_DEFINIÇÃO.md",                                        "SISREG DEFINIÇÃO",                                       2),
            ("SISREG_ADESÃO.md",                                           "SISREG ADESÃO",                                          3),
            ("ATUALIZAÇÃO_DO_SISREG.md",                                   "ATUALIZAÇÃO DO SISREG",                                  4),
            ("CENTRAIS_SISREG.md",                                         "CENTRAIS SISREG",                                        5),
            ("DADOS_PARA_A_CONFIGURAÇÃO_E_IMPLANTAÇÃO_DO_SISREG.md",       "DADOS PARA A CONFIGURAÇÃO E IMPLANTAÇÃO DO SISREG",      6),
            ("IMPORTAÇÃO_DE_NOVOS_PROCEDIMENTOS_NO_SISREG.md",             "IMPORTAÇÃO DE NOVOS PROCEDIMENTOS NO SISREG",            7),
            ("SOLICITAÇÃO_DE_ACESSO_AO_BI-SISREG.md",                      "SOLICITAÇÃO DE ACESSO AO BI-SISREG",                     8),
            ("SOLICITAÇÃO_DE_SENHA_PARA_O_SISREG.md",                      "SOLICITAÇÃO DE SENHA PARA O SISREG",                    9),
            ("SISREG_CAPACITAÇÃO.md",                                      "SISREG CAPACITAÇÃO",                                    10),
            ("ALVO_DO_CAPACITAÇÃO_DO_SISREG.md",                           "ALVO DO CAPACITAÇÃO DO SISREG",                         11),
            ("RELAÇÃO_DOS_INSCRITOS.md",                                   "RELAÇÃO DOS INSCRITOS",                                 12),
            ("GUIA_DE_PORTARIA,_DECRETO_E_LEI_PARA_CENTRAIS.md",           "GUIA DE PORTARIA, DECRETO E LEI PARA CENTRAIS",         13),
            ("Glossário.md",                                               "Glossário",                                             14),
            ("NOVIDADES.md",                                               "NOVIDADES",                                             15),
            ("CGRA.md",                                                    "CGRA",                                                  16),
            ("DRAC.md",                                                    "DRAC",                                                  17),
            ("SAS.md",                                                     "SAS",                                                   18),
            ("Ministerio_da_Saúde.md",                                     "Ministerio da Saúde",                                   19),
        ]
    }
}

# ---------------------------------------------------------------------------
# Mapeamento: título wiki (minúsculo) → URL Jekyll
# Construído automaticamente a partir do NAV_CONFIG
# ---------------------------------------------------------------------------
def build_wiki_url_map():
    """Cria dicionário: título_wiki.lower() → url_jekyll"""
    url_map = {}
    for section_dir, cfg in NAV_CONFIG.items():
        for filename, wiki_title, _ in cfg["files"]:
            # URL Jekyll: /docs/SECAO/NOME_DO_ARQUIVO_SEM_MD/
            stem = filename[:-3]  # remove .md
            url = f"/docs/{section_dir}/{stem}/"
            url_map[wiki_title.lower()] = url
    # Aliases adicionais (variações de título encontradas no wiki)
    extras = {
        "sisreg não está carregando a página (erros nos cookies)":
            "/docs/09_ERROS/SISREG_NÃO_ESTA_CARREGANDO_A_PAGINA_(ERRO_NO_COOKIES)/",
        "ministério da saúde": "/docs/99_OUTROS/Ministerio_da_Saúde/",
    }
    url_map.update(extras)
    return url_map

WIKI_URL_MAP = build_wiki_url_map()

# ---------------------------------------------------------------------------
# Carregamento do XML
# ---------------------------------------------------------------------------
def load_xml_pages(xml_path):
    """Retorna dicionário: título_wiki → texto_wikitext"""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    ns = {'mw': 'http://www.mediawiki.org/xml/export-0.10/'}
    pages = {}
    for page in root.findall('mw:page', ns):
        title = page.find('mw:title', ns).text
        rev   = page.find('mw:revision', ns)
        if rev is None:
            continue
        text_elem = rev.find('mw:text', ns)
        text = text_elem.text or '' if text_elem is not None else ''
        pages[title] = text
    return pages

# ---------------------------------------------------------------------------
# Utilitários de imagem
# ---------------------------------------------------------------------------
def img_path(filename):
    """Gera path /images/... com URL encoding de espaços."""
    name = filename.strip()
    for prefix in ('/images/', 'images/'):
        if name.startswith(prefix):
            name = name[len(prefix):]
    return '/images/' + name.replace(' ', '%20')

# ---------------------------------------------------------------------------
# Conversão de tabelas MediaWiki → Markdown
# ---------------------------------------------------------------------------
def _strip_cell_attrs(cell_text):
    """
    Remove atributos MediaWiki de uma célula.

    Exemplos:
      'colspan="2" |**AMBULATORIAL**'  →  '**AMBULATORIAL**'
      ' align="center" |texto'         →  'texto'
      'texto normal'                   →  'texto normal'
    """
    # Padrão: um ou mais pares attr="val" (ou attr=val) seguidos de |
    m = re.match(
        r'^\s*(?:(?:colspan|rowspan|style|class|align|valign|width|bgcolor|'
        r'height|id|scope|headers)\s*=\s*(?:"[^"]*"|\'[^\']*\'|\S+)\s*)+\|(.*)$',
        cell_text.strip(),
        re.IGNORECASE
    )
    if m:
        return m.group(1).strip()
    return cell_text.strip()


def convert_wiki_table(table_text):
    """Converte tabela MediaWiki para tabela Markdown."""
    lines = table_text.strip().splitlines()
    headers = []
    rows    = []
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
            # Cabeçalho – separa por !! ou |
            cell_raw = line.lstrip('!').strip()
            cells = re.split(r'\s*!!\s*|\s*\|\|\s*', cell_raw)
            for c in cells:
                headers.append(_strip_cell_attrs(c))
        elif line.startswith('|'):
            # Células de dados – separa por ||
            cell_raw = line.lstrip('|').strip()
            cells = re.split(r'\s*\|\|\s*', cell_raw)
            for c in cells:
                current_row.append(_strip_cell_attrs(c))
        else:
            # Continuação de célula anterior
            if current_row:
                current_row[-1] = current_row[-1] + ' ' + line.strip()
            elif headers:
                headers[-1] = headers[-1] + ' ' + line.strip()

    if current_row:
        rows.append(current_row[:])

    if not headers and not rows:
        return ''

    # Número de colunas
    num_cols = max(len(headers), max((len(r) for r in rows), default=0))
    if num_cols == 0:
        return ''

    # Completar cabeçalhos genéricos se necessário
    while len(headers) < num_cols:
        headers.append(f'Coluna {len(headers)+1}')

    # Construir tabela Markdown
    def esc(cell):
        return cell.replace('\n', ' ').replace('|', '\\|').strip()

    result = ['| ' + ' | '.join(esc(h) for h in headers) + ' |']
    result.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')

    for row in rows:
        while len(row) < len(headers):
            row.append('')
        row = row[:len(headers)]
        result.append('| ' + ' | '.join(esc(c) for c in row) + ' |')

    return '\n'.join(result)


def fix_wiki_tables(content):
    """Substitui todas as tabelas wiki no conteúdo."""
    def replace_table(m):
        converted = convert_wiki_table(m.group(0))
        return '\n\n' + converted + '\n\n' if converted else '\n\n'
    return re.sub(r'\{\|[\s\S]*?\|\}', replace_table, content)

# ---------------------------------------------------------------------------
# Resolução de links internos
# ---------------------------------------------------------------------------
def resolve_wiki_link(target, display_text=None):
    """
    Converte um link interno wiki para Markdown.

    target: o destino do link (ex: "Administrador Estadual",
            ":SISREG DEFINIÇÃO", "Administrador_Municipal#ANCHOR")
    display_text: texto exibido (pode ser None → usar target)
    """
    # Normalizar target
    raw = target.strip().lstrip(':')

    # Separar âncora
    anchor = ''
    if '#' in raw:
        raw, anchor_raw = raw.split('#', 1)
        anchor = '#' + anchor_raw.strip().replace(' ', '_')

    # Ignorar categorias (Categoria: / Category:)
    if re.match(r'^categor[íi]a\s*:', raw, re.IGNORECASE) or \
       re.match(r'^category\s*:', raw, re.IGNORECASE):
        text = display_text.strip() if display_text else raw.split(':', 1)[-1].strip()
        return text

    # Ignorar links especiais (Predefinição, Arquivo sem imagem conhecida, etc.)
    if re.match(r'^predefinição\s*:', raw, re.IGNORECASE):
        return display_text.strip() if display_text else ''

    # Troca underscores por espaços para lookup
    lookup = raw.replace('_', ' ').strip().lower()

    url = WIKI_URL_MAP.get(lookup)
    if url:
        url_with_anchor = url + anchor
        text = display_text.strip() if display_text else raw.replace('_', ' ').strip()
        # Remover negrito wiki do texto de link
        text = re.sub(r"'''(.+?)'''", r'\1', text)
        return f'[{text}]({url_with_anchor})'

    # Não encontrado no mapa → retorna só o texto
    return display_text.strip() if display_text else raw.replace('_', ' ').strip()

# ---------------------------------------------------------------------------
# Conversão principal do corpo MediaWiki → Markdown
# ---------------------------------------------------------------------------
def convert_body(content):
    """Converte wikitext para Markdown compatível com Just the Docs."""

    # 1. Decodificar entidades HTML
    content = html_module.unescape(html_module.unescape(content))

    # 2. Converter tabelas wiki ANTES de outros processamentos
    content = fix_wiki_tables(content)

    # 3. Remover imagens lixo do pandoc (RackMultipart...)
    content = re.sub(r'!\[[^\]]*\]\(RackMultipart[^)]+\)', '', content)

    # 4. Remover div e span tags
    content = re.sub(r'</?div[^>]*>', '', content)
    content = re.sub(r'</?span[^>]*>', '', content)

    # 5. Remover nowiki
    content = re.sub(r'<nowiki\s*/?>', '', content)

    # 6. Headings ===h=== → ### h  e  ==h== → ## h
    content = re.sub(r'^===\s*(.+?)\s*===\s*$', r'### \1', content, flags=re.MULTILINE)
    content = re.sub(r'^==\s*(.+?)\s*==\s*$',   r'## \1',  content, flags=re.MULTILINE)

    # 7. Bold / Italic
    content = re.sub(r"'''(.+?)'''", r'**\1**', content)
    content = re.sub(r"''(.+?)''",   r'*\1*',   content)

    # 8. [[Arquivo:name|opts]] e [[arquivo:name]] → imagem (igual a File:)
    def arquivo_tag(m):
        fname = m.group(1).strip()
        opts_str = m.group(2) or ''
        if opts_str:
            opts = [x.strip() for x in opts_str.split('|')]
            size = next((re.search(r'(\d+)px', o) for o in opts), None)
            alt_candidates = [o for o in opts if not re.match(r'\d+px$', o)
                              and o.lower() not in ('frame','thumb','left','right',
                                                    'center','none','frameless')]
            alt = alt_candidates[0] if alt_candidates else fname
            path = img_path(fname)
            if size:
                return f'<img src="{path}" width="{size.group(1)}" alt="{alt}" />'
            else:
                return f'![{alt}]({path})'
        else:
            return f'![{fname}]({img_path(fname)})'

    content = re.sub(
        r'\[\[(?:Arquivo|arquivo):([^\|\]\n]+)(?:\|([^\]\n]*))?\]\]',
        arquivo_tag, content)

    # 9. [[File:name|opts]] → imagem
    def file_tag(m):
        fname   = m.group(1).strip()
        opts_str = m.group(2) or ''
        if opts_str:
            opts = [x.strip() for x in opts_str.split('|')]
            size = next((re.search(r'(\d+)px', o) for o in opts), None)
            alt_candidates = [o for o in opts if not re.match(r'\d+px$', o)
                              and o.lower() not in ('frame','thumb','left','right',
                                                    'center','none','frameless')]
            alt = alt_candidates[0] if alt_candidates else fname
            path = img_path(fname)
            if size:
                return f'<img src="{path}" width="{size.group(1)}" alt="{alt}" />'
            else:
                return f'![{alt}]({path})'
        else:
            return f'![{fname}]({img_path(fname)})'

    content = re.sub(
        r'\[\[File:([^\|\]\n]+)(?:\|([^\]\n]*))?\]\]',
        file_tag, content, flags=re.IGNORECASE)

    # 10. Links externos com texto: [[http://url | text]] → [text](url)
    content = re.sub(
        r'\[\[(https?://[^\|\]\n]+)\s*\|\s*([^\]\n]+)\]\]',
        lambda m: f'[{m.group(2).strip()}]({m.group(1).strip()})',
        content
    )
    # 11. Links externos sem texto: [[http://url]] → <url>
    content = re.sub(
        r'\[\[(https?://[^\]\n]+)\]\]',
        lambda m: f'<{m.group(1).strip()}>',
        content
    )

    # 12. Links internos com texto: [[Target|Display]] ou [[:Target|Display]]
    def internal_link_with_text(m):
        return resolve_wiki_link(m.group(1), m.group(2))

    content = re.sub(
        r'\[\[:?([^\|\]\n#][^\|\]\n]*(?:#[^\|\]\n]*)?)?\|([^\]\n]+)\]\]',
        internal_link_with_text,
        content
    )

    # 13. Links internos sem texto: [[Target]] ou [[:Target]]
    def internal_link_no_text(m):
        return resolve_wiki_link(m.group(1))

    content = re.sub(
        r'\[\[:?([^\]\n]+)\]\]',
        internal_link_no_text,
        content
    )

    # 14. Imagens Markdown com src local (sem /) → adicionar /images/
    def fix_md_img(m):
        alt = m.group(1)
        src = m.group(2).strip()
        if not src.startswith('/') and not src.startswith('http'):
            src = '/images/' + src.replace(' ', '%20')
        return f'![{alt}]({src})'

    content = re.sub(
        r'!\[([^\]]*)\]\(([^/h][^\s)]*\.(?:png|jpg|gif|jpeg|webp))\)',
        fix_md_img, content, flags=re.IGNORECASE
    )

    # 15. <img src sem caminho absoluto → adicionar /images/
    def fix_img_tag(m):
        src  = m.group(1)
        rest = m.group(2)
        if not src.startswith('/') and not src.startswith('http'):
            src = '/images/' + src.replace(' ', '%20')
        return f'<img src="{src}"{rest}'

    content = re.sub(r'<img\s+src="([^"]+)"([^>]*>)', fix_img_tag, content)

    # 16. Remover linhas vazias excessivas
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    return content.strip()

# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------
def build_frontmatter(title, layout, nav_order, parent=None, has_children=False):
    fields = [
        f'title: "{title}"',
        f'layout: {layout}',
        f'nav_order: {nav_order}',
    ]
    if parent:
        fields.append(f'parent: "{parent}"')
    if has_children:
        fields.append('has_children: true')
    return '\n'.join(fields) + '\n'

# ---------------------------------------------------------------------------
# Processamento de um arquivo
# ---------------------------------------------------------------------------
def process_page(wiki_text, wiki_title, dest_path, nav_order, parent_title):
    """Converte wikitext e salva como Markdown em dest_path."""
    body = convert_body(wiki_text)
    fm   = build_frontmatter(wiki_title, 'default', nav_order, parent_title)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(f'---\n{fm}---\n\n{body}\n')
    print(f'  ✓ {os.path.basename(dest_path)}  ← "{wiki_title}"')

# ---------------------------------------------------------------------------
# Índices de seção e raiz
# ---------------------------------------------------------------------------
def create_section_index(section_dir, title, nav_order, description):
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
    content = (
        '---\n'
        'layout: default\n'
        'title: Início\n'
        'nav_order: 0\n'
        '---\n\n'
        '# Manual SISREG\n\n'
        'Bem-vindo ao manual online do **Sistema de Regulação – SISREG**.\n\n'
        'O SISREG é um sistema web desenvolvido pelo DATASUS/MS, disponibilizado '
        'gratuitamente para estados e municípios, destinado à gestão de todo o '
        'Complexo Regulador.\n\n'
        '---\n\n'
        '*Elaboração, distribuição e informações*\n\n'
        '**MINISTÉRIO DA SAÚDE**  \n'
        'Secretaria de Atenção Especializada à Saúde – SAES  \n'
        'Departamento de Regulação Assistencial e Controle – DRAC\n\n'
        '---\n\n'
        '## Perfis de Usuário\n\n'
        '- **[Administrador](/docs/01_ADMINISTRADOR/)** — Administrador estadual e municipal\n'
        '- **[Regulador/Autorizador](/docs/02_REGULADOR_AUTORIZADOR/)** — Regulação e autorização\n'
        '- **[Coordenador de Unidade](/docs/03_COORDENADOR_DE_UNIDADE/)** — Coordenação da unidade\n'
        '- **[Solicitante](/docs/04_SOLICITANTE/)** — Solicitações ambulatoriais e hospitalares\n'
        '- **[Executante](/docs/05_EXECUTANTE/)** — Atendimento ambulatorial\n'
        '- **[Executante Int](/docs/06_EXECUTANTE_INT/)** — Internação hospitalar\n'
        '- **[Auditor](/docs/07_AUDITOR/)** — Auditoria de AIH\n'
        '- **[Videofonista](/docs/08_VIDEOFONISTA/)** — Registro sem conectividade\n\n'
        '## Suporte\n\n'
        '- **[Erros e Soluções](/docs/09_ERROS/)** — Resolução de problemas comuns\n'
        '- **[LGPD](/docs/10_LGPD/)** — Lei Geral de Proteção de Dados\n'
        '- **[Outros](/docs/99_OUTROS/)** — Glossário, legislação e referências\n'
    )
    with open(os.path.join(ROOT_DIR, 'index.md'), 'w', encoding='utf-8') as f:
        f.write(content)
    print('  ✓ index.md raiz')


def create_custom_page(dest_path, title, nav_order, parent_title, body):
    """Cria uma página Markdown com conteúdo customizado (não vem do XML)."""
    fm = build_frontmatter(title, 'default', nav_order, parent_title)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(f'---\n{fm}---\n\n{body}\n')
    print(f'  ✓ {os.path.basename(dest_path)}  [gerado]')

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    import shutil
    print('=== Conversão MediaWiki XML → Just the Docs (v3) ===\n')

    # Carregar páginas do XML
    print(f'[0] Carregando XML: {XML_FILE}')
    xml_pages = load_xml_pages(XML_FILE)
    print(f'    {len(xml_pages)} páginas encontradas.\n')

    # Limpar pastas antigas que não fazem parte da nova estrutura
    print('[1] Limpando estrutura antiga em docs/...')
    new_sections = set(NAV_CONFIG.keys())
    if os.path.isdir(DOCS_DIR):
        for entry in os.listdir(DOCS_DIR):
            full = os.path.join(DOCS_DIR, entry)
            if os.path.isdir(full) and entry not in new_sections:
                shutil.rmtree(full)
                print(f'  ✗ removido: docs/{entry}/')

    # index.md raiz
    print('\n[2] Criando index.md raiz...')
    create_root_index()

    # Processar seções
    print('\n[3] Processando seções e arquivos...')
    missing = []
    for section_dir_name, cfg in NAV_CONFIG.items():
        section_dest = os.path.join(DOCS_DIR, section_dir_name)
        print(f'\nSeção: {cfg["title"]}')
        create_section_index(section_dest, cfg['title'], cfg['nav_order'], cfg['description'])

        # Remover arquivos órfãos na seção (não pertencem mais a ela)
        allowed = set(f for f, _, _ in cfg['files'])
        allowed.add('index.md')
        allowed.update(ep['filename'] for ep in cfg.get('extra_pages', []))
        if os.path.isdir(section_dest):
            for existing in os.listdir(section_dest):
                if existing.endswith('.md') and existing not in allowed:
                    os.remove(os.path.join(section_dest, existing))
                    print(f'  ✗ removido órfão: {existing}')

        # Páginas do XML
        for filename, wiki_title, nav_order in cfg['files']:
            dest = os.path.join(section_dest, filename)
            if wiki_title in xml_pages:
                process_page(
                    xml_pages[wiki_title],
                    wiki_title,
                    dest,
                    nav_order,
                    cfg['title']
                )
            else:
                print(f'  ✗ NÃO ENCONTRADO no XML: "{wiki_title}"')
                missing.append(wiki_title)

        # Páginas customizadas (não vêm do XML)
        for ep in cfg.get('extra_pages', []):
            dest = os.path.join(section_dest, ep['filename'])
            create_custom_page(
                dest,
                ep['title'],
                ep['nav_order'],
                cfg['title'],
                ep['body']
            )

    if missing:
        print(f'\n⚠ Páginas não encontradas no XML: {missing}')

    print('\n=== Concluído! ===')


if __name__ == '__main__':
    main()
