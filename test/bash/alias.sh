# EXPORT
if [[ "$-" = *i* ]]; then

  alias sb="source ~/.bashrc"

  type rg >/dev/null 2>&1 && alias grep='rg'

  __platform=$(uname -a)
  if [[ "$__platform" =~ arch ]]; then
    ty fd >/dev/null 2>&1 && alias find=fd
  elif [[ "$__platform" =~ debian ]]; then
    if ty fdfind >/dev/null 2>&1; then
      alias find=fdfind
      alias fd=fdfind
    fi
  elif [[ "$__platform" =~ kali ]]; then
    if ty fdfind >/dev/null 2>&1; then
      alias find=fdfind
      alias fd=fdfind
    fi
  fi

  alias shutdown="shutdown now"

  type nvimpager >/dev/null 2>&1 && alias less='nvimpager'
fi
