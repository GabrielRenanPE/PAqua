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
