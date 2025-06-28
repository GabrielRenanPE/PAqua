// Filtro de Kalman simplificado para pH
class FiltroKalmanPH {
private:
  float estimate = 7.0;
  float errorEstimate = 1.0;
  const float errorMeasurement = 0.1;
  
public:
  float filtrar(float measurement) {
    float gain = errorEstimate / (errorEstimate + errorMeasurement);
    estimate = estimate + gain * (measurement - estimate);
    errorEstimate = (1 - gain) * errorEstimate;
    return estimate;
  }
};

// Filtro de média móvel ponderada
class FiltroMMP {
private:
  static const int TAMANHO_JANELA = 5;
  float valores[TAMANHO_JANELA];
  int indice = 0;
  
public:
  float filtrar(float novoValor) {
    valores[indice] = novoValor;
    indice = (indice + 1) % TAMANHO_JANELA;
    
    float soma = 0, pesoTotal = 0;
    for(int i = 0; i < TAMANHO_JANELA; i++) {
      float peso = (i == indice) ? 1.5 : 1.0;
      soma += valores[i] * peso;
      pesoTotal += peso;
    }
    return soma / pesoTotal;
  }
};

// Instâncias dos filtros
FiltroKalmanPH filtroKalmanPH;
FiltroMMP filtroMMPTurbidez, filtroMMPCor, filtroMMPCloro;

// Funções de leitura com calibração
float lerPH(int pino) {
  float voltage = analogRead(pino) * 3.3 / 4095.0;
  return 2.5 * voltage + 4.0;
}

float lerTurbidez(int pino) {
  int raw = analogRead(pino);
  return raw * 5.0 / 4095.0;
}

float lerCor(int pino) {
  int raw = analogRead(pino);
  return raw * 30.0 / 4095.0;
}

float lerCloro(int pino) {
  int raw = analogRead(pino);
  return raw * 3.0 / 4095.0;
}

// Funções de filtragem
float filtrarPH(float ph) {
  return filtroKalmanPH.filtrar(ph);
}

float filtrarTurbidez(float turbidez) {
  return filtroMMPTurbidez.filtrar(turbidez);
}

float filtrarCor(float cor) {
  return filtroMMPCor.filtrar(cor);
}

float filtrarCloro(float cloro) {
  return filtroMMPCloro.filtrar(cloro);
}