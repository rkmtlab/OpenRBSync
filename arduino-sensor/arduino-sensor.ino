//const int eegpin =
const int ecgpin = 0;
//const int edapin =
//const int emgpin =

void setup() {

  Serial.begin(9600);          // For Serial Monitor

  //pinMode(eegpin,OUTPUT);
  pinMode(ecgpin,OUTPUT);
  //pinMode(edapin,OUTPUT);
  //pinMode(emgpin,OUTPUT);
}

void loop() {

  float ecg = analogRead(ecgpin);
  Serial.print('C');
  Serial.println(ecg);

  /*
  float eeg = analogRead(eegpin);
  Serial.print('E');
  Serial.println(eeg);

  float eda = analogRead(edapin);
  Serial.print('D');
  Serial.println(eda);

  float emg = analogRead(emgpin);
  Serial.print('M');
  Serial.println(emg);
  */
  
  delay(100);                    // considered best practice in a simple sketch.
}

  
