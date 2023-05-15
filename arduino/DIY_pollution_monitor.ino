#include <dht.h>        // Include library
#define outPin 7       // Defines pin number to which the sensor is connected
#include <LiquidCrystal.h> // includes the LiquidCrystal Library 
LiquidCrystal lcd(8, 9, 10, 11, 12, 13); // Creates an LCD object. Parameters: (rs, enable, d4, d5, d6, d7) 

dht DHT;                // Creates a DHT object

int sensorPin=A0; // MQ6
int sensorData;
int sensorPin1=A1; // MQ9
int sensorData1;
void setup()
{  
  Serial.begin(9600);   
  pinMode(sensorPin,INPUT);    
  pinMode(sensorPin1,INPUT); 
  lcd.begin(16,2);                      
 }
void loop()
{
  
  int readData = DHT.read11(outPin);

  float t = DHT.temperature;        // Read temperature
  float h = DHT.humidity;           // Read humidity

  Serial.print("Temperature = ");
  Serial.print(t);
  Serial.print("°C | ");
  Serial.print((t*9.0)/5.0+32.0);        // Convert celsius to fahrenheit
  Serial.println("°F ");
  Serial.print("Humidity = ");
  Serial.print(h);
  Serial.println("% ");
  Serial.println("");

  sensorData = analogRead(sensorPin);       
  Serial.print("Sensor Data:");
  Serial.println(sensorData);
  sensorData1 = analogRead(sensorPin1);       
  Serial.print("Sensor Data:");
  Serial.println(sensorData1);

 lcd.print("Air Pollution");
 lcd.setCursor(2,2);
 lcd.print("Monitor");
 delay(3000); 
 lcd.clear(); 
 lcd.print("Temperature:"); // Prints "Arduino" on the LCD 
 delay(3000); // 3 seconds delay 
 lcd.setCursor(2,1); // Sets the location at which subsequent text written to the LCD will be displayed 
 lcd.print(t); 
 lcd.print((char)223);
 lcd.print("C");
 delay(3000); 
 lcd.clear(); // Clears the display 
 lcd.print("Humidity:"); // Prints "Arduino" on the LCD 
 delay(3000); // 3 seconds delay 
 lcd.setCursor(2,1); // Sets the location at which subsequent text written to the LCD will be displayed 
 lcd.print(h); 
 lcd.print("%");
 delay(3000);
 lcd.clear(); // Clears the display  
 lcd.print("Sensor Data:"); // Prints "Arduino" on the LCD 
 delay(3000); // 3 seconds delay 
 lcd.setCursor(2,1); // Sets the location at which subsequent text written to the LCD will be displayed 
 lcd.print(sensorData); 
 lcd.print("ppm");
 delay(3000); 
 lcd.clear(); // Clears the display  
 lcd.print("Sensor Data1:"); // Prints "Arduino" on the LCD 
 delay(3000); // 3 seconds delay 
 lcd.setCursor(2,1); // Sets the location at which subsequent text written to the LCD will be displayed 
 lcd.print(sensorData1); 
 lcd.print("ppm");
 delay(3000); 
 lcd.clear(); // Clears the display 
 lcd.blink(); //Displays the blinking LCD cursor 
 delay(400); 
 lcd.clear(); // Clears the LCD screen 
 lcd.print("Enjoy ");
 delay(3000); 
 lcd.clear(); 

  delay(1000);   
                                                 
}
