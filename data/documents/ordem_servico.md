# MANUAL DO USUÁRIO
## Ordens de Serviço — OS

### Sistema SUSE Beleza

---

## 1. Objetivo da tela de Ordens de Serviço

A tela **Ordens de Serviço (OS)** permite controlar os atendimentos realizados pela empresa, desde a abertura da ordem até sua execução e finalização.

Por meio dessa tela, o usuário pode:

- Criar uma nova Ordem de Serviço;
- Selecionar um cliente;
- Informar veículo;
- Definir prioridade;
- Associar um colaborador;
- Adicionar serviços;
- Adicionar produtos;
- Consultar as OS existentes;
- Pesquisar OS por número, cliente, placa ou modelo;
- Filtrar OS por status;
- Identificar pendências de aprovação, assinatura ou pagamento;
- Visualizar as OS em formato Kanban;
- Visualizar as OS em formato de lista;
- Abrir os detalhes de uma OS;
- Agendar um atendimento a partir da criação de uma OS.

---

# 2. Acessando a tela de Ordens de Serviço

Ao acessar a funcionalidade, será apresentada a tela:

**Ordens de Serviço**

No topo da tela existe o botão:

**Nova OS**

Esse botão permite iniciar o cadastro de uma nova Ordem de Serviço.

A tela também apresenta ferramentas para pesquisa, visualização e filtragem das ordens existentes.

---

# 3. Visões da tela

A tela possui duas formas principais de visualizar as Ordens de Serviço:

### Kanban

A visão **Kanban** organiza visualmente as OS de acordo com seu fluxo/status.

Essa visão é útil para acompanhar rapidamente em que etapa cada atendimento está.

### Lista

A visão **Lista** apresenta as Ordens de Serviço em formato de tabela/listagem.

Essa visualização é mais adequada quando o usuário deseja consultar várias OS e localizar rapidamente uma determinada ordem.

Para alternar entre as visões, utilize:

**Kanban | Lista**

---

# 4. Pesquisa de Ordens de Serviço

Na parte superior da tela existe o campo:

**Buscar por nº, cliente, placa...**

A pesquisa permite localizar uma OS utilizando informações como:

- Número da OS;
- Nome do cliente;
- Placa do veículo;
- Modelo do veículo.

### Exemplo

Para localizar uma OS do cliente **João da Silva**, basta digitar parte do nome:

`João`

O sistema exibirá as OS que correspondem ao termo pesquisado.

Também é possível pesquisar pela placa, por exemplo:

`ABC1234`

Ou pelo número da OS:

`OS-000123`

A pesquisa não diferencia letras maiúsculas de minúsculas.

---

# 5. Filtros por status

A tela possui filtros rápidos para alguns dos principais estados da Ordem de Serviço.

Estão disponíveis:

- **Aguardando aprovação**
- **Em execução**
- **Finalizado**

Ao clicar em um desses filtros, a tela passa a exibir somente as OS correspondentes ao status selecionado.

É possível selecionar mais de um status.

Por exemplo, o usuário pode selecionar:

- Aguardando aprovação
- Em execução

Nesse caso, serão exibidas as OS que estejam em qualquer um desses dois estados.

---

# 6. Filtro de pendências

O campo **Pendências** permite localizar OS que possuem alguma ação pendente.

As opções disponíveis são:

### Todas

Exibe as OS independentemente de pendências.

### Aprovação

Exibe OS que possuem pendência relacionada à aprovação do orçamento/serviço.

### Assinatura

Exibe OS que possuem pendência de assinatura.

### Pagamento

Exibe OS que possuem pendência de pagamento.

Esse recurso é útil para identificar rapidamente atendimentos que precisam de alguma ação antes de avançar no processo.

---

# 7. Criando uma nova OS

Para criar uma nova Ordem de Serviço, clique em:

**Nova OS**

Será aberta a tela:

**Nova OS (sem orçamento)**

O cadastro permite criar uma OS diretamente, sem a necessidade de criar previamente um orçamento.

---

# 8. Número da OS

O campo:

**Número (opcional)**

permite informar manualmente o número da OS.

