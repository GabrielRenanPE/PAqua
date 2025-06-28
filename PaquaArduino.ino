#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SD.h>
#include <SPI.h>

LiquidCrystal_I2C lcd1(0x27, 16, 2);
LiquidCrystal_I2C lcd2(0x3F, 16, 2);

const int sensorTurbidezEntrada = 34;
const int sensorPhEntrada = 32;
const int sensorCorEntrada = 25;

const int sensorTurbidezSaida = 35;
const int sensorPhSaida = 33;
const int sensorCorSaida = 26;

const int pinoBoia = 4;
const int pinoReleBomba = 15;
const int pinoDosadorCloro = 14;
const int pinoValvulaCoagulante = 12;

const int pinoSensorVazao = 27;
volatile unsigned int pulsosVazao = 0;
unsigned long tempoAnteriorVazao = 0;
float vazao = 0.0;

bool bombaLigada = false;
bool dosadorLigado = false;
bool valvulaAberta = false;
unsigned long lastUpdateDisplay = 0;
int estadoDisplay = 0;

const float ppmDesejado = 2.0;
const float percentualCloro = 0.12;
const unsigned int tempoPorMl = 1000;
unsigned long ultimaDosagem = 0;
unsigned long tempoDosagemMs = 0;
unsigned long inicioDosagem = 0;
bool dosandoAgora = false;

const int turbidezMin = 100;
const int turbidezMax = 800;
unsigned long tempoValvulaAberta = 0;
unsigned long inicioValvula = 0;
bool valvulaLigandoAgora = false;

void IRAM_ATTR contarPulsosVazao() {
  pulsosVazao++;
}

void setup() {
  Wire.begin(21, 22);
  lcd1.init();
  lcd1.backlight();
  lcd2.init();
  lcd2.backlight();
  Serial.begin(115200);

  pinMode(pinoBoia, INPUT_PULLUP);
  pinMode(pinoReleBomba, OUTPUT);
  pinMode(pinoDosadorCloro, OUTPUT);
  pinMode(pinoValvulaCoagulante, OUTPUT);
  pinMode(pinoSensorVazao, INPUT_PULLUP);

  digitalWrite(pinoReleBomba, LOW);
  digitalWrite(pinoDosadorCloro, LOW);
  digitalWrite(pinoValvulaCoagulante, LOW);

  attachInterrupt(digitalPinToInterrupt(pinoSensorVazao), contarPulsosVazao, RISING);
}

void loop() {
  unsigned long agora = millis();

  if (agora - tempoAnteriorVazao >= 1000) {
    noInterrupts();
    unsigned int pulsos = pulsosVazao;
    pulsosVazao = 0;
    interrupts();

    const float fator = 7.5;
    vazao = pulsos / fator;
    tempoAnteriorVazao = agora;
  }

  float phEntrada = map(analogRead(sensorPhEntrada), 0, 4095, 0, 140) / 10.0;
  float corEntrada = map(analogRead(sensorCorEntrada), 0, 4095, 0, 1000) / 10.0;
  int turbidezEntrada = analogRead(sensorTurbidezEntrada);

  float phSaida = map(analogRead(sensorPhSaida), 0, 4095, 0, 140) / 10.0;
  float corSaida = map(analogRead(sensorCorSaida), 0, 4095, 0, 1000) / 10.0;
  int turbidezSaida = analogRead(sensorTurbidezSaida);

  bool boiaAtiva = digitalRead(pinoBoia) == LOW;

  bool qualidadeOK = (phSaida >= 6.0 && phSaida <= 9.5) &&
                     (turbidezSaida <= 1000) &&
                     (corSaida <= 75.0);

  if ((boiaAtiva && qualidadeOK) != bombaLigada) {
    bombaLigada = (boiaAtiva && qualidadeOK);
    digitalWrite(pinoReleBomba, bombaLigada ? HIGH : LOW);
  }

  if (agora - ultimaDosagem >= 60000 && vazao > 0) {
    float mlCloro = (vazao * ppmDesejado) / (percentualCloro * 1000);
    tempoDosagemMs = mlCloro * tempoPorMl;

    if (tempoDosagemMs > 0) {
      digitalWrite(pinoDosadorCloro, HIGH);
      inicioDosagem = agora;
      dosandoAgora = true;
    }

    ultimaDosagem = agora;
  }

  if (dosandoAgora && (agora - inicioDosagem >= tempoDosagemMs)) {
    digitalWrite(pinoDosadorCloro, LOW);
    dosandoAgora = false;
  }

  if (turbidezEntrada < turbidezMin) {
    tempoValvulaAberta = 0;
  } else if (turbidezEntrada >= turbidezMax) {
    tempoValvulaAberta = 60000;
  } else {
    tempoValvulaAberta = map(turbidezEntrada, turbidezMin, turbidezMax, 0, 60000);
  }

  if (!valvulaLigandoAgora && tempo