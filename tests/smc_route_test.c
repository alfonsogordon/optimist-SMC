#include <assert.h>
#include "../smc/smc_route.h"
int main(void) {
 struct smc_command c;
 c=smc_route(0,1,0x90,0x5e,127);assert(c.action==SMC_ACT_NONE);
 c=smc_route(1,0,0x90,0x5e,127);assert(c.action==SMC_ACT_NONE);
 c=smc_route(1,1,0x90,0x5e,127);assert(c.action==SMC_ACT_PLAY);
 c=smc_route(1,1,0x90,0x5d,127);assert(c.action==SMC_ACT_STOP);
 c=smc_route(1,1,0x90,0x5e,0);assert(c.action==SMC_ACT_NONE);
 c=smc_route(1,1,0x90,0x12,127);assert(c.action==SMC_ACT_MUTE && c.track==2);
 c=smc_route(1,1,0x90,0x1f,127);assert(c.action==SMC_ACT_SELECT && c.track==7);
 c=smc_route(1,1,0xb0,0x10,0x42);assert(c.action==SMC_ACT_ENCODER && c.amount==-2);
 c=smc_route(1,1,0xe7,0x7f,0x7f);assert(c.action==SMC_ACT_LEVEL && c.track==7 && c.amount==127);
 c=smc_route(1,1,0x91,0x12,127);assert(c.action==SMC_ACT_NONE);
 return 0;
}
