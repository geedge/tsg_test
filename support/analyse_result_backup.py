from datetime import datetime 
class Analyse:
    def analyse_result(self, rule_type, verification_result):
        cmd_result = verification_result[0]
        log_result = verification_result[0]
        if rule_type == "statistics":
            metric_result = verification_result[0]
        else:
            metric_result = verification_result[1]
        fail_reason_template = "The verification result of policy effect is failed, the failure reasons are: "
        failure_reason = ""
        if rule_type == "statistics":
            failure_reason = verification_result[1]
        elif rule_type == "service_chaining":
            if cmd_result == False:
                failure_reason = failure_reason + "the metrics do not match the expectant value,"
            if log_result == False:
                failure_reason = failure_reason + "the expected value is not matched with queried values in the logs,"
            if metric_result == False:
                failure_reason = failure_reason + "the expected value is not matched with values of rule detail page,"
            if len(failure_reason) != 0:
                failure_reason = fail_reason_template + failure_reason
                # 把最后一个逗号改成句号
                failure_reason = failure_reason[:failure_reason.rindex(',')] + '.' + failure_reason[failure_reason.rindex(',')+1:]
        elif rule_type == "security" or rule_type == "monitor" or rule_type == "pxy_manipulation" or rule_type == "dos_protection":
            if cmd_result == False:
                failure_reason = failure_reason + "the contents returned by the command do not contain the expected value, "
            if metric_result == False:
                failure_reason = failure_reason + "the metrics do not match the expectation value, "
            if metric_result == None:
                failure_reason = failure_reason + "the metrics query result is empty, "
            if log_result == False:
                failure_reason = failure_reason + "the expected value is not queried in the logs, "
            if log_result == None:
                failure_reason = failure_reason + "the log query result is empty, "
            if len(failure_reason) != 0:
                failure_reason = fail_reason_template + failure_reason
                # 把最后一个逗号改成句号
                failure_reason = failure_reason[:failure_reason.rindex(',')] + '.' + failure_reason[failure_reason.rindex(',')+1:]
        return failure_reason

if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