Caso o campo seja deixado vazio, o sistema gera automaticamente um número para a Ordem de Serviço.

Portanto:

- Se desejar definir o número manualmente, preencha o campo;
- Caso contrário, deixe vazio e permita que o sistema gere o número automaticamente.

---

# 9. Selecionando o cliente

O campo:

**Cliente \***

é obrigatório.

O usuário deve selecionar um cliente cadastrado na base.

Ao abrir o campo, o sistema apresenta os clientes disponíveis.

O nome do cliente pode aparecer acompanhado do telefone.

### Após selecionar o cliente

O sistema busca os dados do cliente e preenche automaticamente o campo:

**Nome do cliente**

O nome também pode ser editado antes de salvar a OS.

> É necessário possuir um cliente selecionado para criar a Ordem de Serviço.

---

# 10. Prioridade da OS

O campo **Prioridade** permite definir a importância ou urgência do atendimento.

Existem quatro opções:

### Baixa

Utilizada para atendimentos sem urgência.

### Média

Prioridade padrão para atendimentos normais.

### Alta

Utilizada quando o atendimento precisa receber maior atenção.

### Crítica

Utilizada para situações que exigem tratamento prioritário.

A prioridade padrão apresentada na criação da OS é:

**Média**

---

# 11. Colaborador

O campo:

**Colaborador (opcional)**

permite associar a Ordem de Serviço a um colaborador.

Esse campo não é obrigatório durante a criação da OS.

O colaborador também pode ser associado posteriormente pelo fluxo da OS.

O sistema possui mecanismos para registrar o colaborador responsável na OS e também nas linhas de serviços e produtos quando aplicável.

---

# 12. Veículo

A estrutura da Ordem de Serviço possui informações para veículo, como:

- Placa;
- Modelo;
- Ano;
- Quilometragem.

Entretanto, na versão da tela fornecida, os campos de **Placa** e **Modelo** estão temporariamente desabilitados/comentados no formulário de criação.

Portanto, embora o modelo de dados da OS suporte essas informações, elas não estão disponíveis para preenchimento diretamente nessa tela na versão apresentada.

---

# 13. Adicionando serviços

A seção:

**Serviços**

permite selecionar os serviços disponíveis no catálogo da empresa.

Para adicionar serviços:

1. Abra o campo **Serviços**;
2. Selecione um ou mais serviços;
3. O sistema exibirá o nome e o preço de cada serviço;
4. Os serviços selecionados serão adicionados ao resumo da OS.

É possível selecionar múltiplos serviços.

Cada serviço possui informações como:

- Serviço;
- Quantidade;
- Valor unitário;
- Valor total;
- Percentual de comissão;
- Valor da comissão.

Na criação direta da OS, a quantidade inicial de cada serviço selecionado é **1**.

---

# 14. Adicionando produtos

A seção:

**Produtos**

permite adicionar produtos disponíveis no catálogo/estoque.

Para adicionar produtos:

1. Abra o campo **Produtos**;
2. Selecione um ou mais produtos;
3. O sistema apresenta o nome e o preço;
4. Quando disponível, também apresenta a quantidade em estoque;
5. Os produtos selecionados aparecem no resumo da OS.

A quantidade inicial de cada produto selecionado é **1**.

O sistema registra informações como:

- Produto;
- Quantidade;
- Valor unitário;
- Valor total;
- Comissão.

Na versão atual da tela fornecida, o percentual de comissão dos produtos é inicializado como **0%**.

---

# 15. Resumo da OS

Depois que serviços ou produtos forem selecionados, a tela apresenta um resumo.

Para cada serviço ou produto é apresentado:

**Quantidade × Nome — Valor**

Exemplo:

`1x Corte — R$ 50,00`

Ao final aparece:

**Total itens**

Esse valor representa a soma dos serviços e produtos adicionados à OS.

---

# 16. Cálculo dos valores

Os valores da OS são armazenados internamente em **centavos**, evitando problemas de precisão financeira.

Para o usuário, entretanto, os valores são apresentados em reais:

**R$ 50,00**

O total é calculado considerando:

**Total dos serviços + Total dos produtos**

Na criação direta da OS:

