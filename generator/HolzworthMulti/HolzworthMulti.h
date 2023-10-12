/*******************************************************************/
/*                                                                 */
/* File Name:   HolzworthMulti.h                                   */
/*                                                                 */
/*                                                                 */
/*******************************************************************/

extern "C" __declspec(dllexport) int deviceAttached(const char *serialnum);
extern "C" __declspec(dllexport) char* usbCommWrite(const char *serialnum, const char *pBuf);
extern "C" __declspec(dllexport) int RFPowerOn(const char *serialnum);
extern "C" __declspec(dllexport) int RFPowerOff(const char *serialnum);
extern "C" __declspec(dllexport) short isRFPowerOn(const char *serialnum);
extern "C" __declspec(dllexport) int setPower(const char *serialnum, short powernum);
extern "C" __declspec(dllexport) int setPowerS(const char *serialnum, const char *powerstr);
extern "C" __declspec(dllexport) short readPower(const char *serialnum);
extern "C" __declspec(dllexport) int setPhase(const char *serialnum, short phasenum);
extern "C" __declspec(dllexport) int setPhaseS(const char *serialnum, const char *phasestr);
extern "C" __declspec(dllexport) short readPhase(const char *serialnum);
extern "C" __declspec(dllexport) int setFrequency(const char *serialnum, INT64 frequencynum);
extern "C" __declspec(dllexport) int setFrequencyS(const char *serialnum, const char *frequencystr);
extern "C" __declspec(dllexport) INT64 readFrequency(const char *serialnum);
extern "C" __declspec(dllexport) int recallFactoryPreset(const char *serialnum);
extern "C" __declspec(dllexport) int saveCurrentState(const char *serialnum);
extern "C" __declspec(dllexport) int recallSavedState(const char *serialnum);
extern "C" __declspec(dllexport) int ModEnableNo(const char *serialnum);
extern "C" __declspec(dllexport) int ModEnableFM(const char *serialnum);
extern "C" __declspec(dllexport) int ModEnablePulse(const char *serialnum);
extern "C" __declspec(dllexport) int ModEnablePM(const char *serialnum);
extern "C" __declspec(dllexport) int setFMDeviation(const char *serialnum, short fmDevnum);
extern "C" __declspec(dllexport) int setFMDeviationS(const char *serialnum,const char *fmDevstr);
extern "C" __declspec(dllexport) int setPMDeviation(const char *serialnum, short pmnum);
extern "C" __declspec(dllexport) int setPMDeviationS(const char *serialnum,const char *pmstr);

extern "C" __declspec(dllexport) void close_all (void);

extern "C" __declspec(dllexport) char* write_string3(const char* serialnum, const char *pBuf);
