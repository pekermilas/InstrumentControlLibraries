const int red = 9;
const int green = 10;
const int blue = 11;

String getValue(String data, char separator, int index){
// https://stackoverflow.com/questions/9072320/split-string-into-string-array
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void setup(){
  Serial.begin(9600);
  pinMode(blue, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(red, OUTPUT);
}

void loop(){
  while (Serial.available() == 0) {}
  String temp = Serial.readString();
  int redPower = getValue(temp,',',0).toInt();
  int greenPower = getValue(temp,',',1).toInt();
  int bluePower = getValue(temp,',',2).toInt();

  analogWrite(red, redPower);
  analogWrite(green, greenPower);
  analogWrite(blue, bluePower);
  Serial.println(0);
}