/*
PEERS RTLS Platform
Copyright (C) NEELAR LLC, 2020
business@neelar.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
#include "port_platform.h"
#include "deca_types.h"
#include "deca_param_types.h"
#include "deca_regs.h"
#include "deca_device_api.h"
#include "default_config.h"
#include "instance.h"
#include "config.h"
#include "LIS2DH12.h"

/**< Task delay. Delays a LED0 task for 200 ms */
#define TASK_DELAY      200

/**< Timer period. LED1 timer will expire after 1000 ms */
#define TIMER_PERIOD    2000

/* Configuration in default_config.h */
app_cfg_t app;

/* @Fn  inittestapplication
 * @brief Function for initializing the SPI.
 *
 * @param[in] void
 */
int inittestapplication(void)
{
    int32_t result = 0;
    int devID; // Decawave Device ID
    decaIrqStatus_t a;

    /* Disable ScenSor (EXT_IRQ) before starting */
    a = decamutexon();
    // Set SPI clock to 2MHz
    port_set_dw1000_slowrate();
    // Read Decawave chip ID
    devID = instancereaddeviceid() ;

    if(DWT_DEVICE_ID != devID)
    {
        //wake up device from low power mode
        //NOTE - in the ARM  code just drop chip select for 200us
        port_wakeup_dw1000();
        // SPI not working or Unsupported Device ID
        devID = instancereaddeviceid() ;
        if (DWT_DEVICE_ID != devID){
            return -1 ;
        }
    }

    // configure: if DW1000 is calibrated then OTP config is used, enable sleep
    result = instance_init( 1 );

    if (0 > result) {
        return(-1) ; // Some failure has occurred
    }
    // Set SPI to 8MHz clock
    port_set_dw1000_fastrate();
    // Read Decawave chip ID
    devID = instancereaddeviceid() ;

    if (DWT_DEVICE_ID != devID)   // Means it is NOT MP device
    {
        // SPI not working or Unsupported Device ID
        return(-1);
    }

    instance_config(app.pConfig) ;  // Set operating channel etc

    decamutexoff(a); //enable ScenSor (EXT_IRQ) before starting
    return result;
}

/* @fn  wake_up_hook
 * @brief Hook function for polling if wake-up condition is occured
 *
 * @param[in] void
 * @param[out] true if MCU needs to proceed from low_power 
 */
bool wake_up_hook()
{
    if( boLIS2_InterruptOccurred() ) {
        return true;
    }
    if( deca_uart_rx_data_ready() ) {
        return true;
    }
    return false;
}


/*!
* @brief Run the accelerometer motion detection test mode.
*
* Initialise the accelerometer to detect motion and generate
* an interrupt.  Call the accelerometer foreground task, waiting
* for the interrupt to occur.
* On detecting motion turn on the blue LED, after a period of
* inactivity, turn off the LED and wait for another motion event.
*/
static void vTestModeMotionDetect(void)
{
    param_block_t *pbss = get_pbssConfig();

    /* Motion Detection Interrupt */
    static char gMotionDetInt = 0;

    if(gMotionDetInt == 1)
    {
      LEDS_ON(BSP_LED_0_MASK);
    }

    // Check for an accelerometer trigger event
    if (boLIS2_InterruptOccurred())
    {
        // now clear it
        boLIS2_InterruptClear();
        uint8_t u8Status = u8LIS2_EventStatus();

        if (u8Status & (XHIE | YHIE | ZHIE))
        {
            // Any combination of X,Y,Z motion passing
            // high threshold generates an interrupt
            LEDS_ON(BSP_LED_0_MASK);
            
            app.current_blink_interval_ms = pbss->blink.interval_in_ms;

            vLIS2_EnableInactivityDetect();
            gMotionDetInt = 1;
        }
        else // Assume low threshold (plus delay) detected
        {
            app.current_blink_interval_ms = pbss->blink.interval_slow_in_ms;

            LEDS_OFF(BSP_LED_0_MASK);
            vLIS2_EnableWakeUpDetect();
            gMotionDetInt = 0;
        }
    }
}

int main(void)
{
   
    memset(&app,0,sizeof(app));

    PEERS_peripherals_init();

    /* reset decawave */
    PEERS_reset_DW1000();

    /* set defualt PRF and bit rate etc.. */
    load_bssConfig();                 /**< load the RAM Configuration parameters from NVM block */
    app.pConfig = get_pbssConfig();

    if(PEERS_inittestapplication() < 0)
    {
        return -1; // Failed to intialze SPI.
    }

    app.firststart = 1;
    /* Enable blink */
    app.blinkenable = 1;
    app.current_blink_interval_ms = app.pConfig->blink.interval_in_ms;

    // Initialise the accelerometer
    // Note: this function blocks for 20ms.
    PEERS_vLIS2_Init();

    // Check the TWI and acceleromter are talking
    uint8_t u8ID = u8LIS2_TestRead();
    PEERS_vLIS2_PowerDown();

    // Set accelerometer activity detection level
    PEERS_vLIS2_EnableWakeUpDetect();

    PEERS_port_set_app_wakeup_check_hook(wake_up_hook);

    // No RTOS task here so just call the main loop here.
    // Loop forever responding to ranging requests.
    while(1)
    {
        // test mode is motion dection
        PEERS_vTestModeMotionDetect();
        // checking UART buffer ready to proceed
        if( PEERS_deca_uart_rx_data_ready() )
        {
            /* process UART msg based on user input. */
            PEERS_process_uartmsg();
            }
        if (app.blinkenable)
        {
            instance_run();    //< transmit packet if allowed
        }
    }
}
