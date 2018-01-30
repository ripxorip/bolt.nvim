if exists("b:current_syntax")
  finish
endif

syntax match commands "<Ret>"
syntax match commands "<C-q>"
syntax match commands "<C-a>"

syntax match group "+.*"
" syntax match path "-.*$"
syntax match path "$>.*$"

syntax match commands "-->.*"
highlight link group Keyword
highlight link path Debug
highlight link file Debug

let b:current_syntax = "vim_tc_explorer"

