## Aplicação de Agendamento de Revisões Utilizando Aprendizado por Reforço
Esse repositório hospeda o back-end da aplicação de agendamento de revisões utilizando aprendizado por reforço e 
repetição espaçada. O aprendizado por reforço é implementado utilizando o Q-Learning (Os parâmentros definidos pelo 
Q-learning podem ser encontrados em: agente/agente.py).  
A implementação contempla o Agente (calcula o novo EF do card), pelo Ambiente (calcula a recompensa e fornece um 
estado ao agente) e pela API (faz comunicação com o protótipo da Interface do usuário).  
O repositório do protótipo da interface do usuário pode ser encontrada nesse 
[link](https://github.com/algoritmo-agendamento-revisao/arali-frontend).

### Requisitos de software:
* Python 3.6+
* pip3
* MongoDB

### Configuração do Mongo
* O mongoDB deve estar com o serviço rodando no endereço localhost (127.0.0.1) na porta 27017.
* Deve ser criado um banco de dados com o nome 'arali', assim como uma coleção com o nome: 'estado'.

### Dependências em Python
São especificadas no arquivo requirements.txt