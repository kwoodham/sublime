set number

set nocompatible
filetype off
set linebreak

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

Plugin 'tpope/vim-sensible'
Plugin 'godlygeek/tabular'
Plugin 'plasticboy/vim-markdown'
Plugin 'dhruvasagar/vim-table-mode'

Plugin 'alok/notational-fzf-vim'

" All of your Plugins must be added before the following line
call vundle#end()
filetype plugin indent on

let g:vim_markdown_folding_disabled = 1
let g:vim_markdown_follow_anchor = 1
let g:vim_markdown_autowrite = 1
let g:vim_markdown_toc_autofit = 1

set conceallevel=2

let g:table_mode_corner='|'

set rtp+='/usr/local/opt/fzf'

let g:nv_search_paths = ['~/zettelkasten', '~/ministry']

" Macro to link to zettel id under cursor
let @l = 'bi[[ea]]'

" Macro to open the zettel id link under the cursor
let @o = 'yaw:e "*.md'

" Macro to yank a bible reference and copy in the esv
let @r = "0Y:.!esvget.py  \"\<BS>\<CR>"

" Macro to make word **bold**
let @b = 'bi**ea**'

" Macro to make word _italics_
let @i = 'bi_ea_'
