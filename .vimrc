set number
set wrap linebreak

call plug#begin()
Plug 'tpope/vim-sensible'
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
Plug 'godlygeek/tabular'
Plug 'vimwiki/vimwiki'
Plug 'plasticboy/vim-markdown'
Plug 'vim-pandoc/vim-pandoc'
Plug 'ctrlpvim/ctrlp.vim'
Plug 'kyoz/purify', { 'rtp': 'vim' }

" Initialize plugin system
call plug#end()

" Set theme
syntax on 
" colorscheme purify
colorscheme zenburn

" Configure Markdown 
let g_vim_markdown_folding_disabled = 0
let g_vim_markdown_follow_anchor = 1
let g_vim_markdown_autowrite = 1
let g_vim_markdown_toc_autofit = 1
let g_vim_markdown_no_extensions_in_markdown = 1
let g_vim_markdown_edit_url_in = 'tab'
set suffixesadd=.md

" Configure vim-pandoc
let g:pandoc#filetypes#handled = ["pandoc", "markdown"]
let g:pandoc#filetypes#pandoc_markdown = 0
let g:pandoc#biblio#sources = 'c'



set conceallevel=2

let g:table_mode_corner = '|'

" Load aliases
source ~/.vim-aliases

" Center cursor (set to 0 to disable)
set scrolloff=999


" Spelling
set spell
set spelllang=en_us
set spellfile=~/.vim/spell/en.utf-8.add


" Set up Zettelkasten 
" https://www.edwinwenink.xyz/posts/48-vim_fast_creating_and_linking_notes/

let g:zettelkasten = "~/Zettelkasten/"
command! -nargs=1 NewZettel :execute ":e" zettelkasten . strftime("%Y%m%d%H%M") . "-<args>.md"
noremap <leader>nz :NewZettel

" CtrlP function for inserting a markdown link with Ctrl-X
function! CtrlPOpenFunc(action, line)
   if a:action =~ '^h$'
      " Get the filename
      let filename = fnameescape(fnamemodify(a:line, ':t'))
	  let filename_wo_timestamp = fnameescape(fnamemodify(a:line, ':t:s/\d\+-//'))

      " Close CtrlP
      call ctrlp#exit()
      call ctrlp#mrufiles#add(filename)

      " Insert the markdown link to the file in the current buffer
	  " Old .filename_wo_timestamp.
	  " OLD let mdlink = "[ ".filename." ]( ".filename." )"
          let filename_wo_escape = fnamemodify(a:line, ':t:s/\.md//')
	  let mdlink = "[[".filename_wo_escape."]]"
      put=mdlink
  else
      " Use CtrlP's default file opening function
      call call('ctrlp#acceptfile', [a:action, a:line])
   endif
endfunction

let g:ctrlp_open_func = {
         \ 'files': 'CtrlPOpenFunc',
         \ 'mru files': 'CtrlPOpenFunc'
         \ }


" make_note_link: List -> Str
" returned string: [Title](YYYYMMDDHH.md)
function! s:make_note_link(l)
        " fzf#vim#complete returns a list with all info in index 0
        let line = split(a:l[0], ':')
        let ztk_id = l:line[0]
    try
        let ztk_title = substitute(l:line[2], '\#\+\s\+', '', 'g')
catch

        let ztk_title = substitute(l:line[1], '\#\+\s\+', '', 'g')
endtry
        let mdlink = "[" . ztk_title ."](". ztk_id .")"
        return mdlink
endfunction

" mnemonic link zettel
inoremap <expr> <c-l>z fzf#vim#complete({
  \ 'source':  'rg --no-heading --smart-case  ^\#',
  \ 'reducer': function('<sid>make_note_link'),
  \ 'options': '--multi --reverse --margin 15%,0',
  \ 'up':    5})
" mnemonic link ag
inoremap <expr> <c-l>a fzf#vim#complete(fzf#vim#with_preview({
  \ 'source':  'ag --smart-case  ^\#',
  \ 'reducer': function('<sid>make_note_link'),
  \ 'options': '--multi --reverse --margin 15%,0',
  \ 'up':    5}))

" https://ibnishak.github.io/blog/post/copy-to-termux-clip/
vnoremap <C-x> :!termux-clipboard-set<CR>
vnoremap <C-c> :w !termux-clipboard-set<CR><CR>
inoremap <C-v> <ESC>:read !termux-clipboard-get<CR>i

" Passage lookup through ESV API
noremap <LEADER>p Vy:.!~/esv/passage.py <C-r>"<Cr>
vnoremap <LEADER>q :s/^/> /g<Cr>A<Cr><ESC>xi<Cr>
vnoremap <LEADER>e :s/$/  /g<Cr>A<Cr><ESC>xi<Cr>

" Number the set of lines selected using visual mode
" See https://vim.fandom.com/wiki/Insert_line_numbers
vnoremap <LEADER>n :s/^/\=printf("%02d. ", line(".") - line("'<") + 1)<Cr>

" Date string for headings
noremap <LEADER>d :.!date +"\%Y\%m\%d \%A"<Cr>0i_(<ESC>A)_<Cr><Cr>

" Accept the default spelling suggestion (#1)
noremap <LEADER>z 1z=<CR>
