---
title: "Erros de Exportação BPA"
layout: default
nav_order: 2
parent: "Erros e Soluções"
---

Caso haja erro na geração do BPA, o operador deve clicar em “Exibir Erros...” que abrirá a tela abaixo.

![GERANDO BPA 4.png](/images/GERANDO%20BPA%204.png)

**a)	Seq.:** é a linha em que o erro se encontra.

**b)	Cód. Escala:** apresenta a escala do profissional que está relacionada ao erro do BPA. 

**c)	CPF Prof. Exec.:** apresenta o CPF do profissional executante do procedimento.

**d)	Profissional Executante:** apresenta o nome do profissional executante.

**e)	Cód. Proc. Interno:** apresenta o código interno do grupo do procedimento. Quando o procedimento for isolado, o mesmo número aparecerá no Código Item

**f)	Desc. Proc. Interno:** apresenta a descrição do grupo do procedimento no SISREG.

**g)	Cód. Item:** apresenta o código interno do procedimento utilizado no SISREG.

**h)	Desc. Item:** apresenta a descrição do procedimento no SISREG.

**i)	Cód. Proc. Unificado:** apresenta o código da tabela SIGTAP do procedimento. 

**j)	Proc. Ambulatorial:** apresenta o resultado da associação em que SISREG faz com o código SIGTAP ao tipo de registro. Dessa forma, caso a central de regulação utilize uma escala com procedimento APAC, o sistema não irá gerar BPA e neste campo irá aparecer o código “ERRO”.

**k)	CNS Prof. Exec.:** apresenta o resultado da associação que o sistema faz com o CNS do profissional Executante e o CNES da unidade. Caso apresente erro neste campo, é necessário verificar o CNES da unidade e atualizá-lo no SISREG.

Após a correção dos erros apresentados, o operador pode realizar novamente a geração do BPA.