- Desconto inicial: R$ 0,00;
- Acréscimo inicial: R$ 0,00;
- Total da OS = total dos itens.

O modelo também permite registrar posteriormente descontos, acréscimos e comissões.

---

# 17. Salvando a OS

Depois de preencher os dados obrigatórios, clique em:

**Salvar OS**

O sistema verifica se o formulário está válido.

O cliente é obrigatório e o nome do cliente precisa estar preenchido.

Durante o salvamento, o botão apresenta:

**Salvando...**

Após a criação, o sistema apresenta a mensagem:

**OS criada!**

A nova OS é então disponibilizada na tela de Ordens de Serviço.

---

# 18. Status inicial de uma nova OS

Uma OS criada diretamente pela tela **Nova OS (sem orçamento)** recebe inicialmente o status:

**AGUARDANDO_APROVACAO**

Na interface, esse status é apresentado como:

**Aguardando aprovação**

O fluxo da OS possui os seguintes status previstos:

| Status | Significado |
|---|---|
| ABERTA | OS aberta |
| ORCADA | OS possui orçamento |
| AGUARDANDO_APROVACAO | Aguardando aprovação |
| APROVADA | Atendimento aprovado |
| AGENDADO | Atendimento agendado |
| PAUSADO | Atendimento temporariamente pausado |
| EM_EXECUCAO | Atendimento em execução |
| REPROVADA | Atendimento/orçamento reprovado |
| CANCELADA | OS cancelada |
| FINALIZADO | Atendimento finalizado |

---

# 19. Fluxo da Ordem de Serviço

De maneira geral, uma Ordem de Serviço pode passar pelas seguintes etapas:

**Abertura → Orçamento → Aprovação → Agendamento → Execução → Finalização → Pagamento**

Nem todas as OS necessariamente passarão por todas as etapas.

Por exemplo, uma OS criada diretamente sem orçamento pode iniciar em:

**Aguardando aprovação**

Já uma OS criada a partir de um agendamento pode iniciar em:

**Agendado**

---

# 20. Aprovação

O sistema possui suporte ao processo de aprovação da OS.

São registrados eventos relacionados à aprovação, incluindo:

- Link enviado;
- Visualização;
- Aprovação total;
- Aprovação parcial;
- Reprovação;
- Solicitação de ajuste;
- Assinatura.

Esses eventos podem ser associados à Ordem de Serviço para manter o histórico do processo de aprovação.

---

# 21. Link de aprovação

O sistema possui suporte a links de aprovação.

Um link possui:

- Token;
- OS associada;
- Versão do orçamento;
- Data de criação;
- Data de expiração, quando definida;
- Status.

O status do link pode ser:

**ATIVO**

ou

**EXPIRADO**

Isso permite controlar o acesso do cliente ao processo de aprovação.

---

# 22. Pendências da OS

Uma Ordem de Serviço pode possuir três tipos principais de pendência:

### Aprovação

Indica que existe uma aprovação que precisa ser realizada.

### Assinatura

Indica que existe uma assinatura pendente.

### Pagamento

Indica que o pagamento ainda precisa ser realizado.

Essas pendências podem ser utilizadas pelos filtros da tela para localizar rapidamente as OS que necessitam de atenção.

---

# 23. Execução do atendimento

Durante o ciclo de vida da OS, o atendimento pode passar por estados como:

**EM_EXECUCAO**

e

**PAUSADO**

O sistema possui campos para registrar:

- Momento em que a execução foi iniciada;
- Momento em que foi pausada;
- Momento em que foi finalizada.

Essas informações permitem acompanhar o histórico temporal da execução.

---

# 24. Finalização

Quando a OS é marcada como:

**FINALIZADO**

o sistema executa processos relacionados ao encerramento do atendimento.

Entre os processos previstos estão:

- Registro do histórico do cliente;
- Geração/garantia do lançamento financeiro;
- Processamento das metas;
- Registro de informações relacionadas ao atendimento;
- Criação de acompanhamento pós-serviço no CRM.

O pagamento também pode ser processado posteriormente pelo fluxo financeiro.

---

# 25. Pagamento da OS

