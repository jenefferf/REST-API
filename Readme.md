# Simulação do protocolo de commit em duas fases

​	Esta Restful API foi desenvolvida com o intuito de implementar o algoritmo de eleição utilizando protocolo de commit de duas fases. É importante ressaltar que esta implementação foi desenvolvida apenas para fins didáticos.

# Passos para realização do experimento

- Faça um clone do repositório;

- Instale as depedência do projeto utilizando o comado: pip3  install -r requeriments.txt. De preferência, instale as depedências dentro de um diretório virtual;

- Para executar a API será necessário informar o nome da aplicação e a porta que será utilizada para fazer as requisições.
  Por exemplo: python3 app.py 45000.
   É importante ressaltar que para o experimento funcionar será necessário executar, ao menos, três aplicações em portas distintas.

- Para fazer as requisições para as aplicações é possível utilizar o cURL ou qualquer outro sofwtare  que tem como objetivo testar serviços RESTful, por exemplo, o postman;

- O usuário deverá carregar uma semente em cada uma das aplicações em execução. Utilizando o método HTTP POST na rota  /semente e deverá encaminhar o seguinte *body*:

  {	

  ​	"s": 123

  }
  Informe um número diferente de semente para cada endpoint.

- O usuário deverá escolher uma aplicações para ser  coordenadora. Para tanto, deverá fazer um POST na rota /replicas e encaminhar o seguinte *body* no formato Json:
  {"replicas": [
            {
                "id": "replica 1",
                "endpoint": "http://localhost:55000"
            },
              {
                "id": "replica 2",
                "endpoint": "http://localhost:65000"
            }
          ]

- Após fazer a escolha do coordenador todas as ações nas contas devem ser feitas diretamente para a aplicação coordenadora através do método POST na rota  /acao e informando o seguinte *body* no formato Json:

  {
              "id": "id1",
              "operacao": "debito",
              "conta": 123,
              "valor": 10
     }

  Obs: As operações podem variar entre debito ou crédito, assim como o valor e número da conta.

  # Funcionalidades Implementas

  ​	Todas funcionalidades requisitadas pelo projeto foram implementadas. 

  

  