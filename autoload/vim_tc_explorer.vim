function vim_tc_explorer#encode_buffer()
  call setline(1, luaeval(
        \    'require("vim_tc_explorer").migic(unpack(_A))',
        \    [getline(1, '$'), &textwidth, '  ']))
endfunction

