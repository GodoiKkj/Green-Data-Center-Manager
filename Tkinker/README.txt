Descrição

Este software simula a gestão de um Data Center verde, focando no uso de energia renovável e energia regular para alimentar servidores. Ele gerencia a alocação de energia, o status dos servidores, e visualiza os dados através de gráficos interativos, com a finalidade de otimizar o uso de recursos energéticos.


Instruções de Execução

Execução do programa: Execute o script Python. A interface de login será exibida.
O login padrão é "administrador" e "admin" como senha.
Após o login bem-sucedido, o painel de controle (Dashboard) será carregado.

Painel de Controle: O painel de controle exibe o consumo de energia renovável e regular, o número de servidores ativos e inativos, e a carga de cada servidor.
Você pode visualizar gráficos em tempo real sobre a distribuição de energia e o status dos servidores.

Fechar o Programa: No painel de controle, um botão "Sair" permite encerrar a aplicação e interromper a execução das threads de atualização.


Dependências

Use o seguinte comando para instalar as dependências:

pip install matplotlib

pip install sortedcontainers


Justificativa para as Escolhas Técnicas:

Arquitetura e Modularidade
A escolha de modularizar o código em classes distintas (como EnergySource, Server, DataCenter, etc.) é essencial para manter a escalabilidade e facilitar a manutenção do sistema. Cada componente é responsável por uma parte específica da funcionalidade, o que permite atualizações ou modificações sem impactar outras áreas. Além disso, esse design orientado a objetos facilita a adição de novos tipos de servidores ou fontes de energia no futuro, sem a necessidade de grandes refatorações.

Interface Gráfica
A escolha do Tkinter para a interface gráfica é justificada pela sua simplicidade e por ser uma biblioteca padrão do Python, o que elimina a necessidade de dependências externas. Isso é útil para manter o sistema leve e facilmente distribuível. O uso do Matplotlib para gráficos interativos é apropriado, pois ele permite uma visualização eficaz do consumo de energia e distribuição de carga, além de ser amplamente utilizado e bem documentado.

Simulação de Backend com Threads
A utilização de threading é uma escolha eficiente para manter a fluidez do sistema, permitindo que a interface gráfica seja atualizada sem bloquear outras operações do backend. Isso é fundamental para a performance, especialmente em sistemas que precisam processar dados em tempo real, como no seu caso, onde a alocação de energia e status dos servidores precisa ser monitorada continuamente.

Alocação de Energia e Sustentabilidade
A implementação da alocação de energia, priorizando fontes renováveis, reflete uma preocupação com a sustentabilidade, o que é um objetivo crescente em muitos data centers modernos. Essa abordagem não só atende à demanda energética de forma eficiente, mas também reflete práticas ecologicamente responsáveis.

Uso de SortedList e SortedDict
A escolha do SortedList da biblioteca sortedcontainers é adequada para manter a lista de servidores ordenada dinamicamente, sem a necessidade de reordenação manual. Isso melhora a eficiência, especialmente em sistemas com grandes volumes de dados ou operações frequentes de inserção e remoção. A complexidade logarítmica das operações de inserção, remoção e busca garante que o sistema seja escalável e eficiente, mesmo com o aumento do número de servidores ou tarefas.

Além disso, o uso de SortedDict para operações baseadas em chave-valor ordenada contribui para a eficiência nas buscas e na manutenção da ordem dos dados. A escolha de encapsular essa estrutura em uma classe ajuda na clareza e modularidade do código, tornando a implementação mais flexível e extensível para novos requisitos ou funcionalidades.

Gerenciamento de Temperatura e Redistribuição de Carga
O gerenciamento da temperatura dos servidores e a redistribuição de carga são essenciais para evitar superaquecimento e garantir a eficiência energética. A lógica de resfriamento e redistribuição gradual (em "pedaços" de carga) reflete práticas comuns de gerenciamento térmico em data centers, promovendo a sustentabilidade e a performance.

Flexibilidade e Escalabilidade
A flexibilidade do sistema, garantida pela modularidade das classes e pelo uso de estruturas eficientes como SortedList e SortedDict, permite a fácil expansão do sistema à medida que novos tipos de servidores ou fontes de energia são adicionados. O design modular também facilita a manutenção, permitindo alterações em uma parte do sistema sem impactar outras áreas.

Performance e Testes
A simulação da execução do sistema com tarefas que têm um tempo de delay ajustável e a complexidade de tempo logarítmica mostram uma boa consideração de desempenho. A execução eficiente é crucial para garantir que o sistema possa lidar com grandes volumes de dados sem comprometer a performance, o que é verificado pelos testes de desempenho.