config = {
            "screenshot_config" : [
                {
                    "command" : "stbt screenshot /home/e2e/e2ehost29_local/sanityAutomation/automation_main_28/images/",
                	"defaultCommand" : "stbt screenshot"
                }
            ],

            "testcases_config" : [
            	{
            		"list_command" : "ls -tr /home/e2e/e2ehost29_local/sanityAutomation/automation_main_28"
            	}
            ],

            "createtestcase_config" : [
            	{
            		"dir_path" : "/home/e2e/e2ehost29_local/sanityAutomation/automation_main_28/"
            	}
            ],

             "deletetestcase_config" : [
            	{
            		"delete_command" : "rm -r /home/e2e/e2ehost29_local/sanityAutomation/automation_main_28/"
            	}
            ]
        }