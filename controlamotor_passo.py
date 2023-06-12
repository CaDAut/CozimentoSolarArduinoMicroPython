
#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <AccelStepper.h>

const char* ssid = "NOME_DA_REDE_WIFI";
const char* password = "SENHA_DA_REDE_WIFI";

WebServer server(80);

// Configurações dos motores de passo
#define MOTOR1_STEP_PIN 26
#define MOTOR1_DIR_PIN 27
#define MOTOR2_STEP_PIN 32
#define MOTOR2_DIR_PIN 33
#define MOTOR3_STEP_PIN 34
#define MOTOR3_DIR_PIN 35
#define MOTOR4_STEP_PIN 36
#define MOTOR4_DIR_PIN 39

AccelStepper motor1(AccelStepper::DRIVER, MOTOR1_STEP_PIN, MOTOR1_DIR_PIN);
AccelStepper motor2(AccelStepper::DRIVER, MOTOR2_STEP_PIN, MOTOR2_DIR_PIN);
AccelStepper motor3(AccelStepper::DRIVER, MOTOR3_STEP_PIN, MOTOR3_DIR_PIN);
AccelStepper motor4(AccelStepper::DRIVER, MOTOR4_STEP_PIN, MOTOR4_DIR_PIN);

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Conectar ao Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao Wi-Fi...");
  }

  Serial.println("Conectado ao Wi-Fi!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());

  // Configurar roteamento da Web
  server.on("/", handleRoot);
  server.onNotFound(handleNotFound);
  server.begin();

  // Configurar motores de passo
  motor1.setMaxSpeed(1000);
  motor1.setAcceleration(100);
  motor2.setMaxSpeed(1000);
  motor2.setAcceleration(100);
  motor3.setMaxSpeed(1000);
  motor3.setAcceleration(100);
  motor4.setMaxSpeed(1000);
  motor4.setAcceleration(100);
}

void loop() {
  server.handleClient();

  // Verificar se há novas coordenadas a cada 5 minutos
  if (millis() % (5 * 60 * 1000) == 0) {
    // Obter as coordenadas do usuário externo
    // (você precisará implementar esse código)
    float coord1 = getCoordinate(1);
    float coord2 = getCoordinate(2);
    float coord3 = getCoordinate(3);
    float coord4 = getCoordinate(4);

    // Mover os motores para as coordenadas fornecidas
    motor1.moveTo(coord1);
    motor2.moveTo(coord2);
    motor3.moveTo(coord3);
    motor4.moveTo(coord4);
  }

  // Atualizar os motores
  motor1.run();
  motor2.run();
  motor3.run();
  motor4.run();
}

void handleRoot() {
  String message = "ESP32 está funcionando!";
  server.send(200, "text/plain", message);
}

void handleNotFound() {
  String message = "Página não encontrada";
  server.send(404, "text/plain", message);
}

float getCoordinate(int motorIndex) {
  // Aqui você precisa implementar a lógica para obter as coordenadas
  // do usuário externo para cada motor. Pode ser por meio de uma
  // comunicação serial, conexão com banco de dados ou qualquer outra
  // forma de obter os valores.
  // Neste exemplo, simplesmente retornamos um valor fixo.
  switch (motorIndex) {
    case 1:
      return 1000.0;
    case 2:
      return 2000.0;
    case 3:
      return 3000.0;
    case 4:
      return 4000.0;
    default:
      return 0.0;
  }
}
