## Redação Unicamp Acessível: Sua Chave para a Escrita Leve e Autoral

### **Seja bem-vindo à "Redação Unicamp Acessível"!**

Esta plataforma gratuita, alimentada pela inteligência artificial do Google Gemini, te conecta com Dani Stella, sua professora digital de redações, especialista na prova da Unicamp.

### **O Google Gemini, a mente por trás da Dani Stella:**

A plataforma "Redação Unicamp Acessível" utiliza a [API do Google Gemini](https://aistudio.google.com/app/apikey) para oferecer respostas e feedbacks personalizados. A Dani Stella foi criada a partir de um prompt detalhado que define sua  persona e conhecimento sobre a redação da Unicamp. A API do Gemini permite que Dani Stella acesse e processe informações da coletânea de textos, entenda o contexto da redação e forneça um feedback preciso e útil.

### **Aqui, você terá:**

- **Treinamento de diferentes gêneros textuais:** Aprenda as características de artigos, cartas, manifestos, crônicas, posts e muitos outros gêneros.
- **Dicas para interpretar a coletânea de textos:** Desvende os segredos da coletânea e aprenda a usar as informações dos textos para construir seus próprios argumentos.
- **Estratégias para desenvolver um projeto de texto:** Construa textos coesos e coerentes, com uma estrutura lógica e uma linguagem precisa.
- **Avaliação de redações com feedback detalhado e construtivo:** Receba dicas personalizadas e correções da Dani Stella para aprimorar sua escrita.
- **Auxílio para escrever textos de postagens, artigos científicos etc.:** Dani Stella pode te ajudar a construir textos incríveis para qualquer situação, além da redação do vestibular!

### **Sala de Aula da Dani Stella Digital:**

Visite minha sala de aula [aqui](https://joseph-maazal.notion.site/Sala-de-aula-de-Dani-Stella-a-professora-digital-de-reda-es-715189cb31084854977cbf95713fff15)!

### **Studio da Dani Stella Digital:**

Converse comigo também através do [Google AI Studio](https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%221oj8_QS81ZZs1pqforiI2J_og3OwmJlRc%22%5D,%22action%22:%22open%22,%22userId%22:%22113467815809743682406%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing).

### **Com a Dani Stella, você poderá:**

- **Dominar as características da prova da Unicamp:** Entenda os critérios de avaliação e as estratégias para se destacar.
- **Ampliar seu repertório de gêneros textuais:** Aprenda a escrever com leveza e criatividade em diferentes gêneros.
- **Contar com o apoio e a orientação da Dani Stella:** Receba ajuda para alcançar seus objetivos de escrita.

**Junte-se à comunidade "Redação Unicamp Acessível"!**  Converse com a Dani Stella agora mesmo e dê o primeiro passo rumo à conquista da sua vaga na Unicamp!

## Como usar a plataforma Redação Acessível

Para testar a plataforma e conversar comigo, a Dani Stella, siga estes passos no video abaixo ou na descrição que o segue:

[![Redação Unicamp Acessível, a plataforma de Dani Stella, sua professora digital de redações](https://img.youtube.com/vi/RGs4Cbt1-v4/0.jpg)](https://www.youtube.com/watch?v=RGs4Cbt1-v4)

**1. Acesse a plataforma:**

- A plataforma "Redação Unicamp Acessível" está disponível em: https://redacao-unicamp-acessivel.streamlit.app

**2. Explore a plataforma:**

- Leia as seções da plataforma para se familiarizar com a proposta e entender como usar a plataforma:
    - "✍️ Redação Unicamp Acessível: a chave para a escrita leve e autoral"
    - "🌎 A Unicamp: um portal para o futuro"
    - "🗝️ Redação Unicamp: desvendando os segredos da escrita"
    - "👩🏾‍🏫 Dani Stella: a professora digital que te guia na jornada da escrita autoral"
    - "📚 Provas de Redação Passadas: desvendando os segredos da Unicamp"
    - "🙏 Agradecimentos"

**3. Configure o modelo Gemini:**

- Acesse a seção "⚙️ Configurações do modelo de Inteligência Artificial Gemini"
    - Entre com a sua chave de API do Google Gemini no campo indicado.
    - Para gerar uma chave de API nova, acesse: https://aistudio.google.com/app/apikey
    - Selecione o modelo Gemini desejado.
    - Clique no botão "Executar" para inicializar o modelo.

**4. Converse com a Dani Stella:**

- Após configurar o modelo, você poderá conversar comigo.
- Na caixa de chat, informe o número e o ano da proposta de redação da Unicamp que você escolheu.
- Em seguida, insira a sua redação.
- Dani Stella te dará uma avaliação completa, com um feedback detalhado e construtivo sobre:
    - Proposta Temática (Pt)
    - Gênero (G)
    - Leitura dos Textos (Lt)
    - Convenções da Escrita e Coesão (CeC)

**5. Utilize a Plataforma como um todo:**

- Explore a plataforma, incluindo as provas de redação passadas e as informações sobre a Unicamp.
- Faça o download do prompt da Dani Stella para entender a estrutura da persona.
- Utilize a plataforma como um recurso valioso para aprimorar suas habilidades de escrita e se preparar para o vestibular!

**Lembre-se:**

- O tempo de resposta da Dani Stella pode variar de acordo com o modelo escolhido e a complexidade da sua redação.
- Dani Stella ainda está em fase de aprendizado, e você poderá encontrar algumas falhas e imprecisões em suas respostas.
- Use a plataforma para aprimorar sua escrita, mas sempre revise e edite seu texto com cuidado!

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
    
2. Este comando irá iniciar a plataforma no seu navegador. Você poderá interagir com a Dani Stella e utilizar todas as funcionalidades da plataforma.

**Observações:**

- Certifique-se de ter o Streamlit instalado em seu sistema. Se você não tiver, pode instalar usando `pip install streamlit`.
- Para usar o modelo Gemini, você precisará obter uma chave de API do Google Gemini. Para criar uma chave de API, acesse https://aistudio.google.com/app/apikey.
- Após a instalação e execução, a plataforma estará acessível em seu navegador no endereço `http://localhost:8501`.

## Contribuições

Agradecemos a todos que contribuíram para o desenvolvimento da plataforma "Redação Unicamp Acessível":

- **[Universidade de Campinas (Unicamp)](https://unicamp.br/):**  Agradecemos profundamente à Unicamp por disponibilizar, de forma gratuita, um material de alta qualidade para a prova de redação do vestibular, em especial à Comissão Organizadora da prova de redação. Sem esse material valioso, a persona da Dani Stella e a plataforma "Redação Unicamp Acessível" não seriam possíveis.
- **[Dani Stella (a humana)](https://www.instagram.com/danistellacg/):** A musa inspiradora da persona Dani Stella, a professora digital.
- **[Emilly (a humana)](https://www.linkedin.com/in/emilly-oliveira-a32169272/):** Minha prima, que contribuiu com redações para aprimorar o prompt.
- **[Gabriela (a humana)](https://www.linkedin.com/in/gabriela-martins-08174430a):** Que também ajudou imensamente fornecendo redações para melhorar o prompt.
- **[Nícolas (o humano)](https://www.linkedin.com/in/nicolas-pedoni-8b75722a7):** Que também forneceu suas redações para que pudéssemos melhorar o prompt.
- **[Google DeepMind](https://deepmind.google/) e o [Google Gemini](https://gemini.google.com/app):** A mente brilhante por trás da inteligência artificial que tornou essa plataforma possível. Sem a API gratuita e a grande janela de contexto, a Dani Stella nunca teria sido possível.

**Juntos, estamos construindo uma plataforma que realmente faz a diferença!**

## Licença

Este projeto está licenciado sob a [licença MIT](LICENSE). Também, note que o meu prompt possui algumas cópias diretas das coletâneas e redações comentadas fornecidas publicamente pela comissão organizadora da prova de redação da Unicamp, COMVEST. Consulte os arquivos originais abaixo para acesso na íntegra das propostas e redações comentadas:

- **Vestibular de 2020 da Unicamp:** https://www.comvest.unicamp.br/wp-content/uploads/2020/09/F2_Redacao_2020.pdf
- **Vestibular de 2021 da Unicamp:** https://www.comvest.unicamp.br/wp-content/uploads/2021/11/CQ_RED-3.pdf
- **Vestibular de 2022 da Unicamp:** https://www.comvest.unicamp.br/wp-content/uploads/2022/06/Redacao-comentada_2022.pdf
- **Vestibular de 2023 da Unicamp:** https://www.comvest.unicamp.br/wp-content/uploads/2023/06/F2_REDACAO.pdf
- **Vestibular de 2024 da Unicamp:** https://www.comvest.unicamp.br/wp-content/uploads/2024/06/1o-dia_RED.pdf

## Prontos para esta jornada de descobrimento da escrita autêntica?

**E aí, meus alunos, prontos para desvendar os segredos da escrita?**

Abracem o desafio da Unicamp com paixão e determinação! Lembrem-se: a escrita autêntica é a chave para o sucesso, e eu, Dani Stella, estou aqui para guiar vocês nessa jornada.

**Contem comigo!**

**Dani Stella: a professora digital de redações.**
