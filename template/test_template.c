/*******************************************************************************
*
* FILE: 
*      test_$(MODULE_NAME).c
*
* DESCRIPTION: 
*      Unit tests for $(MODULE_NAME).
*
*******************************************************************************/


/*------------------------------------------------------------------------------
Standard Includes                                                                     
------------------------------------------------------------------------------*/
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
/* and any others as needed for the test */

/*------------------------------------------------------------------------------
Project Includes                                                                     
------------------------------------------------------------------------------*/
#include "sdrtf_pub.h"
#include "main.h"
/* and any others as needed for the test */

/*------------------------------------------------------------------------------
Global Variables 
------------------------------------------------------------------------------*/
/* define any globals here */


/*------------------------------------------------------------------------------
Macros
------------------------------------------------------------------------------*/
/* define any macros here */

/*------------------------------------------------------------------------------
Procedures: Test Helpers
------------------------------------------------------------------------------*/
/* define any helper functions for the test (statics) here. you can avoid 
 * defining prototypes if you do it right. */


/*------------------------------------------------------------------------------
Procedures: Tests
------------------------------------------------------------------------------*/


/*******************************************************************************
*                                                                              *
* PROCEDURE:                                                                   * 
*       test_example					                                       *
*                                                                              *
* DESCRIPTION:                                                                 * 
*       Example test case (remove when ready).								   *
*                                                                              *
*******************************************************************************/
void test_example
	(
	void
    )
{
/*------------------------------------------------------------------------------
Case 1
------------------------------------------------------------------------------*/
/* do setup here. mock returns, etc. */
int a = 3;
float b = 2.0f;
float c;

/* call function under test */
c = a * b;

/* verify results */
TEST_ASSERT_EQ_FLOAT( "Verify that the result is as expected.", c, 6.0f );

} /* test_example */


/*******************************************************************************
*                                                                              *
* PROCEDURE:                                                                   * 
*       main			                                   			           *
*                                                                              *
* DESCRIPTION:                                                                 * 
*       Set up the testing enviroment, call tests, tear down the testing       *
*		environment															   *
*                                                                              *
*******************************************************************************/
int main
	(
	void
	)
{
/*------------------------------------------------------------------------------
Test Cases
------------------------------------------------------------------------------*/
/* Do not modify */
typedef void (*test_callback)(void);
typedef struct unit_test {
	const char* test_name;
	test_callback test_pointer;
} unit_test;

/* Define test cases here */
unit_test tests[] =
	{
	{ "example_test", test_example }
	};

/* Do not modify */
FILE* outfile = fopen( "results.txt", "w" );
TEST_init( outfile, "$(MODULE_NAME)" );
for( int i = 0; i < ( sizeof(tests) / sizeof(unit_test) ); i++ )
	{
	TEST_begin_group( tests[i].test_name );
	tests[i].test_pointer();
	TEST_end_group( tests[i].test_name );
	}

exit( -1 * TEST_finalize() );

} /* main */


/*******************************************************************************
* END OF FILE                                                                  * 
*******************************************************************************/