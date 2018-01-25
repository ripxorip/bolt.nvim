if exists('g:vim_tc_explorer_loaded')
  finish
endif
let g:vim_tc_explorer_loaded = 1

command TcExplore :call vim_tc_explorer#encode_buffer()

