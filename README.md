## Redação Unicamp Acessível: Sua Chave para a Escrita Leve e Autoral

**Seja bem-vindo à "Redação Unicamp Acessível"!**

Esta plataforma gratuita, alimentada pela inteligência artificial do 
Google Gemini, te conecta com Dani Stella, sua professora digital de 
redações, especialista na prova da Unicamp.

**Aqui, você terá:**

- **Treinamento de diferentes gêneros textuais:** Aprenda as características de artigos, cartas, manifestos, crônicas, posts e muitos outros gêneros.
- **Dicas para interpretar a coletânea de textos:** Desvende os segredos da coletânea e aprenda a usar as informações dos textos para construir seus próprios argumentos.
- **Estratégias para desenvolver um projeto de texto:** Construa textos coesos e coerentes, com uma estrutura lógica e uma linguagem precisa.
- **Avaliação de redações com feedback detalhado e construtivo:** Receba dicas personalizadas e correções da Dani Stella para aprimorar sua escrita.
- **Auxílio para escrever textos de postagens, artigos científicos etc.:** Dani Stella pode te ajudar a construir textos incríveis para qualquer situação, além da redação do vestibular!

**Com a Dani Stella, você poderá:**

- **Dominar as características da prova da Unicamp:** Entenda os critérios de avaliação e as estratégias para se destacar.
- **Ampliar seu repertório de gêneros textuais:** Aprenda a escrever com leveza e criatividade em diferentes gêneros.
- **Contar com o apoio e a orientação da Dani Stella:** Receba ajuda para alcançar seus objetivos de escrita.

**Junte-se à comunidade "Redação Unicamp Acessível"!**  Converse com a Dani Stella agora mesmo e dê o primeiro passo rumo à conquista da sua vaga na Unicamp!

## Como usar a plataforma

1. **Acesse a plataforma:** Clique no link do repositório GitHub para acessar a plataforma.
2. **Configure o modelo:** Na seção de configurações, insira sua chave de API do Google Gemini para habilitar a interação com Dani Stella.
3. **Comece a conversar:** Utilize o chat para conversar com Dani Stella.
4. **Solicite uma avaliação:** Informe o número e o ano
da proposta de redação da Unicamp que você escolheu, junto com sua
redação, para que Dani Stella lhe forneça uma avaliação detalhada.

## Arquivos e Estrutura do Projeto

```
└── redacao-unicamp-acessivel
    └── chat_session.py
    └── llm_model.py
    └── main.py
    └── __pycache__
    └── sql_connection.py
        └── chat_history.db

```

- **`redacao-unicamp-acessivel`:** Pasta principal do projeto.
    - **`chat_session.py`:** Gerencia o histórico de conversas com Dani Stella.
    - **`llm_model.py`:** Define as classes base para os modelos de linguagem.
    - **`main.py`:** Código principal da plataforma Streamlit.
    - **`__pycache__`:** Pasta com arquivos compilados.
    - **`sql_connection.py`:** Conexão com o banco de dados SQLite.
    - **`chat_history.db`:** Banco de dados que armazena o histórico das conversas.

## Instalação e Execução

Para usar a plataforma "Redação Unicamp Acessível" localmente, siga as instruções abaixo:

1. **Instale as Dependências:**
    
    ```bash
    python -m pip install -r requirements.txt
    
    ```
    
- Este comando instalará todas as bibliotecas Python necessárias para executar a plataforma.
- **Execute a Plataforma:**
    
    ```bash
    streamlit run redacao-unicamp-acessivel/main.py
    
    ```
    
2. Este comando irá iniciar a plataforma no seu navegador. Você poderá
interagir com a Dani Stella e utilizar todas as funcionalidades da
plataforma.

**Observações:**

- Certifique-se de ter o Streamlit instalado em seu sistema. Se você não tiver, pode instalar usando `pip install streamlit`.
- Para usar o modelo Gemini, você precisará obter uma chave de API do Google Gemini. Para criar uma chave de API, acesse https://aistudio.google.com/app/apikey.
- Após a instalação e execução, a plataforma estará acessível em seu navegador no endereço `http://localhost:8501`.

## Contribuições

Agradecemos a todos que contribuíram para o desenvolvimento da plataforma "Redação Unicamp Acessível":

- **Dani Stella (a humana):** A musa inspiradora da persona Dani Stella, a professora digital.
- **Emilly:** Minha prima, que contribuiu com redações para aprimorar o prompt.
- **Gabriela:** Que também ajudou imensamente fornecendo redações para melhorar o prompt.
- **Nícolas:** Que também forneceu suas redações para que pudéssemos melhorar o prompt.
- **Google DeepMind e o Google Gemini:** A mente
brilhante por trás da inteligência artificial que tornou essa plataforma possível. Sem a API gratuita e a grande janela de contexto, a Dani
Stella nunca teria sido possível.

**Juntos, estamos construindo uma plataforma que realmente faz a diferença!**

## Licença

Este projeto está licenciado sob a licença MIT.
