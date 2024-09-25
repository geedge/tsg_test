--[[
	case 2
	
	在HTTP请求体阶段, 通过lua字符串操作函数gsub，将hello替换为nihao
	www.facebook.com 
--]]
if(tfe.get_current_stage() == "http_req_body")
then
	local req_body = tfe.req.get_body_data()
	if req_body then
		local replace_req_body = string.gsub(req_body, "hello", "nihao");
		tfe.req.set_body_data(replace_req_body)
	end
end
if(tfe.get_current_stage() == "http_resp_body")
then
	local resp_body = tfe.resp.get_body_data()
	if resp_body then
		local replace_resp_body = string.gsub(resp_body, "hello", "nihao");
		tfe.req.set_body_data(replace_resp_body)
	end
end