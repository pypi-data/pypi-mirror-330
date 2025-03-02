if you want to do MAN IN THE MIDDLE - START SUOFEI SCALE APPLICATION AND INSTALL com0com - virtual serial port

BAUD: 9600
NO FLOW CONTROL

Works with HERCULES SERIAL PORT

PROTOCOL:

EXAMPLE FRAME:



5F0400028FD6 6,55 kg
{5F}{04}{00}{00}{1E}{45} 0,30 kg
{5F}{04}{00}{00}{23}{78} 0,35 kg
{5F}{04}{00}{02}{D0}{89} 7,2 kg

PRZYKŁADOWA ODPOWIEDŹ MQTT

0x5F 0x04 0x00 0x05 0x3C 0x62

{5F}{44}{00}{02}{8F}{D6}  -6,55 kg - the second byte is changed to 44 instead of 04