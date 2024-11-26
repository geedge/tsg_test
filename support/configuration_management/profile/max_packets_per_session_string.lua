local payload=APP.data
local payload_len=string.len(payload)

if(payload_len > 0) then
    if (APP.context.packet_sum == nil) then
        APP.context.packet_sum = 1
    else
        APP.context.packet_sum = APP.context.packet_sum + 1
    end
end

if(APP.context.packet_sum > 5 ) then
    APP.append_extra_info("key", "per session test")
end

return "test"
