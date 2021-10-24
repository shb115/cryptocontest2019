#include <stdio.h>

unsigned char add(unsigned char* R, unsigned char* IN1, unsigned char* IN2)
{
  unsigned char CARRY = 0;
  
  R[6] = IN1[6] + IN2[6];
  if (R[6] < IN1[6])
    CARRY = 1;
  
  for (int i = 5;i >= 0;i--)
  {
    if (CARRY)
    {
      R[i] = IN1[i] + IN2[i] + 1;
      if (R[i] <= IN1[i])
        CARRY = 1;
      else
        CARRY = 0;
    }
    else
    {
      R[i] = IN1[i] + IN2[i];
      if (R[i] < IN1[i])
        CARRY = 1;
      else
        CARRY = 0;
    }
  }
  return CARRY;
}

void mod(unsigned char* OUT, unsigned char* IN, unsigned char CARRY)
{
  int i;

  if (CARRY)
  {
    for (i = 6;i >= 1;i--)
    {
      if (IN[i] == 0xff && OUT[i] == 0)
        OUT[i - 1] = IN[i - 1] + 1;
      else
        break;
    }
    for (i;i >= 0;i--)
    {
      OUT[i] = IN[i];
    }       
  }
  else
    OUT = IN;
}

void setup() 
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  unsigned char A[7] = { 0x2D,0x6D,0x01,0x48,0xF5,0xB6,0x44 };
  unsigned char B[7] = { 0x25,0x15,0x9E,0xBD,0xB7,0x93,0xD0 };
  unsigned char C[7] = { 0x3F,0x88,0x48,0x20,0xB9,0x2B,0xAF };
  unsigned char D[7] = { 0x2C,0x55,0x93,0xAF,0xA6,0x60,0xD0 };
  unsigned char E[7] = { 0x36,0xE9,0xAD,0x60,0x60,0x02,0x3D };
  unsigned char R[7], R1[7], R2[7], R3[7], R4[7], CARRY;
  
  u32 time1;
  u32 time2;
  time1 = millis();
  for(int i=0;i<10000;i++)
  {    
    CARRY=add (R1,A,B);
    mod (R1,R1,CARRY);    
    CARRY=add (R2,R1,C);
    mod (R2,R2,CARRY);    
    CARRY=add (R3,R2,D);
    mod (R3,R3,CARRY);
    CARRY=add (R4,R3,E);
    mod (R,R4,CARRY);
    }
    time2 = millis();
    Serial.println((time2-time1));
    }

void loop() {
  // put your main code here, to run repeatedly:

}
