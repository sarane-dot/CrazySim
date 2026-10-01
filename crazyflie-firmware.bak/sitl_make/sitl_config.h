#undef CONFIG_SENSORS_BMI088_BMP3XX
#undef CONFIG_SENSORS_BMI088_SPI
#undef CONFIG_SENSORS_BOSCH
#undef CONFIG_SENSORS_MPU9250_LPS25H
#undef CONFIG_DECK_LIGHTHOUSE
#undef CONFIG_DECK_LOCO
#undef CONFIG_EEPROM

#define motorsResetESCs() do {} while(0)
#define workerLoop() do {} while(0)
extern void vAssertCalled(unsigned long ulLine, const char * const pcFileName);
