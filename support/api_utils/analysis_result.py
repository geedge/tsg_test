class AnalysisResult():
    def analysis_result(self, condition, cfg_list, verification_result):
        if len(cfg_list) != 0:
            timeout_result = cfg_list["timeout_result"]
        else:
            timeout_result = True
        cmd_result = verification_result[0]
        log_result = verification_result[1]
        metric_result = verification_result[2]
        failure_reason = ""
        if condition["policy_type"] == "statistics" and len(verification_result) == 5:
            failure_reason = verification_result[3]
        elif condition["policy_type"] == "service_chaining":
            if cmd_result == False or log_result == False or metric_result == False:
                failure_reason = failure_reason + "The verification result of metrics is failed, the failure reason is: the metrics do not match the expectation value."
        elif condition["policy_type"] == "security" or condition["policy_type"] == "monitor" or condition["policy_type"] == "pxy_manipulation":
            if cmd_result == False and log_result == True and metric_result == True and timeout_result == True:
                failure_reason = failure_reason + "The verification result of policy effect is failed, the failure reason is: the contents returned by the command do not contain the expected value."
            elif cmd_result == False and log_result == True and metric_result == True and timeout_result == False:
                failure_reason = failure_reason + "The verification result of policy effect and creating time are failed, the failure reason is: the contents returned by the command do not contain the expected value, the creating time is over 60s"
            elif cmd_result == False and log_result == False and metric_result == True and timeout_result == True:
                failure_reason = failure_reason + "The verification results of policy effect and logs are failed, the failure reasons are: the contents returned by the command do not contain the expected value; the expected value is not queried in the logs."
            elif cmd_result == False and log_result == False and metric_result == True and timeout_result == False:
                failure_reason = failure_reason + "The verification results of policy effect, logs and creating time are failed, the failure reasons are: the contents returned by the command do not contain the expected value; the expected value is not queried in the logs, the creating time is over 60s"
            elif cmd_result == False and log_result == True and metric_result == False and timeout_result == True:
                failure_reason = failure_reason + "The verification results of policy effect and metrics are failed, the failure reasons are: the contents returned by the command did not contain the expected value; the metrics do not match the expectation value."
            elif cmd_result == False and log_result == True and metric_result == False and timeout_result == False:
                failure_reason = failure_reason + "The verification results of policy effect, metrics and creating time are failed, the failure reasons are: the contents returned by the command did not contain the expected value; the metrics do not match the expectation value, the creating time is over 60s"
            elif cmd_result == True and log_result == False and metric_result == True and timeout_result == True:
                failure_reason = failure_reason + "The verification result of logs is failed, the failure reason is: the expected value is not queried in the logs."
            elif cmd_result == True and log_result == False and metric_result == True and timeout_result == False:
                failure_reason = failure_reason + "The verification result of logs and creating time are failed, the failure reasons are: the expected value is not queried in the logs, the creating time is over 60s"
            elif cmd_result == True and log_result == True and metric_result == False and timeout_result == True:
                failure_reason = failure_reason + "The verification result of metrics is failed, the failure reason is: the metrics do not match the expectation value."
            elif cmd_result == True and log_result == True and metric_result == False and timeout_result == False:
                failure_reason = failure_reason + "The verification result of metrics and creating time are failed, the failure reasos are: the metrics do not match the expectation value, the creating time is over 60s"
            elif cmd_result == True and log_result == True and metric_result == True and timeout_result == False:
                failure_reason = failure_reason + "The verification result of creating time is failed, the failure reason is: the creating time is over 60s."
            elif cmd_result == True and log_result == False and metric_result == False and timeout_result == True:
                failure_reason = failure_reason + "The verification results of logs and metrics are failed, the failure reasons are: the expected value is not queried in the logs; the metrics do not match the expectation value."
            elif cmd_result == True and log_result == False and metric_result == False and timeout_result == False:
                failure_reason = failure_reason + "The verification results of logs, metrics and creating time are failed, the failure reasons are: the expected value is not queried in the logs; the metrics do not match the expectation value, the creating time is over 60s"
            elif cmd_result == False and log_result == False and metric_result == False and timeout_result == True:
                failure_reason = failure_reason + "The verification results of effect, logs and metrics are failed, the failure reasons are: the contents returned by the command do not contain the expected value; the expected value is not queried in the logs; the metrics do not match the expectation value."
            elif cmd_result == False and log_result == False and metric_result == False and timeout_result == False:
                failure_reason = failure_reason + "The verification results of effect, logs, metrics  and creating time are failed, the failure reasons are: the contents returned by the command do not contain the expected value; the expected value is not queried in the logs; the metrics do not match the expectation value, the creating time is over 60s"
            elif cmd_result == True and log_result == True and metric_result == None and timeout_result == False or cmd_result == True and log_result == None and metric_result == True and timeout_result == False or cmd_result == True and log_result == None and metric_result == None and timeout_result == False:
                failure_reason = failure_reason + "The verification result of creating time are failed, the failure reasos are: the creating time is over 60s"
            elif cmd_result == False and log_result == True and metric_result == None and timeout_result == True or cmd_result == False and log_result == None and metric_result == True and timeout_result == True or cmd_result == False and log_result == None and metric_result == None and timeout_result == True:
                failure_reason = failure_reason + "The verification result of policy effect is failed, the failure reason is: the contents returned by the command do not contain the expected value."
            elif cmd_result == False and log_result == True and metric_result == None and timeout_result == False or cmd_result == False and log_result == None and metric_result == True and timeout_result == False or cmd_result == False and log_result == None and metric_result == None and timeout_result == False:
                failure_reason = failure_reason + "The verification result of policy effect and creating time are failed, the failure reason is: the contents returned by the command do not contain the expected value, the creating time is over 60s"
        return failure_reason

if __name__ == "__main__":
    print("test")
