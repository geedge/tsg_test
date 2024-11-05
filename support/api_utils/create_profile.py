#!/usr/bin/python3
# coding=utf-8
import os.path
import time
import requests
import json
import random
import string
from datetime import datetime
import copy


class CreateProfile:
    """
    创建profile接口api
    """

    def process_statistics_post_data(self, profile_statistics_template, post_statistics_data, vsys_id):
        """
        根据测试用例数据，构建post数据请求数据
        :param profile_statistics_template:    模板路径
        :param post_statistics_data:   测试用例数据
        :return:
        """
        # key-value: key为测试数据test_data中定义名称，value为statistic api中metrics_source_fields映射的查询数据
        metrics_source_fields_map = {
            "Client IP Object List": {
                "source_columns": "client_ip_object_list",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Server IP Object List": {
                "source_columns": "server_ip_object_list",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "WebSketch Categories": {
                "source_columns": "fqdn_category_list",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Client IP": {
                "source_columns": "client_ip",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Client Country": {
                "source_columns": "client_country",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Server IP": {
                "source_columns": "server_ip",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Server Country": {
                "source_columns": "server_country",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Client ASN": {
                "source_columns": "client_asn",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Server ASN": {
                "source_columns": "server_asn",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Server FQDN": {
                "source_columns": "server_fqdn",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Server Domain": {
                "source_columns": "server_domain",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Application": {
                "source_columns": "app",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Application Category": {
                "source_columns": "app_category",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Device Group": {
                "source_columns": "device_group",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Client-to-Server TTL": {
                "source_columns": "c2s_ttl",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Server-to-Client TTL": {
                "source_columns": "s2c_ttl",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Client-to-Server Link ID": {
                "source_columns": "c2s_link_id",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Server-to-Client Link ID": {
                "source_columns": "s2c_link_id",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Client Port": {
                "source_columns": "client_port",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Server Port": {
                "source_columns": "server_port",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "HTTP Host": {
                "source_columns": "http_host",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "SSL JA3 Hash": {
                "source_columns": "ssl_ja3_hash",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "SSL SNI": {
                "source_columns": "ssl_sni",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Subscriber ID": {
                "source_columns": "subscriber_id",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Decoded AS": {
                "source_columns": "decoded_as",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Sled IP": {
                "source_columns": "sled_ip",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Flags": {
                "source_columns": "flags",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Direction": {
                "source_columns": "direction",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Session ID": {
                "source_columns": "session_id",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"}]
            },
            "Incoming Packet Length Distribution": {
                "source_columns": "in_pkt_length_distribution",
                "function": [{"function": "MEDIAN", "unit": "short", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "short", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "short", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "packets", "metric_type": "distribution"}]
            },
            "Outgoing Packet Length Distribution": {
                "source_columns": "out_pkt_length_distribution",
                "function": [{"function": "MEDIAN", "unit": "short", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "short", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "short", "metric_type": "distribution"}, ]
            },
            "Packet Length Distribution": {
                "source_columns": "pkt_length_distribution",
                "function": [{"function": "MEDIAN", "unit": "short", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "short", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "short", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "packets", "metric_type": "distribution"}]
            },
            """
            "Incoming Latency(ms)": {
                "source_columns": "in_latency_ms",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "short", "metric_type": "count"},
                             {"function": "RATE", "unit": "sps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "ms", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "ms", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "ms", "metric_type": "distribution"},
                             {"function": "PERCENTILES_HDR", "unit": "ms", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "ms", "metric_type": "distribution"}]
            },
            "Outgoing Latency(ms)": {
                "source_columns": "out_latency_ms",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "short", "metric_type": "count"},
                             {"function": "RATE", "unit": "sps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "ms", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "ms", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "ms", "metric_type": "distribution"},
                             {"function": "PERCENTILES_HDR", "unit": "ms", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "ms", "metric_type": "distribution"}]
            },
            """
            "DTLS Handshake Latency(ms)": {
                "source_columns": "dtls_handshake_latency_ms",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "short", "metric_type": "count"},
                             {"function": "RATE", "unit": "sps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "ms", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "ms", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "ms", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "ms", "metric_type": "distribution"}]
            },
            "SSL Handshake Latency(ms)": {
                "source_columns": "ssl_handshake_latency_ms",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "short", "metric_type": "count"},
                             {"function": "RATE", "unit": "sps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "ms", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "ms", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "ms", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "ms", "metric_type": "distribution"}]
            },
            "TCP Handshake Latency(ms)": {
                "source_columns": "tcp_handshake_latency_ms",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "short", "metric_type": "count"},
                             {"function": "RATE", "unit": "sps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "ms", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "ms", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "ms", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "ms", "metric_type": "distribution"}]
            },
            "Duration": {
                "source_columns": "duration_ms",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "short", "metric_type": "count"},
                             {"function": "RATE", "unit": "sps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "ms", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "ms", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "ms", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "ms", "metric_type": "distribution"}]
            },
            "Round-trip Time": {
                "source_columns": "tcp_rtt_ms",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "short", "metric_type": "count"},
                             {"function": "RATE", "unit": "sps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "ms", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "ms", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "ms", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "ms", "metric_type": "distribution"}]
            },
            "Bytes Sent": {
                "source_columns": "sent_bytes",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "bytes", "metric_type": "count"},
                             {"function": "RATE", "unit": "Bps", "metric_type": "count"},
                             {"function": "BITRATE", "unit": "bps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "bytes", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "bytes", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "bytes", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "bytes", "metric_type": "distribution"}]
            },
            "Packets Sent": {
                "source_columns": "sent_pkts",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "packets", "metric_type": "count"},
                             {"function": "RATE", "unit": "pps", "metric_type": "count"},
                             {"function": "BITRATE", "unit": "bps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "packets", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "packets", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "packets", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "packets", "metric_type": "distribution"}]
            },
            "Packets Received": {
                "source_columns": "received_pkts",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "packets", "metric_type": "count"},
                             {"function": "RATE", "unit": "pps", "metric_type": "count"},
                             {"function": "BITRATE", "unit": "bps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "packets", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "packets", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "packets", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "packets", "metric_type": "distribution"}]
            },
            "Bytes Received": {
                "source_columns": "received_bytes",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "bytes", "metric_type": "count"},
                             {"function": "RATE", "unit": "Bps", "metric_type": "count"},
                             {"function": "BITRATE", "unit": "bps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "bytes", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "bytes", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "bytes", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "bytes", "metric_type": "distribution"}]
            },
            "Incoming Bytes": {
                "source_columns": "in_bytes",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "bytes", "metric_type": "count"},
                             {"function": "RATE", "unit": "Bps", "metric_type": "count"},
                             {"function": "BITRATE", "unit": "bps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "bytes", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "bytes", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "bytes", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "bytes", "metric_type": "distribution"}]
            },
            "Outgoing Bytes": {
                "source_columns": "out_bytes",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "bytes", "metric_type": "count"},
                             {"function": "RATE", "unit": "Bps", "metric_type": "count"},
                             {"function": "BITRATE", "unit": "bps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "bytes", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "bytes", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "bytes", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "bytes", "metric_type": "distribution"}]
            },
            "Incoming Packets": {
                "source_columns": "in_pkts",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "packets", "metric_type": "count"},
                             {"function": "RATE", "unit": "pps", "metric_type": "count"},
                             {"function": "BITRATE", "unit": "bps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "packets", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "packets", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "packets", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "packets", "metric_type": "distribution"}]
            },
            "Outgoing Packets": {
                "source_columns": "out_pkts",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "packets", "metric_type": "count"},
                             {"function": "RATE", "unit": "pps", "metric_type": "count"},
                             {"function": "BITRATE", "unit": "bps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "packets", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "packets", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "packets", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "packets", "metric_type": "distribution"}]
            },
            "New Client-to-Server Flows": {
                "source_columns": "new_c2s_flows",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "flows", "metric_type": "count"},
                             {"function": "RATE", "unit": "fps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "flows", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "flows", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "flows", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "flows", "metric_type": "distribution"}]
            },
            "New Server-to-Client Flows": {
                "source_columns": "new_s2c_flows",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "flows", "metric_type": "count"},
                             {"function": "RATE", "unit": "fps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "flows", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "flows", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "flows", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "flows", "metric_type": "distribution"}]
            },
            "New Sessions": {
                "source_columns": "new_for_this_rule",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "sessions", "metric_type": "count"},
                             {"function": "RATE", "unit": "sps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "sessions", "metric_type": "distribution"}]
            },
            "Closed Sessions": {
                "source_columns": "closed_for_this_rule",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "sessions", "metric_type": "count"},
                             {"function": "RATE", "unit": "sps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "sessions", "metric_type": "distribution"}]
            },
            """            
            "New Incoming Sessions": {
                "source_columns": "new_in_sessions",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "sessions", "metric_type": "count"},
                             {"function": "RATE", "unit": "sps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "sessions", "metric_type": "distribution"}]
            },
            "New Outgoing Sessions": {
                "source_columns": "new_out_sessions",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "sessions", "metric_type": "count"},
                             {"function": "RATE", "unit": "sps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "sessions", "metric_type": "distribution"}]
            },
            "Closed Incoming Sessions": {
                "source_columns": "closed_in_sessions",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "sessions", "metric_type": "count"},
                             {"function": "RATE", "unit": "sps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "sessions", "metric_type": "distribution"}]
            },
            "Closed Outgoing Sessions": {
                "source_columns": "closed_out_sessions",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "sessions", "metric_type": "count"},
                             {"function": "RATE", "unit": "sps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "sessions", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "sessions", "metric_type": "distribution"}]
            },
            "SYN Packets": {
                "source_columns": "syn_pkts",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "packets", "metric_type": "count"},
                             {"function": "RATE", "unit": "pps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "packets", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "packets", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "packets", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "packets", "metric_type": "distribution"}]
            },
            "Client-to-Server IP Fragments": {
                "source_columns": "c2s_ip_fragments",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "packets", "metric_type": "count"},
                             {"function": "RATE", "unit": "pps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "packets", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "packets", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "packets", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "packets", "metric_type": "distribution"}]
            },
            """
            "Server-to-Client IP Fragments": {
                "source_columns": "s2c_ip_fragments",
                "function": [{"function": "UNIQUE_COUNT", "unit": "short", "metric_type": "unique_count"},
                             {"function": "SUM", "unit": "packets", "metric_type": "count"},
                             {"function": "RATE", "unit": "pps", "metric_type": "count"},
                             {"function": "MEDIAN", "unit": "packets", "metric_type": "distribution"},
                             {"function": "P95_PERCENTILE", "unit": "packets", "metric_type": "distribution"},
                             {"function": "P99_PERCENTILE", "unit": "packets", "metric_type": "distribution"},
                             {"function": "HISTOGRAM", "unit": "packets", "metric_type": "distribution"}]
            },
        }
        dimensions_source_fields_map = {
            "__time": "__time",
            "Client IP Object List": "client_ip_object_list",
            "Server IP Object List": "server_ip_object_list",
            "Client IP": "client_ip",
            "Client Country": "client_country",
            "Server IP": "server_ip",
            "Server Country": "server_country",
            "Client ASN": "client_asn",
            "Server ASN": "server_asn",
            "Server FQDN": "server_fqdn",
            "Server Domain": "server_domain",
            "Application": "app",
            "Application Category": "app_category",
            "Device Group": "device_group",
            "Client-to-Server TTL": "c2s_ttl",
            "Server-to-Client TTL": "s2c_ttl",
            "Client-to-Server Link ID": "c2s_link_id",
            "Server-to-Client Link ID": "s2c_link_id",
            "Client Port": "client_port",
            "Server Port": "server_port",
            "HTTP Host": "http_host",
            "SSL JA3 Hash": "ssl_ja3_hash",
            "SSL SNI": "ssl_sni",
            "Subscriber ID": "subscriber_id",
            "Decoded AS": "decoded_as",
            "Sled IP": "sled_ip",
            "Flags": "flags",
            "Direction": "direction"
        }
        unit_map = {
            "bytes": [],
            "Bps": [],
            "bps": [],
            "flows": [],
            "fps": [],
            "sessions": [],
            "sps": [],
            "packets": [],
            "pps": [],
            "short": [],
            "ms": [],
        }
        bytes_uint = []
        metrics_source_fields_map = {k.lower(): v for k, v in metrics_source_fields_map.items()}
        dimensions_source_fields_map = {k.lower(): v for k, v in dimensions_source_fields_map.items()}  # 将key转成小写
        # 读取profile_statistics_template模板文件
        with open(profile_statistics_template, "r", encoding="utf-8") as f_template:
            f_template_dict = json.load(f_template)

        # 处理请求数据，并合并到模板数据中
        chart_template_dict = copy.deepcopy(f_template_dict["statistics_template"]["dataview"]["charts"][0])  # 单个chart模板
        f_template_dict["statistics_template"]["dataview"]["charts"].clear()

        for _ in range(len(post_statistics_data["chart_list"])):
            f_template_dict["statistics_template"]["dataview"]["charts"].append(copy.deepcopy(chart_template_dict))

        for chart_idex in range(len(post_statistics_data["chart_list"])):  # 将数据值复制到post模板中
            chart_type = post_statistics_data["chart_list"][chart_idex]["type"]
            # 重组 type
            f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["display"]["type"] = chart_type
            # 判断是否需要 table_type的数值
            if chart_type == "table":  # 需要判断drill down = drill_down  regular
                f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["display"]["table_type"] = "regular"
            else:
                f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["display"]["table_type"] = ""
            # 重组metric
            metrics_dict = copy.deepcopy(f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["metrics"][0])
            # 清空原有的list内容，在重组
            f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["metrics"].clear()
            chart_pre_name = ""
            chart_after_name = ""
            for metric_index in range(len(post_statistics_data["chart_list"][chart_idex]["metrics"])):
                source_fields_str = post_statistics_data["chart_list"][chart_idex]["metrics"][metric_index]["source_columns"].lower().strip()
                # 通过+号包含多个值
                source_fields_list_temp = source_fields_str.split("+")
                source_fields_list = list(filter(lambda x: x, source_fields_list_temp))  # 排除空元素
                label = ""
                metrics_dict["source_fields"].clear()  # 遍历添加前清空一下旧数据
                for i in range(len(source_fields_list)):
                    tmp_source = metrics_source_fields_map[source_fields_list[i]]["source_columns"]  # 通过映射，从metrics_source_fields_map取出value
                    tmp_label_source = tmp_source.replace("_", " ")
                    label = label + tmp_label_source + " "
                    metrics_dict["source_fields"].append(tmp_source)
                label = label.strip()
                function_name = post_statistics_data["chart_list"][chart_idex]["metrics"][metric_index]["function"]
                metrics_dict["function"]["name"] = function_name
                if "label" in post_statistics_data["chart_list"][chart_idex]["metrics"][metric_index].keys():
                    metrics_dict["label"] = post_statistics_data["chart_list"][chart_idex]["metrics"][metric_index]["label"]
                else:
                    metrics_dict["label"] = label
                metrics_0 = metrics_dict["source_fields"][0]
                for key, value in metrics_source_fields_map.items():
                    if value["source_columns"] == metrics_0:
                        for k in range(len(value["function"])):
                            if value["function"][k]["function"].lower() == function_name.lower():
                                unit = value["function"][k]["unit"]
                                metric_type = value["function"][k]["metric_type"]
                                # print(unit, metric_type)
                                break
                        break

                metrics_dict["unit"] = unit
                metrics_dict["metric_type"] = metric_type
                #metrics_dict["metric_name"] = "{}_{}".format(metric_type, metric_index+1)
                # 当Metrics数量超过4个时处理逻辑：每个Metric Tpye仅能有4个字段：count_1、count_2、count_3、count_4、unique_count_1、unique_count_2、unique_count_3、unique_count_4、distribution_1、distribution_2、、distribution_3、、distribution_4
                metric_index_temp = metric_index + 1
                if metric_index > 3:
                    metric_index_temp = metric_index % 4 + 1
                metrics_dict["metric_name"] = "{}_{}".format(metric_type, metric_index_temp)

                f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["metrics"].append(copy.deepcopy(metrics_dict))
                chart_pre_name = metrics_dict["source_fields"][0] + " "

            # 重组dimensions
            dimensions_dict = copy.deepcopy(f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["dimensions"][0])
            f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["dimensions"].clear()
            for dimension_index in range(len(post_statistics_data["chart_list"][chart_idex]["dimensions"])):
                source_fields_str = post_statistics_data["chart_list"][chart_idex]["dimensions"][dimension_index]["source_columns"][0].lower().strip()
                tmp_source = dimensions_source_fields_map[source_fields_str]
                dimensions_dict["source_fields"].clear()
                dimensions_dict["source_fields"].append(tmp_source)
                label = tmp_source.replace("_", " ")
                dimensions_dict["is_drilldown"] = post_statistics_data["chart_list"][chart_idex]["dimensions"][dimension_index]["is_drilldown"]
                if "__time" in tmp_source:
                    dimensions_dict["label"] = "Time"
                    dimensions_dict["function"]["name"] = "DATETIME_FLOOR_WITH_FILL"  # time维度需要有 DATETIME_FLOOR_WITH_FILL 函数
                else:
                    dimensions_dict["label"] = label  # 将_连接改为空格连接
                f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["dimensions"].append(copy.deepcopy(dimensions_dict))
                chart_after_name = dimensions_dict["source_fields"][0] + " "
            # 重组order by
            post_order_by = post_statistics_data["chart_list"][chart_idex]["order_by"]
            function_name = ""
            if post_order_by == None:
                if chart_type == "table" or chart_type == "bar":
                    f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["order_by"] = f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["metrics"][0]["label"]
                else:
                    f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["order_by"] = ""
            else:
                for _ in range(len(post_statistics_data["chart_list"][chart_idex]["metrics"])):
                    if post_statistics_data["chart_list"][chart_idex]["metrics"][_]["source_columns"].lower().strip() == post_order_by.lower().strip():
                        function_name = post_statistics_data["chart_list"][chart_idex]["metrics"][_]["function"]
                        break
                    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "order_by参数错误:{}".format(post_order_by))
                # f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["order_by"] =  "{}_{}_autoapi".format(function_name.lower(), post_order_by.lower())
                f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["order_by"] = post_order_by.strip()
            # 重组 limit、 drilldown_limit
            if "line" == chart_type:
                if len(post_statistics_data["chart_list"][chart_idex]["dimensions"]) > 1:  # 如果是Line+Dimensions图表，需要添加重组TOP参数，而无Limit参数
                    f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["series_limit"] = int(post_statistics_data["chart_list"][chart_idex]["series_limit"])
                f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["limit"] = 65536
                f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["order_by"] = ""
            elif "histogram" == chart_type:
                # 不加Limit接口报错，故此处统一对histogramChart添加limit值:'{
                #   "code" : 400,
                #   "msg" : "INVALID REQUEST:The limit cannot be empty.",
                #   "data" : null,
                #   "success" : false
                # }'
                f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["limit"] = 65536
            else:
                f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["query"]["limit"] = str(post_statistics_data["chart_list"][chart_idex]["limit"])
            # 重组threshold
            f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["threshold"]["in_bytes"] = int(post_statistics_data["chart_list"][chart_idex]["threshold"]["in_bytes"])
            f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["threshold"]["out_bytes"] = int(post_statistics_data["chart_list"][chart_idex]["threshold"]["out_bytes"])
            # 重组 chart name
            if chart_after_name == "":
                chart_name = "{}".format(chart_pre_name)
            else:
                chart_name = "{}Distributed by{}".format(chart_pre_name, chart_after_name)
            chart_name = chart_name.strip()
            f_template_dict["statistics_template"]["dataview"]["charts"][chart_idex]["name"] = chart_name

        # 重组statistics template name
        if post_statistics_data["name"] == "random_name":
            temp_list = []
            for _ in range(16):
                temp_list.append(random.choice(string.ascii_letters))
            r_letter = "".join(temp_list)
            formatted_time = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
            f_template_dict["statistics_template"]["name"] = "test_statistics_api_no{}_{}".format(r_letter, formatted_time)
        else:
            f_template_dict["statistics_template"]["name"] = post_statistics_data["name"]

        # 重组vsys id
        f_template_dict["vsys"] = vsys_id
        f_template_dict["statistics_template"]["vsys_id"] = vsys_id

        return f_template_dict

    # 生成随机的vlan_id
    def random_vlan_id(self):
        random_num = random.randint(1, 4094)
        return random_num

    # 用传入的sf数据替换模板中的数据
    def process_sf_post_data(self, sf_template_path, sf_post_data, vsys_id):
        with open(sf_template_path, "r") as f:
            sf_template_dict = json.load(f)
        sf_template_dict["vsys"] = vsys_id
        sf_template_dict["service_function"]["vsys_id"] = vsys_id
        sf_template_dict["service_function"]["name"] = sf_post_data["name"]
        sf_template_dict["service_function"]["device_group"]["tag"] = sf_post_data["device_group"]["tag"]
        sf_template_dict["service_function"]["device_group"]["value"] = sf_post_data["device_group"]["value"]
        sf_template_dict["service_function"]["connectivity"]["method"] = sf_post_data["connectivity"]["method"]
        sf_template_dict["service_function"]["admin_status"] = sf_post_data["admin_status"]
        if sf_post_data["connectivity"]["method"] == "vxlan_g":
            sf_template_dict["service_function"]["connectivity"]["dest_ip"] = sf_post_data["connectivity"]["dest_ip"]
            sf_template_dict["service_function"]["health_check"]["method"] = sf_post_data["health_check"]["method"]
            if sf_post_data["health_check"]["method"] == "bfd":
                sf_template_dict["service_function"]["health_check"]["interval_ms"] = sf_post_data["health_check"]["interval_ms"]
                sf_template_dict["service_function"]["health_check"]["retires"] = sf_post_data["health_check"]["retires"]
        else:
            sf_template_dict["service_function"]["connectivity"]["int_vlan_tag"] = self.random_vlan_id()
            sf_template_dict["service_function"]["connectivity"]["ext_vlan_tag"] = self.random_vlan_id()
            sf_template_dict["service_function"]["health_check"]["method"] = "none"
        return sf_template_dict

    # 获取sf profile id
    def get_sf_id(self, headers, sf_tempalte_path, sf_post_data, api_host, vsys_id):
        try:
            profile_type = sf_post_data['profile_type']
            if profile_type == "service_function":
                process_post_data = self.process_sf_post_data(sf_tempalte_path, sf_post_data, vsys_id)
                url = "{}/v1/profiles/service-functions".format(api_host)
                response = requests.post(url, headers=headers, json=process_post_data, verify=False)
                assert response.status_code == 200
                temp_profile_type = profile_type.replace("_", " ")
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(temp_profile_type), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile failed.".format(temp_profile_type), flush=True)
                response_dict = response.json()
                sf_profile_id = response_dict["data"]["service_function"]["uuid"]
            return sf_profile_id
        except AssertionError as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"AssertionError: {e}", flush=True)

    # 用传入的sff数据替换模板中的数据
    def process_sff_post_data(self, sf_profile_id, sff_template_path, sff_post_data, vsys_id):
        with open(sff_template_path, "r") as f:
            sff_template_dict = json.load(f)
        sff_template_dict["vsys"] = vsys_id
        sff_template_dict["service_function_forwarder"]["name"] = sff_post_data["name"]
        sff_template_dict["service_function_forwarder"]["type"] = sff_post_data["type"]
        sff_template_dict["service_function_forwarder"]["load_balance_method"] = sff_post_data["load_balance_method"]
        sff_template_dict["service_function_forwarder"]["load_balance_localization"] = sff_post_data["load_balance_localization"].lower()
        sff_template_dict["service_function_forwarder"]["failure_action"] = sff_post_data["failure_action"]
        if sff_post_data["failure_action"] == "re-dispatch":
            sff_template_dict["service_function_forwarder"]["unavailability_action"] = {}
            sff_template_dict["service_function_forwarder"]["unavailability_action"]["action"] = sff_post_data["unavailability_action"]["action"]
            if sff_post_data["unavailability_action"]["action"] == "bypass":
                sff_template_dict["service_function_forwarder"]["unavailability_action"]["health_service_func_lt"] = sff_post_data["unavailability_action"]["health_service_func_lt"]
        sff_template_dict["service_function_forwarder"]["service_func_profiles"] = sf_profile_id
        return sff_template_dict

    # 用传入的dns_record数据代替模板数据
    def process_dns_record_post_data(self, dns_record_template_path, dns_record_post_data, vsys_id):
        with open(dns_record_template_path, "r") as f:
            dns_record_template_dict = json.load(f)
        dns_record_template_dict["vsys_id"] = vsys_id
        dns_record_template_dict["dns_resource_record"]["type"] = dns_record_post_data["type"]
        dns_record_template_dict["dns_resource_record"]["values"][0]["value"] = dns_record_post_data["value"]
        return dns_record_template_dict

    # 调用创建profile的接口
    def create_profile_from_template(self, path_dict, profile_data, token, api_host, vsys_id):
        """
        创建prfile接口
        :param path_dict:  模板路径 {}
        :param post_data:     请求数据
        :param token:
        :return:   例如:{'profile_type': 'statistics_templates', 'id': 1223, 'template_info': [{'template_id': 1223, 'chart_id': 2881, 'chart_type': 'table'}, {'template_id': 1223, 'chart_id': 2883, 'chart_type': 'table'}]}
        """
        try:
            # 处理请求体数据
            headers = {"Authorization": token}
            create_profile_id_dict = {"profile_type":"", "uuid":""}
            profile_type = profile_data["profile_type"].lower()
            if profile_type == "statistics_templates":
                profile_statistics_template = path_dict["profile_statistics_template"]
                process_post_data = self.process_statistics_post_data(profile_statistics_template, profile_data, vsys_id)
                url = "{}/v1/profiles/statistics-templates".format(api_host)
                headers["Content-Type"] = "application/json"
                # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], process_post_data)
                response = requests.post(url, headers=headers, json=process_post_data, verify=False)
                # assert response.status_code == 200
                temp_profile_type = profile_type.replace("_", " ")
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(temp_profile_type), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile failed.".format(temp_profile_type), flush=True)
                response_dict = response.json()
                # 处理返回数据，提取id
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], response_dict)
                profile_id = response_dict["data"]["statistics_template"]["uuid"]
                create_profile_id_dict["profile_type"] = profile_type
                create_profile_id_dict["uuid"] = profile_id
                path_profile_type = "statistics_template"
                template_info = self.search_statistics_templates(profile_id, path_profile_type, headers, api_host, vsys_id)
                create_profile_id_dict["template_info"] = template_info
                return create_profile_id_dict
            elif profile_type == "service_function_forwarder":
                profile_sff_template = path_dict["profile_sff_template"]
                profile_sf_template = path_dict["profile_sf_template"]
                sf_profile_id_list = []
                sf_condition_values = profile_data["sf_condition"]
                for sf_profile_data in sf_condition_values:
                    sf_profile_id = self.get_sf_id(headers, profile_sf_template, sf_profile_data, api_host, vsys_id)
                    sf_profile_id_list.append(sf_profile_id)
                process_post_data = self.process_sff_post_data(sf_profile_id_list, profile_sff_template, profile_data,vsys_id)
                url = "{}/v1/profiles/service-function-forwarders".format(api_host)
                headers["Content-Type"] = "application/json"
                response = requests.post(url, headers=headers, json=process_post_data, verify=False)
                assert response.status_code == 200
                temp_profile_type = profile_type.replace("_", " ")
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(temp_profile_type), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile failed.".format(temp_profile_type), flush=True)
                response_dict = response.json()
                sff_id = response_dict["data"]["service_function_forwarder"]["uuid"]
                create_profile_id_dict["profile_type"] = profile_type
                create_profile_id_dict["uuid"] = sff_id
                sff_info = self.search_sc_sff(sff_id, headers, api_host, profile_type, vsys_id)
                create_profile_id_dict["sff_info"] = sff_info
                return create_profile_id_dict
            elif profile_type == "response_page":
                files = {"file": ("Response-Pages_1.html", open(path_dict["profiles_deny_path"], 'rb'), "text/plain")}
                del profile_data["profile_type"]
                # 添加vsys id
                profile_data["vsys"] = vsys_id
                url = "{}/v1/profiles/response-pages".format(api_host)
                response = requests.post(url=url, data=profile_data, headers=headers, files=files, verify=False)
                assert response.status_code == 200
                temp_profile_type = profile_type.replace("_", " ")
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(temp_profile_type), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile failed.".format(temp_profile_type), flush=True)
                response_dict = response.json()
                profile_id = response_dict["data"]["response_page"]["uuid"]
                create_profile_id_dict["profile_type"] = profile_type
                create_profile_id_dict["uuid"] = profile_id
                return create_profile_id_dict
            elif profile_type == "proxy_replacement_file":
                files = {"file": ("Create-Hijack-Files-test-3.html", open(path_dict["profiles_hijack_file_path"], 'rb'), "text/plain")}
                del profile_data["profile_type"]
                # 添加vsys id
                profile_data["vsys"] = vsys_id
                url = "{}/v1/profiles/proxy-replacement-files".format(api_host)
                response = requests.post(url=url, data=profile_data, headers=headers, files=files, verify=False)
                assert response.status_code == 200
                temp_profile_type = profile_type.replace("_", " ")
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(temp_profile_type), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile failed.".format(temp_profile_type), flush=True)
                response_dict = response.json()
                profile_id = response_dict["data"]["proxy_replacement_file"]["uuid"]
                create_profile_id_dict["profile_type"] = profile_type
                create_profile_id_dict["uuid"] = profile_id
                return create_profile_id_dict
            elif profile_type == "proxy_js_file":
                file_name = os.path.basename(path_dict["profiles_insert_profile_path"])
                files = {"file": (file_name, open(path_dict["profiles_insert_profile_path"], 'rb'), "text/plain")}
                del profile_data["profile_type"]
                # 添加vsys id
                profile_data["vsys"] = vsys_id
                url = "{}/v1/profiles/proxy-js-files".format(api_host)
                # url = "{}/v1/profiles/proxy-inject-scripts".format(api_host)
                response = requests.post(url=url, data=profile_data, headers=headers, files=files, verify=False)
                assert response.status_code == 200
                temp_profile_type = profile_type.replace("_", " ")
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(temp_profile_type), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile failed.".format(temp_profile_type), flush=True)
                response_dict = response.json()

                profile_id = response_dict["data"]["proxy_js_file"]["uuid"]
                create_profile_id_dict["profile_type"] = profile_type
                create_profile_id_dict["uuid"] = profile_id
                return create_profile_id_dict
            elif profile_type == "proxy_css_file":
                file_name = os.path.basename(path_dict["profiles_insert_profile_path"])
                files = {"file": (file_name, open(path_dict["profiles_insert_profile_path"], 'rb'), "text/plain")}
                del profile_data["profile_type"]
                # 添加vsys id
                profile_data["vsys"] = vsys_id
                url = "{}/v1/profiles/proxy-css-files".format(api_host)
                # url = "{}/v1/profiles/proxy-inject-scripts".format(api_host)
                response = requests.post(url=url, data=profile_data, headers=headers, files=files, verify=False)
                assert response.status_code == 200
                temp_profile_type = profile_type.replace("_", " ")
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(temp_profile_type), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile failed.".format(temp_profile_type), flush=True)
                response_dict = response.json()
                profile_id = response_dict["data"]["proxy_css_file"]["uuid"]
                create_profile_id_dict["profile_type"] = profile_type
                create_profile_id_dict["uuid"] = profile_id
                return create_profile_id_dict
            elif profile_type == "http_manipulation_script":
                files = {"file": ("run_script_hijack.lua", open(path_dict["profiles_run_script_path"], 'rb'), "text/plain")}
                del profile_data["profile_type"]
                # 添加vsys id
                profile_data["vsys"] = vsys_id
                url = "{}/v1/profiles/proxy-lua-scripts".format(api_host)
                response = requests.post(url=url, data=profile_data, headers=headers, files=files, verify=False)
                #print(response.text)
                assert response.status_code == 200
                temp_profile_type = profile_type.replace("_", " ")
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(temp_profile_type), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile failed.".format(temp_profile_type), flush=True)
                response_dict = response.json()
                profile_id = response_dict["data"]["proxy_lua_script"]["uuid"]
                create_profile_id_dict["profile_type"] = profile_type
                create_profile_id_dict["uuid"] = profile_id
                return create_profile_id_dict
            elif profile_type == "dns_record":
                profile_dns_record_template = path_dict["profile_dns_record_template"]
                # profile_data['type'] = "dns_resource_record"
                process_post_data = self.process_dns_record_post_data(profile_dns_record_template, profile_data, vsys_id)
                # 添加vsys id
                process_post_data["vsys"] = vsys_id
                url = "{}/v1/profiles/dns-resource-records".format(api_host)
                #print(json.dumps(process_post_data))
                response = requests.post(url, headers=headers, json=process_post_data, verify=False)
                assert response.status_code == 200
                temp_profile_type = profile_type.replace("_", " ")
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(temp_profile_type), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile failed.".format(temp_profile_type), flush=True)
                response_dict = response.json()
                profile_id = response_dict["data"]["dns_resource_record"]["uuid"]
                create_profile_id_dict["profile_type"] = profile_type
                create_profile_id_dict["uuid"] = profile_id
                return create_profile_id_dict
            elif profile_type == "traffic_mirror":
                # 添加vsys id
                profile_data["vsys"] = vsys_id
                del profile_data['profile_type']
                url = "{}/v1/profiles/traffic-mirroring-profiles".format(api_host, vsys_id)
                #print(json.dumps(profile_data))
                response = requests.post(url=url, json=profile_data, headers=headers, verify=False)
                #print(response.text)
                assert response.status_code == 200
                temp_profile_type = profile_type.replace("_", " ")
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(temp_profile_type), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile failed.".format(temp_profile_type), flush=True)
                response_dict = response.json()
                profile_id = response_dict["data"]["traffic_mirroring_profile"]["uuid"]
                create_profile_id_dict["profile_type"] = profile_type
                create_profile_id_dict["uuid"] = profile_id
                return create_profile_id_dict
            elif profile_type == "ssl_keyring":
                decryption_keying_type = profile_data["decryption_keying_type"]
                public_file_name = profile_data["public_file"]
                private_file_name = profile_data["private_file"]
                if decryption_keying_type == "trusted":
                    files = {
                        "public_file": (public_file_name, open(path_dict["profiles_trust_ssl_keyring_public_path"], 'rb'), "text/plain"),
                        "private_file": (private_file_name, open(path_dict["profiles_trust_ssl_keyring_private_path"], 'rb'), "text/plain"),
                    }
                else:
                    files = {
                        "public_file": (public_file_name, open(path_dict["profiles_untrust_ssl_keyring_public_path"], 'rb'), "text/plain"),
                        "private_file": (private_file_name, open(path_dict["profiles_untrust_ssl_keyring_private_path"], 'rb'), "text/plain"),
                    }
                    time.sleep(1)   # 避免两次创建时间间隔小
                del profile_data["profile_type"]
                del profile_data["decryption_keying_type"]
                del profile_data["public_file"]
                del profile_data["private_file"]
                url = "{}/v1/profiles/decryption-keyrings".format(api_host)
                response = requests.post(url=url, data=profile_data, headers=headers, files=files, verify=False)
                #print(response.text)
                assert response.status_code == 200
                temp_profile_type = profile_type.replace("_", " ")
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(temp_profile_type), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile failed.".format(temp_profile_type), flush=True)
                response_dict = response.json()
                profile_id = response_dict["data"]["ssl_keyring"]["uuid"]
                create_profile_id_dict["profile_type"] = profile_type
                create_profile_id_dict["decryption_keying_type"] = decryption_keying_type
                create_profile_id_dict["uuid"] = profile_id
                return create_profile_id_dict
            elif profile_type == "ssl_decryption":
                del profile_data["profile_type"]
                url = "{}/v1/profiles/decryption-profiles".format(api_host)
                #print(json.dumps(profile_data))
                response = requests.post(url=url, headers=headers, json=profile_data, verify=False)
                #print(response.text)
                assert response.status_code == 200
                temp_profile_type = profile_type.replace("_", " ")
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(temp_profile_type), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile failed.".format(temp_profile_type), flush=True)
                response_dict = response.json()
                profile_id = response_dict["data"]["decryption_profile"]["uuid"]
                create_profile_id_dict["profile_type"] = profile_type
                create_profile_id_dict["uuid"] = profile_id
                return create_profile_id_dict
            elif profile_type == "tcp_option":
                del profile_data["profile_type"]
                url = "{}/v1/profiles/proxy-tcp-option-profiles".format(api_host)
                #print(json.dumps(profile_data))
                response = requests.post(url=url, headers=headers, json=profile_data, verify=False)
                #print(response.text)
                assert response.status_code == 200
                temp_profile_type = profile_type.replace("_", " ")
                if response.status_code == 200:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile successfully.".format(temp_profile_type), flush=True)
                else:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Create {} profile failed.".format(temp_profile_type), flush=True)
                response_dict = response.json()
                profile_id = response_dict["data"]["proxy_tcp_option_profile"]["uuid"]
                create_profile_id_dict["profile_type"] = profile_type
                create_profile_id_dict["uuid"] = profile_id
                return create_profile_id_dict
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "to be added the other profile.")
        except AssertionError as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"AssertionError: {e}", flush=True)
            raise

    def search_statistics_templates(self, template_id, profile_type, headers, api_host, vsys_id):
        if profile_type == "statistics_template":
            api_path_profile_type = "statistics-templates"
        url = "{}/v1/profiles/{type}".format(api_host, type=api_path_profile_type)
        params_dict = {
            "vsys": vsys_id,
            "uuids": template_id
        }
        response = requests.get(url, params=params_dict, headers=headers, verify=False)
        # 打桩数据
        r_dict = response.json()
        template_info = []
        chart_info = {"template_id": template_id, "chart_id": 0, "chart_type": ""}
        for chart in r_dict["data"]["list"][0]["dataview"]["charts"]:
            chart_info["chart_type"] = chart["display"]["type"]
            chart_info["chart_id"] = chart["id"]
            chart_info["version"] = chart["version"]
            chart_info["metrics"] = []
            chart_info["dimensions"] = []
            for i in range(len(chart["query"]["dimensions"])):
                metric_name = chart["query"]["dimensions"][i]["source_fields"][0]
                label = chart["query"]["dimensions"][i]["label"]
                tmp_dict_1 = {"metric_name": metric_name, "label": label}
                chart_info["dimensions"].append(tmp_dict_1)
            for j in range(len(chart["query"]["metrics"])):
                metric_type = chart["query"]["metrics"][j]["metric_type"]
                metric_name = chart["query"]["metrics"][j]["metric_name"]
                label = chart["query"]["metrics"][j]["label"]
                function_name = chart["query"]["metrics"][j]["function"]["name"]
                tmp_dict_2 = {"function":
                                  {"name": function_name},
                              "metric_type": metric_type,
                              "metric_name": metric_name,
                              "label": label}
                chart_info["metrics"].append(tmp_dict_2)
            if "order_by" in chart["query"].keys():  # 有 order_by 则取出
                chart_info["order_by"] = chart["query"]["order_by"]
            chart_info["limit"] = chart["query"]["limit"]
            chart_info["topk"] = ""
            template_info.append(copy.deepcopy(chart_info))
        return template_info

    # 搜索sf并获取返回结果中的sf相关信息
    def search_sc_sff(self, sff_id, headers, api_host, profile_type, vsys_id):
        if profile_type == "service_function_forwarder":
            api_path_profile_type = "service-function-forwarders"
        url = "{}/v1/profiles/{type}/{ids}".format(api_host, type=api_path_profile_type, ids=sff_id)
        params_dict = {
            "vsys": vsys_id
        }
        response = requests.get(url=url, params=params_dict, headers=headers, verify=False)
        r_dict = response.json()
        sff_info = {"id": sff_id, "type": "","sf_info": []}
        if(len(r_dict["data"]["service_func_profiles"])>0):
            sf_profile_id_list = r_dict["data"]["service_func_profiles"]
            for i in sf_profile_id_list:
                sf_profile_id = i
                sff_info["sf_info"].append(self.search_sc_sf(sf_profile_id, headers, api_host,vsys_id))
            sff_info["load_balance_localization"] = r_dict["data"]["load_balance_localization"]
            sff_info["type"] = r_dict["data"]["type"]
            sff_info["failure_action"] = r_dict["data"]["failure_action"]
        return sff_info

    # 搜索sff并获取返回结果中的相关信息
    def search_sc_sf(self, sf_id, headers, api_host, vsys_id):
        url = "{}/v1/profiles/{type}/{id}".format(api_host, type="service-functions", id=sf_id)
        params_dict = {
            "vsys": vsys_id
        }
        response = requests.get(url, params=params_dict, headers=headers, verify=False)
        r_dict = response.json()
        #print(json.dumps(r_dict))
        sf_info = {"uuid": sf_id, "connectivity": {"method": ""}, "health_check": {"method": ""}}
        if r_dict["data"]["connectivity"]["method"] == "vxlan_g":
            sf_info["connectivity"]["method"] = r_dict["data"]["connectivity"]["method"]
            sf_info["connectivity"]["dest_ip"] = r_dict["data"]["connectivity"]["dest_ip"]
            sf_info["health_check"]["method"] = r_dict["data"]["health_check"]["method"]
        else:
            sf_info["connectivity"]["method"] = r_dict["data"]["connectivity"]["method"]
            sf_info["health_check"]["method"] = "none"
        sf_info["device_tag"] = r_dict["data"]["device_group"]["value"]
        sf_info["admin_status"] = r_dict["data"]["admin_status"]
        return sf_info


if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")