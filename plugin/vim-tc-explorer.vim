fun! HelloWorld()
  :echo "Spawning new buffer"
  " Open a new split and set it up.
  split TC_Explorer
  normal! ggdG
  setlocal filetype=vim_tc_explorer
  setlocal buftype=nofile
  " Remap enter in insert mode
  inoremap <buffer> <CR> $
  " Callback to when a new character is inserted 
  :au! InsertCharPre <buffer> :call ProcessChar()
  " Go to insert mode
  :startinsert
endfun

fun! ProcessChar()
  " Lastly, make the char useless
  let v:char = ''
  :echo v:char
endfun


" Declare the commands
command! VteExplore :call HelloWorld()
" Maps
nnoremap å :VteExplore <CR>

