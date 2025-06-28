import serial
import pandas as pd
from datetime import datetime
import time
import os

# --- CONFIGURAÇÕES ---
# Altere para a porta serial correta. Exemplos:
# Windows: 'COM3'
# Linux: '/dev/ttyUSB0' ou '/dev/ttyACM0'
# macOS: '/dev/cu.usbmodem1411'
SERIAL_PORT = 'COM3' 
BAUD_RATE = 115200
OUTPUT_FILE = 'dados_tratamento_agua.csv'
# Intervalo em segundos para salvar os dados no arquivo
SAVE_INTERVAL_SECONDS = 300 # Salva a cada 5 minutos

# --- ESTRUTURA DE DADOS ---
# Lista para armazenar os registros de dados em memória
data_records = []
# Nomes das colunas para o DataFrame do pandas
# A ordem DEVE ser a mesma do Arduino
columns = [
    'timestamp', 
    'ph_entrada', 
    'cor_entrada', 
    'turbidez_entrada',
    'ph_saida', 
    'cor_saida', 
    'turbidez_saida', 
    'vazao_L_min',
    'bomba_ligada', 
    'dosando_cloro', 
    'valvula_coagulante_aberta'
]

def parse_data(line: str) -> dict or None:
    """
    Interpreta uma linha de dados vinda do Arduino e a transforma em um dicionário.
    """
    try:
        parts = line.strip().split(',')
        if len(parts) != len(columns) - 1: # -1 porque o timestamp é adicionado aqui
            print(f"[AVISO] Linha de dados malformada recebida: {line}")
            return None

        # Converte os valores para os tipos corretos (float e int)
        values = [float(p) for p in parts]
        
        # Cria um dicionário com os dados
        record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ph_entrada': values[0],
            'cor_entrada': values[1],
            'turbidez_entrada': int(values[2]),
            'ph_saida': values[3],
            'cor_saida': values[4],
            'turbidez_saida': int(values[5]),
            'vazao_L_min': values[6],
            'bomba_ligada': bool(int(values[7])),
            'dosando_cloro': bool(int(values[8])),
            'valvula_coagulante_aberta': bool(int(values[9]))
        }
        return record
    except (ValueError, IndexError) as e:
        print(f"[ERRO] Não foi possível interpretar a linha: '{line}'. Erro: {e}")
        return None

def save_data_to_csv():
    """
    Salva os dados coletados em memória para um arquivo CSV e limpa a lista.
    """
    global data_records
    if not data_records:
        print("[INFO] Nenhum dado novo para salvar.")
        return

    print(f"[INFO] Salvando {len(data_records)} registros em '{OUTPUT_FILE}'...")
    
    # Cria um DataFrame do pandas com os dados coletados
    df = pd.DataFrame(data_records)
    
    # Verifica se o arquivo já existe para decidir se o cabeçalho deve ser escrito
    file_exists = os.path.exists(OUTPUT_FILE)
    
    # Salva no arquivo CSV. 'a' para 'append' (adicionar ao final).
    df.to_csv(OUTPUT_FILE, mode='a', header=not file_exists, index=False)
    
    # Limpa a lista em memória após salvar
    data_records = []
    print("[INFO] Dados salvos com sucesso.")


def main():
    """
    Função principal que inicia a escuta da porta serial.
    """
    last_save_time = time.time()
    
    print("--- Backend de Coleta de Dados da Estação de Tratamento ---")
    print(f"Escutando a porta serial '{SERIAL_PORT}' a {BAUD_RATE} bps.")
    print(f"Os dados serão salvos em '{OUTPUT_FILE}'.")
    print("Pressione Ctrl+C para parar o programa e salvar os dados restantes.")

    try:
        # Inicia a conexão serial
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            ser.flush() # Limpa o buffer de entrada

            while True:
                # Verifica se há dados na porta serial
                if ser.in_waiting > 0:
                    try:
                        # Lê uma linha (termina em \n) e a decodifica de bytes para string
                        line = ser.readline().decode('utf-8').strip()
                        
                        if line:
                            # Interpreta a linha de dados
                            record = parse_data(line)
                            if record:
                                # Adiciona o registro válido à nossa lista
                                data_records.append(record)
                                print(f"Recebido: {record}")
                    except Exception as e:
                        print(f"[ERRO] Erro ao ler da serial: {e}")

                # Verifica se está na hora de salvar os dados no arquivo
                if time.time() - last_save_time > SAVE_INTERVAL_SECONDS:
                    save_data_to_csv()
                    last_save_time = time.time()

    except serial.SerialException as e:
        print(f"\n[ERRO FATAL] Não foi possível abrir a porta serial '{SERIAL_PORT}'.")
        print(f"Detalhes: {e}")
        print("Verifique se a porta está correta e se o Arduino está conectado.")
    except KeyboardInterrupt:
        print("\n[INFO] Programa interrompido pelo usuário.")
    finally:
        # Garante que os últimos dados coletados sejam salvos antes de sair
        print("[INFO] Salvando dados finais antes de encerrar...")
        save_data_to_csv()
        print("--- Programa finalizado. ---")


if __name__ == '__main__':
    main()