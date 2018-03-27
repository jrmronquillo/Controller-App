config = {
            "screenshot_config" : [
                {
                    "command" : "touch ",
                    "defaultCommand" : "touch defaultScreenshot"
             
                }
            ],

            "testcases_config" : [
            	{
            		"list_command": "ls -tr testDIR/"
            	}
            ],

            "createtestcase_config" : [
            	{
            		"dir_path" : "testDIR/"
            	}
            ], 

            "deletetestcase_config" : [
            	{
            		"delete_command" : "rm -r testDIR/"
            	}
            ]
        }