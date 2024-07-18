def extract_value(type, value):
        if type == "packets":
            if " " in value:
                value_number = int(value.split(" ")[0])
                value_unit = value.split(" ")[-1]
            else:
                value_number = int(value)
                value_unit = ""
        elif type == "bytes":
            if " " in value:
                value_unit = value.split(" ")[-1]
                if value_unit == "B":
                    value_number = int(value.split(" ")[0])
                else:
                    value_number = float(value.split(" ")[0])
            else:
                value_number = 0
                value_unit = ""
        return value_number, value_unit
    
if __name__ == "__main__":
    type = "bytes"
    value = "184.02 KB"
    extract_value(type, value)