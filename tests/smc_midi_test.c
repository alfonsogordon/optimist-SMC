#include <assert.h>
#include "../smc/smc_midi.h"
int main(void) {
 struct smc_event e;
 e=smc_decode(0x90,0x08,127); assert(e.kind==SMC_BUTTON && e.index==8 && e.value==1);
 e=smc_decode(0x80,0x08,127); assert(e.kind==SMC_BUTTON && e.value==0);
 e=smc_decode(0x90,0x5e,0); assert(e.kind==SMC_BUTTON && e.value==0);
 e=smc_decode(0xb0,0x10,64); assert(e.kind==SMC_KNOB && e.index==0 && e.value==64);
 e=smc_decode(0xe7,127,127); assert(e.kind==SMC_FADER && e.index==7 && e.wide==16383 && e.value==127);
 e=smc_decode(0xe0,0,0); assert(e.kind==SMC_FADER && e.value==0);
 e=smc_decode(0x91,0x08,127); assert(e.kind==SMC_OTHER);
 e=smc_decode(0xb0,0x10,255); assert(e.kind==SMC_OTHER);
 return 0;
}
