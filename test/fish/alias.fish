# EXPORT
abbr -a x chmod +x
# EXPORT
abbr -a cls clear
# EXPORT
abbr -a --set-cursor lr 'ln -s (realpath %)'
# EXPORT
abbr -a --set-cursor lns 'ln -s (realpath %)'
abbr -a shutdown "shutdown now"
abbr -a op xdg-open

if type neovide >/dev/null 2>&1
    abbr -a nv neovide
end

# EXPORT
if type trash-put >/dev/null 2>&1
    abbr -a rm trash-put
end

if type code >/dev/null 2>&1
    abbr -a coder "code -r ."
end

if type xclip >/dev/null 2>&1
    abbr -a copy "xclip -selection clipboard"
end

# EXPORT
if type rg >/dev/null 2>&1
    abbr -a grep rg
end

if type cargo >/dev/null 2>&1
    abbr -a ca cargo
end

# EXPORT: !debian
if type fd >/dev/null 2>&1
    abbr -a find fd
end

if type fssh >/dev/null 2>&1
    abbr -a ssh fssh
end

if type exercism >/dev/null 2>&1
    abbr -a sub exercism submit
end

# EXPORT
function alias
    cd "$HOME/.config/fish/conf.d/" || exit 255
    funced alias
    prevd
end


abbr -a rss $EDITOR $XDG_CONFIG_HOME/newsboat/urls

# EXPORT
abbr -a j journalctl -xe

# NOTE: alias for newsboat
if type setproxy >/dev/null 2>&1
    abbr -a newsboat 'setproxy; newsboat'
    abbr -a nb 'setproxy; newsboat'
end

if type yt-dlp >/dev/null 2>&1
    abbr -a --set-cursor yt "setproxy -p 7891
and yt-dlp '%'
and fd . . -e vtt -d 1 -x ffmpeg -i {} {.}.srt
and exec notify-send 'Download done'
"
end

# EXPORT
abbr -a fish exec fish

# EXPORT
if type gdb >/dev/null 2>&1
    abbr -a gdb gdb -q
end

# wget
abbr --set-cursor wget "setproxy
and exec wget --hsts-file=$XDG_DATA_HOME/wget-hsts '%'
"
# objdump
# EXPORT
if type objdump >/dev/null 2>&1
    abbr -a objdump objdump -Mintel -d
end

# mitm proxy
if type mitmproxy >/dev/null 2>&1
    abbr -a mitmproxy "mitmproxy --set confdir=$XDG_CONFIG_HOME/mitmproxy"
end
if type mitmweb >/dev/null 2>&1
    abbr -a mitmweb "mitmweb --set confdir=$XDG_CONFIG_HOME/mitmproxy"
end

function kali
    if not test (virsh list | rg Kali)
        virsh start Kali
        sleep 4
    end
    ssh kali
end

# EXPORT
if type proxychains >/dev/null 2>&1
  abbr -a px proxychains -q -f ~/.proxychains.conf
end


abbr --set-cursor -a ns notify-send --expire-time 0 "'%'"
