# teste-frexco
Repositório para o teste seletivo na Frexco.
# **Solução**
As tecnologias utilizadas para realizar o projeto foram Django e Django Rest Framework. A autenticação é realizada por meio do Simple JWT. A autenticação pode ser feita utilizando o email ou username. Todos os métodos HTTP, exceto o POST, precisam de um usuário autenticado para realizer a ação, e além disso um usuário só pode alterar suas próprias informações.

# Como Iniciar:
Após realizer o clone do projeto, para instalar todas as dependências utilizadas no mesmo, bast executar o comando abaixo:
```
pip install -r requirements.txt
```
# Endpoints utilizado na API
<table>
  <thead>
    <th>Método HTTP</th>
    <th>Endpoint</th>
    <th>Resultado</th>
  </thead>
  <tbody>
     <tr>
      <td>GET</td>
      <td>/users/</td>
      <td>Retorna todos os usuários</td>
    </tr>
    <tr>
      <td>GET</td>
      <td>/users/{id}/</td>
      <td>Retorna um usuário específico</td>
    </tr>
     <tr>
      <td>POST</td>
      <td>/users/</td>
      <td>Criando um usuário</td>
    </tr>
    <tr>
      <td>PATCH</td>
      <td>/users/{id}/</td>
      <td>Realiza alteração dos dados de um usuário.</td>
    </tr>
    <tr>
      <td>DELETE</td>
      <td>/users/{id}/</td>
      <td>Remover um usuário</td>
    </tr>  
  </tbody>
</table>
