/*
 * blink_led.c
 *
 *  Created on: November 03, 2025
 *      Author: Nguyen Kha Duong
 *      Contact via email: duong nguyen kha.daniel@gmail.com
 */

/**********************************************************************************************************************
 * Includes
 *********************************************************************************************************************/
#include "led.h"
/**********************************************************************************************************************
 * Macro definitions
 *********************************************************************************************************************/
#define LED_TOGGLE_DEFAULT_PERIOD_MS (100U)

/**********************************************************************************************************************
 * Typedef definitions
 *********************************************************************************************************************/
/*LED internal state type */
typedef enum e_led_state {
    LED_STATE_OFF = 0U,
    LED_STATE_ON,
    LED_STATE_TOGGLE
} led_state_t;

/**********************************************************************************************************************
 * Private function prototypes
 *********************************************************************************************************************/
static void led_output_config(GPIO_TypeDef* p_port, uint16_t pin);
static void led_delay(uint32_t delay_ms);

/**********************************************************************************************************************
 * ISR prototypes
 *********************************************************************************************************************/
void LED_Timer_IRQHandler(void);

/**********************************************************************************************************************
 * Private global variables
 *********************************************************************************************************************/
static led_state_t g_led_state = LED_STATE_OFF;

/**********************************************************************************************************************
 * Global variables
 *********************************************************************************************************************/
GPIO_InitTypeDef g_led_gpio_init = {0};

/**********************************************************************************************************************
 * Function
 *********************************************************************************************************************/

/******************************************************************************************************************/ /**
 * @brief  Initialize LED GPIO.
 * @note   Configure LED pin as output push-pull.
 * @param[in]  p_port  GPIO port of LED (e.g., GPIOA)
 * @param[in]  pin     GPIO pin of LED (e.g., GPIO_PIN_5)
 *********************************************************************************************************************/
void LED_Init(GPIO_TypeDef* p_port, uint16_t pin)
{
    /* Enable corresponding GPIO clock */
    if (p_port == GPIOA) {
        __HAL_RCC_GPIOA_CLK_ENABLE();
    } else if (p_port == GPIOB) {
        __HAL_RCC_GPIOB_CLK_ENABLE();
    } else if (p_port == GPIOC) {
        __HAL_RCC_GPIOC_CLK_ENABLE();
    }

    led_output_config(p_port, pin);
    g_led_state = LED_STATE_OFF;
}

/******************************************************************************************************************/ /**
 * @brief  Turn LED on.
 * @param[in]  p_port  GPIO port of LED
 * @param[in]  pin     GPIO pin of LED
 *********************************************************************************************************************/
void LED_On(GPIO_TypeDef* p_port, uint16_t pin)
{
    HAL_GPIO_WritePin(p_port, pin, GPIO_PIN_SET);
    g_led_state = LED_STATE_ON;
}

/******************************************************************************************************************/ /**
 * @brief  Turn LED off.
 * @param[in]  p_port  GPIO port of LED
 * @param[in]  pin     GPIO pin of LED
 *********************************************************************************************************************/
void LED_Off(GPIO_TypeDef* p_port, uint16_t pin)
{
    HAL_GPIO_WritePin(p_port, pin, GPIO_PIN_RESET);
    g_led_state = LED_STATE_OFF;
}

/******************************************************************************************************************/ /**
 * @brief  Toggle LED state.
 * @param[in]  p_port  GPIO port of LED
 * @param[in]  pin     GPIO pin of LED
 *********************************************************************************************************************/
void LED_Toggle(GPIO_TypeDef* p_port, uint16_t pin)
{
    HAL_GPIO_TogglePin(p_port, pin);
    g_led_state = (g_led_state == LED_STATE_ON) ? LED_STATE_OFF : LED_STATE_ON;
}

/******************************************************************************************************************/ /**
 * @brief  Blink LED for a number of times with custom delay.
 * @param[in]  p_port     GPIO port of LED
 * @param[in]  pin        GPIO pin of LED
 * @param[in]  count      Number of times to blink
 * @param[in]  delay_ms   Delay in milliseconds between each toggle
 *********************************************************************************************************************/
void LED_Blink(GPIO_TypeDef* p_port, uint16_t pin, uint8_t count, uint32_t delay_ms)
{
    for (uint8_t i = 0; i < count; i++) {
        HAL_GPIO_TogglePin(p_port, pin);
        led_delay(delay_ms);
    }

    /* Ensure LED ends OFF */
    HAL_GPIO_WritePin(p_port, pin, GPIO_PIN_RESET);
    g_led_state = LED_STATE_OFF;
}

/**********************************************************************************************************************
 * Private Functions
 *********************************************************************************************************************/

/******************************************************************************************************************/ /**
 * @brief  Configure LED GPIO output.
 * @param[in]  p_port  GPIO port
 * @param[in]  pin     GPIO pin
 *********************************************************************************************************************/
static void led_output_config(GPIO_TypeDef* p_port, uint16_t pin)
{
    g_led_gpio_init.Pin   = pin;
    g_led_gpio_init.Mode  = GPIO_MODE_OUTPUT_PP;
    g_led_gpio_init.Pull  = GPIO_NOPULL;
    g_led_gpio_init.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(p_port, &g_led_gpio_init);
}

/******************************************************************************************************************/ /**
 * @brief  Delay helper for LED operations.
 * @param[in]  delay_ms  Delay time in milliseconds
 *********************************************************************************************************************/
static void led_delay(uint32_t delay_ms)
{
    HAL_Delay(delay_ms);
}

/******************************************************************************************************************/ /**
 * @brief  Example ISR for LED control (placeholder).
 *********************************************************************************************************************/
void LED_Timer_IRQHandler(void)
{
    /* Example ISR logic placeholder */
}