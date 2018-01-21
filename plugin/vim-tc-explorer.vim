fun! s:InitExplorer()
  :echo "Spawning new buffer"
  " Open a new split and set it up.
  split TC_Explorer
  normal! ggdG
  setlocal filetype=vim_tc_explorer
  setlocal buftype=nofile
  " Remap enter in insert mode
  inoremap <buffer> <CR> $
  " Callback to when a new character is inserted 
  " Might need to user another autocmd since InsertCharPre is using 'textlock'
  :au! InsertCharPre <buffer> :call s:ProcessChar()
  :call s:ListDirectory()
  " Set the marker to the first element in the list
  let s:marker = b:filteredDir[0]
  " Draw initial gui
  :call s:DrawGui()
  " Go to insert mode
  :startinsert
endfun

" Callback that is executed when a new 
" character is entered
fun! s:ProcessChar()
  " Lastly, make the char useless
  let v:char = ''
  " :call s:LocalDebug('jennifer')
endfun

fun! s:ListDirectory()
  " Get the current directory listing,
  " also need verification on Windows.
  let b:unfilteredDir = systemlist('ls -a')
  let b:unfilteredDir = b:unfilteredDir[2:len(b:unfilteredDir)]
  " Remove current and parent directories
  let b:filteredDir = b:unfilteredDir
endfun

fun! s:DrawGui()
  " Clear the previous frame
  normal! gg
  normal! dG
  let textList = ['==== TC explorer (alpha) ===']
  let cwd = getcwd()
  call add (textList, cwd)
  call add (textList, "-----------------------------")
  " Add the filtered list
  for f in b:filteredDir
    call add (textList, f)
  endfor
  call add (textList, "-----------------------------")
  call add (textList, "")
  call append(0, textList)
  " Set marker to the first item in the filtered list
  :normal! gg
  " Get down to the first element in the list, three down
  :normal! 3j
endfun

fun! s:LocalDebug(debugStr)
  " :stopinsert
  normal! G
  :call setline('.', 'Coconuts')
  " :call append(0, 'hej')
  " Set marker to the first item in the filtered list
  " :normal! gg
  " Get down to the first element in the list, three down
  " :normal! 3j
  " :startinsert
endfun

" Declare the commands
command! VteExplore :call s:InitExplorer()
" Maps
nnoremap å :VteExplore <CR>