O sistema possui uma operação específica para pagamento da OS.

Ao processar o pagamento:

1. O sistema localiza ou cria o lançamento financeiro relacionado à OS;
2. O lançamento é marcado como pago;
3. A pendência de pagamento é removida;
4. A OS é atualizada;
5. O status passa para **FINALIZADO**.

O lançamento financeiro recebe uma referência associada à OS, permitindo relacionar o atendimento ao registro financeiro.

---

# 26. Histórico do cliente

Quando uma OS é finalizada, o sistema pode registrar informações no histórico do cliente.

Entre os dados registrados estão:

- Cliente;
- Data do atendimento;
- Profissional;
- Serviços realizados;
- Valor;
- Observações;
- Referência da OS;
- Número da OS.

Isso permite manter o histórico dos atendimentos realizados para cada cliente.

---

# 27. Pós-serviço

Após a finalização da OS, o sistema também possui integração com o CRM para criação de um acompanhamento pós-serviço.

Na implementação apresentada, é criado automaticamente um follow-up de pós-serviço com:

**Canal: WhatsApp**

e previsão de:

**2 horas após o serviço**

Esse acompanhamento pode ser utilizado para ações de relacionamento com o cliente.

---

# 28. Agendando um atendimento a partir da OS

Na tela de criação da OS existe o botão:

**Agendar na agenda**

Esse recurso permite iniciar o processo de agendamento utilizando os dados informados na OS.

O sistema envia para o módulo de agenda informações como:

- Cliente;
- Nome do cliente;
- Modelo do veículo;
- Placa do veículo;
- Observações.

As observações incluem uma referência de que o agendamento foi iniciado a partir de uma OS.

---

# 29. Selecionando uma OS para atendimento

O sistema possui uma tela/modal de seleção de OS chamada:

**Selecionar OS**

Essa tela possui duas abas:

- **Fila**
- **Agenda**

### Fila

Permite consultar as OS disponíveis na fila.

### Agenda

Permite consultar as OS relacionadas aos atendimentos agendados para o dia.

---

# 30. Pesquisa na seleção de OS

Na tela **Selecionar OS**, existe o campo:

**Buscar**

A pesquisa pode ser realizada por:

- ID da OS;
- Placa;
- Nome do cliente.

Ao localizar a OS desejada, basta selecioná-la.

---

# 31. Check-in

A estrutura da OS possui informações resumidas sobre o check-in.

O check-in pode registrar:

- Se o check-in foi concluído;
- Se a assinatura do cliente foi realizada;
- Se a assinatura do atendente foi realizada;
- Se existem fotos;
- Quantidade de fotos;
- Quantidade de anexos.

Essas informações são utilizadas para verificar se os requisitos do atendimento foram cumpridos.

---

# 32. Prioridade operacional

A prioridade pode ser utilizada para organizar a fila de atendimento.

As prioridades disponíveis são:

| Prioridade | Uso |
|---|---|
| BAIXA | Atendimento com baixa urgência |
| MEDIA | Atendimento normal |
| ALTA | Atendimento prioritário |
| CRITICA | Atendimento de alta prioridade |

---

# 33. Informações principais de uma OS

Cada Ordem de Serviço possui informações de identificação e controle.

Entre elas:

- ID da OS;
- Número;
- Cliente;
- Veículo;
- Status;
- Prioridade;
- Colaborador;
- Serviços;
- Produtos;
- Totais;
- Versão do orçamento;
- SLA;
- Pendências;
- Check-in;
- Datas de criação e atualização;
- Orçamento relacionado.

---

# 34. Orçamento relacionado à OS

Uma OS pode possuir um orçamento associado.

Quando existe orçamento, o sistema pode sincronizar informações como:

- Serviços;
- Produtos;
- Quantidades;
- Valores;
- Descontos;
- Acréscimos;
- Total;
- Comissões.

O orçamento também possui uma versão.

A OS mantém a informação da:

**Versão do orçamento atual**

Isso permite identificar qual versão do orçamento está atualmente associada ao atendimento.

---

# 35. SLA

A OS possui suporte a SLA.

O SLA contém:

