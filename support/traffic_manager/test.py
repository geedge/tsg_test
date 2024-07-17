
def test(type):
    sent_pkts = 100
    sent_bytes = 500
    received_pkts = 200
    received_bytes = 900
    
    traffic_result = {'total_packets': 175, 'total_packets_sent': 45, 'total_packets_received': 130, 'total_bytes': 180025, 'total_bytes_sent': 5799, 'total_bytes_received': 174226, 'total_syn_pkt': 1}
    if type == "raw":
        byte_value = traffic_result["total_bytes"]
        pkt_value = traffic_result["total_packets"]
        lost_pkt = 3
        lost_byte = 192
        if cfg_list["sf_method"] == "vxlan_g" and cfg_list["sf_dest_ip"] in sc_active_ip_list:
            if cfg_list["app_name_1"]:
                pkt_value -= lost_pkt
                byte_value -= lost_byte
            traffic_result["total_bytes"] = byte_value + 50 * pkt_value
            if 1000 <= pkt_value < 10000:
                pkt_value_temp = int(round(pkt_value/1000, 0))
            elif pkt_value < 1000: 
                pkt_value_temp = pkt_value
            if 1024 <= traffic_result["total_bytes"] < 1048576:
                total_bytes_temp = round(traffic_result["total_bytes"]/1024.0, 2)
            elif traffic_result["total_bytes"] < 1024:
                total_bytes_temp = traffic_result["total_bytes"]
            if cfg_list["type"] == 1:
                if sent_bytes == received_bytes == total_bytes_temp and sent_pkts == received_pkts == pkt_value_temp:
                    metric_result = True
                else:
                    metric_result = False
            elif cfg_list["type"] == 2:
                if sent_bytes == total_bytes_temp and sent_pkts == pkt_value_temp and received_bytes == received_pkts == 0:
                    metric_result = True
                else:
                    metric_result = False
            else:
                metric_result = False
        elif cfg_list["sf_method"] == "layer2_switch":
            if cfg_list["app_name_1"]:
                pkt_value -= lost_pkt
                byte_value -= lost_byte
            traffic_result["total_bytes"] = byte_value + 4 * pkt_value
            if 1000 <= pkt_value < 10000:
                pkt_value_temp = int(round(pkt_value/1000, 0))
            elif pkt_value < 1000: 
                pkt_value_temp = pkt_value
            if 1024 <= traffic_result["total_bytes"] < 1048576:
                total_bytes_temp = round(traffic_result["total_bytes"]/1024.0, 2)
            elif traffic_result["total_bytes"] < 1024:
                total_bytes_temp = traffic_result["total_bytes"]
            if cfg_list["type"] == 2:
                if sent_bytes == total_bytes_temp and sent_pkts == pkt_value_temp and received_bytes == received_pkts == 0:
                    metric_result = True
                else:
                    metric_result = False
            else:
                metric_result = False
    elif type == "decrypted":
        if cfg_list["sf_method"] == "vxlan_g" and cfg_list["sf_dest_ip"] in sc_active_ip_list:
            if cfg_list["type"] == 1:
                if sent_bytes == received_bytes and sent_pkts == received_pkts:
                    metric_result = True
                else:
                    metric_result = False
            elif cfg_list["type"] == 2:
                if sent_bytes != 0 and sent_pkts != 0 and received_bytes == received_pkts == 0:
                    metric_result = True
                else:
                    metric_result = False
            else:
                metric_result = False
        elif cfg_list["sf_method"] == "layer2_switch":
            if cfg_list["type"] == 2:
                if sent_bytes != 0 and sent_pkts != 0 and received_bytes == received_pkts == 0:
                    metric_result = True
                else:
                    metric_result = False
            else:
                metric_result = False
                        
if __name__ == '__main__':
    test()