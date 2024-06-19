function string.indexOf(s, pattern, init)
    init = init or 0
    local index = string.find(s, pattern, init, true)
    return index or -1;
end

function string_insert(str,index,insertStr, flag) 
    if flag and string.find(str, flag) ~=nil then
        index = index + #flag
    end
    local pre = string.sub(str, 1, index -1)
    local tail = string.sub(str, index, -1)
    local createStr = string.format("%s%s%s", pre, insertStr, tail)
	--print(createStr)
    return createStr
    end

if(tfe.get_current_stage() == "http_resp_body")
then
	local resp_body = tfe.resp.get_body_data()
	if resp_body then
		local index=string.indexOf(resp_body, "</head>")
		if index > 0 then
			local insert_resp_body=string_insert(resp_body, index,"<script type=\"text/javascript\" class=\"RQ_SCRIPT\">alert(\"ALERT\")</script>")
			if insert_resp_body then
			tfe.resp.set_body_data(insert_resp_body)
			end
		end
	end
end