**Prazo previsto**

e pode indicar:

**Expirado**

Isso permite controlar se o prazo previsto para atendimento foi ultrapassado.

A tela fornecida não apresenta diretamente um controle de SLA, mas a informação faz parte da estrutura da OS.

---

# 36. Boas práticas para o usuário

Para manter as Ordens de Serviço organizadas:

1. Sempre selecione o cliente correto;
2. Confira o nome do cliente antes de salvar;
3. Defina uma prioridade adequada;
4. Adicione todos os serviços necessários;
5. Adicione os produtos utilizados quando aplicável;
6. Confira o total antes de salvar;
7. Utilize os status corretamente;
8. Acompanhe as pendências de aprovação, assinatura e pagamento;
9. Utilize a pesquisa para localizar rapidamente uma OS;
10. Mantenha o fluxo da OS atualizado durante o atendimento.

---

# 37. Exemplo de utilização

### Situação

Um cliente chega para realizar um serviço.

### Passo 1 — Criar OS

Clique em:

**Nova OS**

### Passo 2 — Cliente

Selecione o cliente cadastrado.

O sistema preencherá o nome automaticamente.

### Passo 3 — Prioridade

Selecione:

**Média**

### Passo 4 — Serviço

Selecione o serviço desejado.

Exemplo:

**Serviço de atendimento**

### Passo 5 — Produto

Caso seja necessário utilizar um produto, selecione-o na seção **Produtos**.

### Passo 6 — Conferência

Confira o resumo:

- Serviços;
- Produtos;
- Quantidades;
- Valores;
- Total.

### Passo 7 — Salvar

Clique em:

**Salvar OS**

A OS será criada com o status:

**Aguardando aprovação**

A partir desse momento, ela poderá ser acompanhada pela tela de Ordens de Serviço.

---

# 38. Resumo dos principais botões

| Botão/Controle | Função |
|---|---|
| Nova OS | Criar uma nova Ordem de Serviço |
| Kanban | Exibir OS em formato Kanban |
| Lista | Exibir OS em formato de lista |
| Buscar | Localizar uma OS |
| Aguardando aprovação | Filtrar OS nesse status |
| Em execução | Filtrar OS em execução |
| Finalizado | Filtrar OS finalizadas |
| Pendências | Filtrar por aprovação, assinatura ou pagamento |
| Agendar na agenda | Criar/iniciar um agendamento a partir da OS |
| Salvar OS | Criar a Ordem de Serviço |
| Cancelar | Cancelar o preenchimento da nova OS |
| Fechar | Fechar a tela/modal |

---

# 39. Fluxo resumido

```text
                 NOVA OS
                    │
                    ▼
              Selecionar cliente
                    │
                    ▼
             Definir prioridade
                    │
                    ▼
          Adicionar serviços/produtos
                    │
                    ▼
             Conferir valores
                    │
                    ▼
                SALVAR
                    │
                    ▼
        AGUARDANDO APROVAÇÃO
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
      APROVADA             REPROVADA
          │
          ▼
       AGENDADO
          │
          ▼
     EM EXECUÇÃO
          │
     ┌────┴────┐
     ▼         ▼
  PAUSADO   EXECUÇÃO
               │
               ▼
          FINALIZADO
               │
               ▼
            PAGAMENTO
               │
               ▼
         HISTÓRICO / CRM
```

---

# 40. Conclusão

A tela de **Ordens de Serviço** centraliza o controle dos atendimentos, permitindo acompanhar o processo desde a criação da OS até sua execução, finalização e pagamento.

O usuário deve utilizar principalmente:

- **Nova OS** para criar atendimentos;
- **Pesquisa** para localizar OS;
- **Kanban** para acompanhar o fluxo;
- **Lista** para consultar registros;
- **Filtros de status** para acompanhar etapas;
- **Filtro de pendências** para identificar ações necessárias;
- **Agendar na agenda** quando o atendimento precisar ser programado.

O sistema também mantém informações relacionadas a orçamento, aprovação, colaboradores, comissões, check-in, financeiro, histórico do cliente e CRM, formando um fluxo integrado para gerenciamento do atendimento.