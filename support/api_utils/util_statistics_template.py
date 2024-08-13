import inspect
from datetime import datetime, timezone


class UtilStatisticsTemplate():
    def time_dif_seconds(self, time_str1, time_str2):
        # 将字符串解析为datetime对象
        time_format = "%Y-%m-%dT%H:%M:%SZ"

        # 使用datetime.strptime解析时间字符串
        time1 = datetime.strptime(time_str1, time_format).replace(tzinfo=timezone.utc)
        time2 = datetime.strptime(time_str2, time_format).replace(tzinfo=timezone.utc)

        # 计算时间差
        time_difference = time2 - time1

        # 将时间差转换为秒
        difference_in_seconds = time_difference.total_seconds()

        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"时间差为: {difference_in_seconds}秒")
        return difference_in_seconds

    tmp_break_list = ["Client IP Object List", "Server IP Object List", "Session ID",
        "client_ip_sketch", "server_ip_sketch", "fqdn_category", "client_ip_object_list", "server_ip_object_list", "websketch_categories"]  # 兼容UI API，所以三组值

    def get_all_metrics_or_dimensions(self, type="metrics"):
        """
        type获取数据类型：
        "metrics",获取所有Metrics
        "dimensions",获取所有Dimensions
        "count_metrics",获取Count类Metrics
        "unique_count_metrics",获取Count类Metrics
        "distribution_metrics",获取Count类Metrics
        """
        all_metrics = {
            'client_ip_object_list': 'Client IP Object List',
            'server_ip_object_list': 'Server IP Object List',
            'client_ip': 'Client IP',
            'client_country': 'Client Country',
            'server_ip': 'Server IP',
            'server_country': 'Server Country',
            'client_asn': 'Client ASN',
            'server_asn': 'Server ASN',
            'server_fqdn': 'Server FQDN',
            'server_domain': 'Server Domain',
            'app': 'Application',
            'app_category': 'Application Category',
            'device_group': 'Device Group',
            'c2s_ttl': 'Client-to-Server TTL',
            's2c_ttl': 'Server-to-Client TTL',
            'c2s_link_id': 'Client-to-Server Link ID',
            's2c_link_id': 'Server-to-Client Link ID',
            'client_port': 'Client Port',
            'server_port': 'Server Port',
            'http_host': 'HTTP Host',
            'ssl_ja3_hash': 'SSL JA3 Hash',
            'ssl_sni': 'SSL SNI',
            'subscriber_id': 'Subscriber ID',
            'decoded_as': 'Decoded AS',
            'sled_ip': 'Sled IP',
            'flags': 'Flags',
            'direction': 'Direction',
            'session_id': 'Session ID',
            'in_pkt_length_distribution': 'Incoming Packet Length Distribution',
            'out_pkt_length_distribution': 'Outgoing Packet Length Distribution',
            'pkt_length_distribution': 'Packet Length Distribution',
            'in_latency_ms': 'Incoming Latency(ms)',
            'out_latency_ms': 'Outgoing Latency(ms)',
            'dtls_handshake_latency_ms': 'DTLS Handshake Latency(ms)',
            'ssl_handshake_latency_ms': 'SSL Handshake Latency(ms)',
            'tcp_handshake_latency_ms': 'TCP Handshake Latency(ms)',
            'duration_ms': 'Duration',
            'tcp_rtt_ms': 'Round-trip Time',
            'sent_bytes': 'Bytes Sent',
            'sent_pkts': 'Packets Sent',
            'received_pkts': 'Packets Received',
            'received_bytes': 'Bytes Received',
            'in_bytes': 'Incoming Bytes',
            'out_bytes': 'Outgoing Bytes',
            'in_pkts': 'Incoming Packets',
            'out_pkts': 'Outgoing Packets',
            'new_c2s_flows': 'New Client-to-Server Flows',
            'new_s2c_flows': 'New Server-to-Client Flows',
            'new_in_sessions': 'New Incoming Sessions',
            'new_out_sessions': 'New Outgoing Sessions',
            'closed_in_sessions': 'Closed Incoming Sessions',
            'closed_out_sessions': 'Closed Outgoing Sessions',
            'syn_pkts': 'SYN Packets',
            'c2s_ip_fragments': 'Client-to-Server IP Fragments',
            's2c_ip_fragments': 'Server-to-Client IP Fragments'
        }
        if type == "metrics":
            return 200, all_metrics
        elif type == "dimensions":
            return self.get_specify_elements_dict(all_metrics, 0, 27)
        elif type == "count_metrics":
            return self.get_specify_elements_dict(all_metrics, 31, (len(all_metrics) - 1))
        elif type == "unique_count_metrics":
            code,metric_tmp = self.get_specify_elements_dict(all_metrics, 0, 28)
            if code == 200:
                code, metric_tmp1 = self.get_specify_elements_dict(all_metrics, 31, (len(all_metrics) - 1))
                if code == 200:
                    for k, v in metric_tmp1.items():
                        metric_tmp[k] = v
            return code, metric_tmp
        elif type == "distribution_metrics":
            return self.get_specify_elements_dict(all_metrics, 28, (len(all_metrics) - 1))
        else:
            return 200, all_metrics


    def get_specify_elements_dict(self, dicts, start, end):
        result = {}
        try:
            # n = 28
            # p = sorted([(k, v) for k, v in dicts.items()], reverse=True)
            # s = set()
            i = 0
            for k, v in dicts.items():
                if i >= start and i < end:
                    result[k] = v
                i = i + 1
            return 200, result
        except Exception as e:
            self.error_print_function(inspect.currentframe().f_code.co_name, e)
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}")
            return 400, result
    def error_print_function(self,function,error):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Class:{self.__class__.__name__},Function:{function}Error: {error}", flush=True)
if __name__ == '__main__':
    util = UtilStatisticsTemplate()
    print("dimensions")
    print(util.get_all_metrics_or_dimensions("dimensions"))
    print("count_metrics")
    print(util.get_all_metrics_or_dimensions("count_metrics"))
    print("unique_count_metrics")
    print(util.get_all_metrics_or_dimensions("unique_count_metrics"))
    print("distribution_metrics")
    print(util.get_all_metrics_or_dimensions("distribution_metrics"))