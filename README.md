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

O Guia Eletrônico do **Sistema de Regulação (SISREG III)** foi desenvolvido com o objetivo de qualificar e apoiar os profissionais de saúde das Centrais de Regulação que utilizam essa ferramenta para implementar ações de regulação no seu território.

O SISREG III é um software web desenvolvido pelo DATASUS/MS, disponibilizado gratuitamente para estados e municípios e destinado à gestão de todo o Complexo Regulador, desde a rede de atenção primária até a atenção especializada, visando regular o acesso aos serviços de saúde do SUS e potencializar a eficiência no uso dos recursos assistenciais.

Este repositório é a **reescrita e migração** do manual originalmente publicado no MediaWiki do Ministério da Saúde:

> 🔗 **Wiki original:** [wiki.saude.gov.br/SISREG](https://wiki.saude.gov.br/SISREG/index.php/P%C3%A1gina_principal)

O wiki foi criado e mantido por mim durante minha atuação na **Coordenação Geral de Regulação e Avaliação (CGRA/DRAC/SAES/MS)**. Com a evolução das ferramentas disponíveis, decidi migrar o conteúdo para uma plataforma mais moderna, acessível e com melhor experiência de leitura.

### Por que migrar?

- O MediaWiki institucional tem acesso restrito e manutenção limitada
- Jekyll + Just the Docs oferece publicação estática, busca integrada e navegação por perfil
- O conteúdo pode ser versionado, revisado e atualizado de forma transparente via Git

---

## Objetivos do SISREG

O SISREG tem como objetivo a sistematização de funções reguladoras, tais como:

- Permitir a distribuição dos recursos assistenciais disponíveis de forma regionalizada e hierarquizada;
- Facilitar o planejamento dos recursos assistenciais em uma região;
- Acompanhar, dinamicamente, a execução dos tetos pactuados entre os estabelecimentos de saúde;
- Permitir o referenciamento, em todos os níveis de atenção, nas redes pública e contratada;
- Identificar as áreas de desproporção entre a oferta e a demanda;
- Disponibilizar informações, em tempo real, sobre a oferta de leitos, consultas e exames especializados;
- Permitir o agendamento de internações e atendimentos eletivos para os pacientes;
- Controlar o fluxo dos pacientes nos estabelecimentos de saúde;
- Distribuir os limites (cotas) entre os estabelecimentos de saúde solicitantes, conforme pactuações.

---

## Módulos do SISREG

### Módulo Ambulatorial

Regula o acesso dos pacientes a consultas, exames especializados e SADT:

- Controla as agendas dos profissionais de saúde;
- Controla o fluxo dos pacientes — solicitação, agendamento e atendimento;
- Gera relatórios gerenciais;
- Controla os limites de solicitação e execução dos procedimentos especializados.

### Módulo Hospitalar

Regula os leitos hospitalares dos estabelecimentos de saúde vinculados ao SUS:

- Acompanha a alocação e disponibilidade de leitos em tempo real;
- Encaminha e autoriza internações de urgência;
- Agenda e autoriza internações eletivas;
- Controla o fluxo dos pacientes nos hospitais (admissão, internação e alta);
- Controla as emissões e autorizações das AIH.

---

## Perfis de Usuário

| Perfil | Atribuições principais |
|---|---|
| **Administrador Estadual** | Configura pactuações entre municípios, insere avisos e gerencia senhas de administradores |
| **Administrador Municipal** | Cadastra operadores, importa dados do CNES, configura procedimentos e cotas |
| **Coordenador de Unidade** | Gerencia escalas, fila de espera e fila de regulação da unidade |
| **Solicitante** | Solicita e acompanha procedimentos ambulatoriais e hospitalares |
| **Regulador/Autorizador** | Autoriza, nega ou devolve solicitações conforme protocolos clínicos |
| **Executante** | Confirma execução de procedimentos e gera BPA |
| **Executante Int** | Admite internações, realiza transferências, registra alta |
| **Auditor** | Verifica AIH autorizadas e realiza consultas de solicitações |
| **Videofonista** | Registra solicitações de unidades sem conectividade direta com o SISREG |

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

