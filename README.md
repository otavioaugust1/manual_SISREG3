# Manual SISREG

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Jekyll](https://img.shields.io/badge/jekyll-4.3+-red.svg)
![Just the Docs](https://img.shields.io/badge/just--the--docs-0.10+-blue.svg)
![Status](https://img.shields.io/badge/status-em%20atualização-yellow.svg)

> **Projeto pessoal — em atualização contínua.**

Manual online do **Sistema de Regulação – SISREG**, desenvolvido e mantido por [Otávio Santos](https://github.com/otavioaugust1).

Documentação construída com [Jekyll](https://jekyllrb.com/) e o tema [Just the Docs](https://just-the-docs.com/).

---

## Sobre este projeto

O **SISREG** é um sistema web desenvolvido pelo DATASUS/MS e disponibilizado gratuitamente para estados e municípios, destinado à gestão de todo o Complexo Regulador — contemplando os módulos ambulatorial e hospitalar.

Este repositório é a **reescrita e migração** do manual originalmente publicado no MediaWiki do Ministério da Saúde:

> 🔗 **Wiki original:** [wiki.saude.gov.br/SISREG](https://wiki.saude.gov.br/SISREG/index.php/P%C3%A1gina_principal)

O wiki foi criado e mantido por mim durante minha atuação na **Coordenação Geral de Regulação e Avaliação (CGRA/DRAC/SAES/MS)**. Com a evolução das ferramentas disponíveis, decidi migrar o conteúdo para uma plataforma mais moderna, acessível e com melhor experiência de leitura.

### Por que migrar?

- O MediaWiki institucional tem acesso restrito e manutenção limitada
- Jekyll + Just the Docs oferece publicação estática, busca integrada e navegação por perfil
- O conteúdo pode ser versionado, revisado e atualizado de forma transparente via Git

---

## Estrutura de navegação

O manual está organizado por **perfil de usuário**, refletindo como o SISREG é utilizado na prática:

| # | Seção | Conteúdo |
|---|---|---|
| 01 | **Administrador** | Estadual e Municipal |
| 02 | **Regulador/Autorizador** | Regulação e autorização |
| 03 | **Coordenador de Unidade** | Coordenação da unidade |
| 04 | **Solicitante** | Solicitações ambulatoriais e hospitalares |
| 05 | **Executante** | Atendimento ambulatorial |
| 06 | **Executante Int** | Internação hospitalar |
| 07 | **Auditor** | Auditoria de AIH |
| 08 | **Videofonista** | Registro sem conectividade |
| 09 | **Erros e Soluções** | Problemas comuns e suas correções |
| 10 | **LGPD** | Proteção de dados no SISREG |
| 99 | **Outros** | Glossário, legislação, capacitação e referências |

---

## Como executar localmente

### Pré-requisitos

- Ruby 3.x
- Bundler (`gem install bundler`)

### 1. Clonar o repositório

```bash
git clone https://github.com/otavioaugust1/manual_SISREG3.git
cd manual_SISREG3
```

### 2. Instalar dependências

```bash
sudo bundle install
```

### 3. Executar o servidor local

```bash
bundle exec jekyll serve
```

Acesse: **http://localhost:4000**

### 4. Fazer Build

```bash
jekyll build
```

Os arquivos serão gerados em `_site/`

---

## Licença

**MIT License** — Veja [LICENSE](LICENSE).

---

**Otávio Santos** — [@otavioaugust1](https://github.com/otavioaugust1)

