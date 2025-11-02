augroup markdown_shortcuts
  autocmd!
  autocmd FileType markdown call s:markdown_mappings()
augroup END

function! s:markdown_mappings()
		" Bold: **text**
		inoremap <buffer> <C-b> ****<Left><Left>
		" Italic: *text*
		inoremap <buffer> <C-i> **<Left>
		" Inline code: `code`
		inoremap <buffer> <C-k> ``<Left>
		" Code block (triple backticks)
		inoremap <buffer> <C-l> ```<CR><CR>```<Esc>kA

		" Build on writing file
		autocmd!
		let s:project_root = expand('<sfile>:p:h')  " directory where this .vimrc/.exrc lives
		autocmd BufWritePost *.md execute '!python3 ' . shellescape(expand('<sfile>:p:h') . '/build.py')
endfunction
