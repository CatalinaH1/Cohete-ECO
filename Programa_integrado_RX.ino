#include <SPI.h>
#include <RF24.h>

RF24 radio(10, 8); // CE, CSN
const byte address[6] = "00001";

float ALTITUD, AcX, AcY, AcZ, GyX, GyY, GyZ, TEMPERATURA;

void setup() 
{
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setChannel(101);
  radio.setDataRate(RF24_250KBPS);
  radio.setPALevel(RF24_PA_MAX);
  radio.startListening(); 
}

void loop()
{
  if (radio.available())     
  {  
    float datos[8];
    radio.read(datos, sizeof(datos));
    ALTITUD = datos[0];
    AcX = datos[1];
    AcY = datos[2];
    AcZ = datos[3];
    GyX = datos[4];
    GyY = datos[5];
    GyZ = datos[6];
    TEMPERATURA = datos[7];

    Serial.print(ALTITUD);
    Serial.print(",");
    Serial.print(AcX);
    Serial.print(",");
    Serial.print(AcY);
    Serial.print(",");
    Serial.print(AcZ);
    Serial.print(",");
    Serial.print(GyX);
    Serial.print(",");
    Serial.print(GyY);
    Serial.print(",");
    Serial.print(GyZ);
    Serial.print(",");
    Serial.println(TEMPERATURA); 
  }
  delay(50);
}
