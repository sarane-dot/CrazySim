#include "usddeck.h"

bool usddeckLoggingEnabled(void) { return false; }
enum usddeckLoggingMode_e usddeckLoggingMode(void) { return usddeckLoggingMode_Disabled; }
int usddeckFrequency(void) { return 0; }
void usddeckTriggerLogging(void) {}
uint32_t usddeckFileSize(void) { return 0; }
bool usddeckRead(uint32_t offset, uint8_t* buffer, uint16_t length) { return false; }
