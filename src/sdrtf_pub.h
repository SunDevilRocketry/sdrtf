/*******************************************************************************
*
* FILE: 
* 		sdrtf_pub.h
*
* DESCRIPTION: 
* 		The Sun Devil Rocketry embedded test framework.
*
*******************************************************************************/


/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef USB_H
#define USB_H

#ifdef __cplusplus
extern "C" {
#endif


/*------------------------------------------------------------------------------
 Includes 
------------------------------------------------------------------------------*/
#include <stdio.h>
#include <stdbool.h>

/*------------------------------------------------------------------------------
 Macros and Globals 
------------------------------------------------------------------------------*/
#define DFLT_FLOAT_TOLERANCE 0.0001f

/* asserts */
#define TEST_ASSERT_TRUE( msg, actual ) TEST_assert( ASSERT_TYPE_EQ, msg, actual, __LINE__, __FILE__ )
#define TEST_ASSERT_FALSE( msg, actual ) TEST_assert( ASSERT_TYPE_NE, msg, actual, __LINE__, __FILE__ )

#define TEST_ASSERT_EQ_FLOAT( msg, actual, expected ) TEST_assert_float( ASSERT_TYPE_EQ, msg, actual, expected, DFLT_FLOAT_TOLERANCE, __LINE__, __FILE__ )
#define TEST_ASSERT_NE_FLOAT( msg, actual, expected ) TEST_assert_float( ASSERT_TYPE_NE, msg, actual, expected, DFLT_FLOAT_TOLERANCE, __LINE__, __FILE__ )
#define TEST_ASSERT_LT_FLOAT( msg, actual, expected ) TEST_assert_float( ASSERT_TYPE_LT, msg, actual, expected, DFLT_FLOAT_TOLERANCE, __LINE__, __FILE__ )
#define TEST_ASSERT_GT_FLOAT( msg, actual, expected ) TEST_assert_float( ASSERT_TYPE_GT, msg, actual, expected, DFLT_FLOAT_TOLERANCE, __LINE__, __FILE__ )
#define TEST_ASSERT_LE_FLOAT( msg, actual, expected ) TEST_assert_float( ASSERT_TYPE_LE, msg, actual, expected, DFLT_FLOAT_TOLERANCE, __LINE__, __FILE__ )
#define TEST_ASSERT_GE_FLOAT( msg, actual, expected ) TEST_assert_float( ASSERT_TYPE_GE, msg, actual, expected, DFLT_FLOAT_TOLERANCE, __LINE__, __FILE__ )

#define TEST_ASSERT_EQ_UINT( msg, actual, expected ) TEST_assert_uint( ASSERT_TYPE_EQ, msg, actual, expected, __LINE__, __FILE__ )
#define TEST_ASSERT_NE_UINT( msg, actual, expected ) TEST_assert_uint( ASSERT_TYPE_NE, msg, actual, expected, __LINE__, __FILE__ )
#define TEST_ASSERT_LT_UINT( msg, actual, expected ) TEST_assert_uint( ASSERT_TYPE_LT, msg, actual, expected, __LINE__, __FILE__ )
#define TEST_ASSERT_GT_UINT( msg, actual, expected ) TEST_assert_uint( ASSERT_TYPE_GT, msg, actual, expected, __LINE__, __FILE__ )
#define TEST_ASSERT_LE_UINT( msg, actual, expected ) TEST_assert_uint( ASSERT_TYPE_LE, msg, actual, expected, __LINE__, __FILE__ )
#define TEST_ASSERT_GE_UINT( msg, actual, expected ) TEST_assert_uint( ASSERT_TYPE_GE, msg, actual, expected, __LINE__, __FILE__ )

#define TEST_ASSERT_EQ_SINT( msg, actual, expected ) TEST_assert_sint( ASSERT_TYPE_EQ, msg, actual, expected, __LINE__, __FILE__ )
#define TEST_ASSERT_NE_SINT( msg, actual, expected ) TEST_assert_sint( ASSERT_TYPE_NE, msg, actual, expected, __LINE__, __FILE__ )
#define TEST_ASSERT_LT_SINT( msg, actual, expected ) TEST_assert_sint( ASSERT_TYPE_LT, msg, actual, expected, __LINE__, __FILE__ )
#define TEST_ASSERT_GT_SINT( msg, actual, expected ) TEST_assert_sint( ASSERT_TYPE_GT, msg, actual, expected, __LINE__, __FILE__ )
#define TEST_ASSERT_LE_SINT( msg, actual, expected ) TEST_assert_sint( ASSERT_TYPE_LE, msg, actual, expected, __LINE__, __FILE__ )
#define TEST_ASSERT_GE_SINT( msg, actual, expected ) TEST_assert_sint( ASSERT_TYPE_GE, msg, actual, expected, __LINE__, __FILE__ )

#define TEST_ASSERT_EQ_MEMORY( msg, actual, expected, size ) TEST_assert_memory( ASSERT_TYPE_EQ, msg, actual, expected, size, __LINE__, __FILE__ )
#define TEST_ASSERT_NE_MEMORY( msg, actual, expected, size ) TEST_assert_memory( ASSERT_TYPE_NE, msg, actual, expected, size, __LINE__, __FILE__ )
#define TEST_ASSERT_LT_MEMORY( msg, actual, expected, size ) TEST_assert_memory( ASSERT_TYPE_LT, msg, actual, expected, size, __LINE__, __FILE__ )
#define TEST_ASSERT_GT_MEMORY( msg, actual, expected, size ) TEST_assert_memory( ASSERT_TYPE_GT, msg, actual, expected, size, __LINE__, __FILE__ )
#define TEST_ASSERT_LE_MEMORY( msg, actual, expected, size ) TEST_assert_memory( ASSERT_TYPE_LE, msg, actual, expected, size, __LINE__, __FILE__ )
#define TEST_ASSERT_GE_MEMORY( msg, actual, expected, size ) TEST_assert_memory( ASSERT_TYPE_GE, msg, actual, expected, size, __LINE__, __FILE__ )

/*------------------------------------------------------------------------------
 Typdefs 
------------------------------------------------------------------------------*/
typedef enum {
    ASSERT_TYPE_EQ,
    ASSERT_TYPE_GT,
    ASSERT_TYPE_LT,
    ASSERT_TYPE_GE,
    ASSERT_TYPE_LE,
    ASSERT_TYPE_NE
} ASSERT_TYPE;

/*------------------------------------------------------------------------------
 Function Prototypes 
------------------------------------------------------------------------------*/

/* test_driver.c */
void TEST_init
    ( 
    FILE* outfile_handle_in,
    char test_name_in[32]
    );

/* test_assert.c */
void TEST_assert
    (
    ASSERT_TYPE assert_type,
    char* msg,
    bool actual,
    uint32_t line, /* pass in __LINE__ from the caller */
    const char* file /* pass in __FILE__ from the caller */
    );

void TEST_assert_float
    (
    ASSERT_TYPE assert_type,
    char* msg,
    float actual, 
    float expected,
    float tolerance,
    uint32_t line, /* pass in __LINE__ from the caller */
    const char* file /* pass in __FILE__ from the caller */
    );

void TEST_assert_uint
    (
    ASSERT_TYPE assert_type,
    char* msg,
    uint32_t actual, 
    uint32_t expected,
    uint32_t line, /* pass in __LINE__ from the caller */
    const char* file /* pass in __FILE__ from the caller */
    );

void TEST_assert_sint
    (
    ASSERT_TYPE assert_type,
    char* msg,
    int32_t actual, 
    int32_t expected,
    uint32_t line, /* pass in __LINE__ from the caller */
    const char* file /* pass in __FILE__ from the caller */
    );

void TEST_assert_memory
    (
    ASSERT_TYPE assert_type,
    char* msg,
    void* actual, 
    void* expected,
    size_t size,
    uint32_t line, /* pass in __LINE__ from the caller */
    const char* file /* pass in __FILE__ from the caller */
    );

#ifdef __cplusplus
}
#endif

#endif /* USB_H */

/*******************************************************************************
* END OF FILE                                                                  * 
*******************************************************************************/