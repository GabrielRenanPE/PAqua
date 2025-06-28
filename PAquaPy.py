import serial
import pandas as pd
from datetime import datetime
import time
import os

SERIAL_PORT = 'COM3' 
BAUD_RATE = 115200
OUTPUT_FILE = 'dados_tratamento_agua.csv'
SAVE_INTERVAL_SECONDS = 300

data_records = []
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
    try:
        parts = line.strip().split(',')
        if len(parts) != len(columns) - 1:
            print(f"[AVISO] Linha de dados malformada recebida: {line}")
            return None

        values = [float(p) for p in parts]
        
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
    global data_records
    if not data_records:
        print("[INFO] Nenhum dado novo para salvar.")
        return

    print(f"[INFO] Salvando {len(data_records)} registros em '{OUTPUT_FILE}'...")
    
    df = pd.DataFrame(data_records)
    
    file_exists = os.path.exists(OUTPUT_FILE)
    
    df.to_csv(OUTPUT_FILE, mode='a', header=not file_exists, index=False)
    
    data_records = []
    print("[INFO] Dados salvos com sucesso.")


def main():
    last_save_time = time.time()
    
    print("--- Backend de Coleta de Dados da Estação de Tratamento ---")
    print(f"Escutando a porta serial '{SERIAL_PORT}' a {BAUD_RATE} bps.")
    print(f"Os dados serão salvos em '{OUTPUT_FILE}'.")
    print("Pressione Ctrl+C para parar o programa e salvar os dados restantes.")

    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            ser.flush()

            while True:
                if ser.in_waiting > 0:
                    try:
                        line = ser.readline().decode('utf-8').strip()
                        
                        if line:
                            record = parse_data(line)
                            if record:
                                data_records.append(record)
                                print(f"Recebido: {record}")
                    except Exception as e:
                        print(f"[ERRO] Erro ao ler da serial: {e}")

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
        print("[INFO] Salvando dados finais antes de encerrar...")
        save_data_to_csv()
        print("--- Programa finalizado. ---")


if __name__ == '__main__':
    main()
