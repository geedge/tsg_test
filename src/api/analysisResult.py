class AnalysisResult():
    def analysis_result(self, condition, cfg_list, verification_result):
        if len(cfg_list) != 0:
            timeout_result = cfg_list["timeout_result"]
        else:
            timeout_result = True
        cmd_result = verification_result[0]
        log_result = verification_result[1]
        metric_result = verification_result[2]
        if len(verification_result) == 4:
            statistics_failure_reason = verification_result[3]
        failure_reason = ""
        if condition["policyType"] == "statistics":
            failure_reason = statistics_failure_reason
        elif condition["policyType"] == "service_chaining":
            if cmd_result == False or log_result == False or metric_result == False:
                failure_reason = failure_reason + "The verification result of metrics is failed, the failure reason is: the metrics do not match the expectation value."
        elif condition["policyType"] == "tsg_security":
            if cmd_result == False and log_result == True and metric_result == True and timeout_result == True:
                failure_reason = failure_reason + "The verification result of policy effect is failed, the failure reason is: the contents returned by the command do not contain the expected value."
            elif cmd_result == False and log_result == True and metric_result == True and timeout_result == False:
                failure_reason = failure_reason + "The verification result of policy effect and create time are failed, the failure reason is: the contents returned by the command do not contain the expected value, the create time is over 60s"
            elif cmd_result == False and log_result == False and metric_result == True and timeout_result == True:
                failure_reason = failure_reason + "The verification results of policy effect and logs are failed, the failure reasons are: the contents returned by the command do not contain the expected value; the expected value is not queried in the logs."
            elif cmd_result == False and log_result == False and metric_result == True and timeout_result == False:
                failure_reason = failure_reason + "The verification results of policy effect, logs and create time are failed, the failure reasons are: the contents returned by the command do not contain the expected value; the expected value is not queried in the logs, the create time is over 60s"
            elif cmd_result == False and log_result == True and metric_result == False and timeout_result == True:
                failure_reason = failure_reason + "The verification results of policy effect and metrics are failed, the failure reasons are: the contents returned by the command did not contain the expected value; the metrics do not match the expectation value."
            elif cmd_result == False and log_result == True and metric_result == False and timeout_result == False:
                failure_reason = failure_reason + "The verification results of policy effect, metrics and create time are failed, the failure reasons are: the contents returned by the command did not contain the expected value; the metrics do not match the expectation value, the create time is over 60s"
            elif cmd_result == True and log_result == False and metric_result == True and timeout_result == True:
                failure_reason = failure_reason + "The verification result of logs is failed, the failure reason is: the expected value is not queried in the logs."
            elif cmd_result == True and log_result == False and metric_result == True and timeout_result == False:
                failure_reason = failure_reason + "The verification result of logs and create time are failed, the failure reasons are: the expected value is not queried in the logs, the create time is over 60s"
            elif cmd_result == True and log_result == True and metric_result == False and timeout_result == True:
                failure_reason = failure_reason + "The verification result of metrics is failed, the failure reason is: the metrics do not match the expectation value."
            elif cmd_result == True and log_result == True and metric_result == False and timeout_result == False:
                failure_reason = failure_reason + "The verification result of metrics and create time are failed, the failure reasos are: the metrics do not match the expectation value, the create time is over 60s"
            elif cmd_result == True and log_result == True and metric_result == True and timeout_result == False:
                failure_reason = failure_reason + "The verification result of create time is failed, the failure reason is: the create time is over 60s."
            elif cmd_result == True and log_result == False and metric_result == False and timeout_result == True:
                failure_reason = failure_reason + "The verification results of logs and metrics are failed, the failure reasons are: the expected value is not queried in the logs; the metrics do not match the expectation value."
            elif cmd_result == True and log_result == False and metric_result == False and timeout_result == False:
                failure_reason = failure_reason + "The verification results of logs, metrics and create time are failed, the failure reasons are: the expected value is not queried in the logs; the metrics do not match the expectation value, the create time is over 60s"
            elif cmd_result == False and log_result == False and metric_result == False and timeout_result == True:
                failure_reason = failure_reason + "The verification results of effect, logs and metrics are failed, the failure reasons are: the contents returned by the command do not contain the expected value; the expected value is not queried in the logs; the metrics do not match the expectation value."
            elif cmd_result == False and log_result == False and metric_result == False and timeout_result == False:
                failure_reason = failure_reason + "The verification results of effect, logs, metrics  and create time are failed, the failure reasons are: the contents returned by the command do not contain the expected value; the expected value is not queried in the logs; the metrics do not match the expectation value, the create time is over 60s"
        return failure_reason

if __name__ == "__main__":
    print("test")
