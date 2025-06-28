-----

# 💧 Sistema de Monitoramento e Controle de Tratamento de Água

> Projeto IoT para automação e monitoramento de parâmetros de qualidade da água, com coleta de dados em tempo real para análise e geração de relatórios.

Este projeto utiliza um microcontrolador (ESP32/Arduino) para ler dados de sensores em um sistema simplificado de tratamento de água e controlar atuadores como bombas e válvulas. Um backend em Python é responsável por coletar esses dados via comunicação serial, processá-los e armazená-los em um arquivo CSV para futuras análises.

-----

## ✨ Funcionalidades

  - **Monitoramento em Tempo Real:** Leitura contínua dos sensores de pH, Cor e Turbidez na entrada e na saída do sistema.
  - **Controle de Atuadores:**
      - Acionamento automático da bomba principal com base no nível do reservatório (boia) e na qualidade da água de saída.
      - Dosagem de cloro com base na vazão da água.
      - Controle de uma válvula solenoide para dosagem de coagulante (ex: sulfato férrico) proporcional à turbidez da água de entrada.
  - **Interface Local:** Exibição dos principais parâmetros e status do sistema em dois displays LCD I2C.
  - **Coleta e Armazenamento de Dados:** Um script Python coleta todos os dados enviados pelo microcontrolador e os salva periodicamente em um arquivo `.csv`, com timestamp, para fácil importação e análise.

-----

## 🛠️ Tecnologias e Hardware Utilizados

### Hardware

  * Microcontrolador: **ESP32** (recomendado pelos pinos) ou **Arduino Mega**.
  * Sensores:
      * 2x Sensor de pH
      * 2x Sensor de Turbidez
      * 2x Sensor de Cor
      * 1x Sensor de Vazão de Água
      * 1x Sensor de Nível tipo Boia
  * Atuadores:
      * Módulo Relé para acionamento da Bomba Principal e Bomba Dosadora.
      * Válvula Solenoide para o coagulante.
  * Display: 2x Display LCD 16x2 com módulo I2C.

### Software e Linguagens

  * **C++** (no ambiente Arduino) para a lógica embarcada.
  * **Python 3** para o backend de coleta de dados.
  * **Bibliotecas Principais:**
      * Arduino: `Wire`, `LiquidCrystal_I2C`.
      * Python: `pyserial` (para comunicação serial) e `pandas` (para manipulação e salvamento dos dados).

-----

## 🚀 Como Executar o Projeto

Siga este passo a passo para colocar o sistema em funcionamento.

### Pré-requisitos

1.  **Arduino IDE:** Tenha o ambiente de desenvolvimento do Arduino instalado.
2.  **Bibliotecas Arduino:** Instale a biblioteca `LiquidCrystal_I2C` através do Gerenciador de Bibliotecas da IDE.
3.  **Python 3:** Tenha o Python 3 instalado no computador que rodará o backend.
4.  **Bibliotecas Python:** Instale as dependências `pyserial` e `pandas` com o seguinte comando no seu terminal:
    ```bash
    pip install pyserial pandas
    ```

### Passo a Passo

#### 1\. Montagem do Hardware

Conecte todos os sensores, relés, displays e atuadores ao seu microcontrolador. As conexões devem seguir os pinos definidos no início do código C++ (`.ino`).

#### 2\. Gravar o Código no Microcontrolador

1.  Abra o arquivo `.ino` do projeto na Arduino IDE.
2.  Verifique se o tipo de placa (Ex: "ESP32 Dev Module") e a porta COM/Serial correta estão selecionados no menu `Ferramentas`.
3.  Clique no botão "Carregar" (seta para a direita) para enviar o código ao microcontrolador.

#### 3\. Configurar o Backend Python

1.  Abra o arquivo `backend.py` em um editor de código.
2.  **Atenção:** Encontre a linha `SERIAL_PORT = 'COM3'` e **altere o valor** para a porta serial à qual seu Arduino está conectado.
      * **No Windows:** Geralmente `COM3`, `COM4`, etc.
      * **No Linux:** Geralmente `/dev/ttyUSB0` ou `/dev/ttyACM0`.
      * **No macOS:** Geralmente `/dev/cu.usbmodemXXXX`.
3.  Você pode ajustar o intervalo de salvamento alterando a variável `SAVE_INTERVAL_SECONDS`.

#### 4\. Executar o Backend

1.  Com o Arduino já rodando e conectado ao computador via USB, abra um terminal (Prompt de Comando, PowerShell, etc).
2.  Navegue até a pasta onde o arquivo `backend.py` está salvo.
3.  Execute o script com o comando:
    ```bash
    python backend.py
    ```

#### 5\. Verificar a Saída

  - O terminal começará a exibir os dados recebidos do Arduino em tempo real.
  - Na pasta do projeto, um arquivo chamado `dados_tratamento_agua.csv` será criado. Este arquivo será atualizado com os novos dados coletados a cada intervalo definido (padrão de 5 minutos).
  - Você pode abrir o arquivo `.csv` com Excel, Google Sheets ou outra ferramenta de planilhas para analisar os dados.

-----

## 📂 Estrutura do Repositório

```
/
├── arduino_controller/
│   └── arduino_controller.ino  # Código C++ para o microcontrolador
│
├── python_backend/
│   └── backend.py              # Script Python para coleta de dados
│
└── README.md                   # Este arquivo de documentação
```

-----

## 📈 Próximos Passos (Sugestões)

  - [ ] Criar um Dashboard Web (com Flask ou Dash) para visualização dos dados em tempo real.
  - [ ] Integrar um banco de dados (como SQLite ou InfluxDB) para um armazenamento mais robusto.
  - [ ] Desenvolver um sistema de alertas (e-mail, Telegram) para quando os parâmetros da água estiverem fora do ideal.
  - [ ] Utilizar os dados do `.csv` em um Jupyter Notebook para análises estatísticas e criação de gráficos.

-----

## 📄 Licença

Este projeto está sob a licença APACHE 2.0. Veja o arquivo `LICENSE` para mais detalhes.

-----

## Feito com🩸e 💦 por:
**Anthonny Lucas** LinkedIn:

**Gabriel Renan** (LinkedIn: https://www.linkedin.com/in/gabrielrenan-computer-eng/ || GitHub: https://github.com/GabrielRenanPE)

**Wemerson Carvalho**. LinkeDin:
