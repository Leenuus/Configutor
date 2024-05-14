# EXPORT
set -gx XDG_CONFIG_HOME "$HOME/.config"
# EXPORT
set -gx XDG_CACHE_HOME "$HOME/.cache"
# EXPORT
set -gx XDG_DATA_HOME "$HOME/.local/share"
# EXPORT
set -gx XDG_STATE_HOME "$HOME/.local/state"
set -gx CONFIG_DIR "$HOME/Dotfiles"

set -gx SOURCE_FISH_RC "true"

fish_add_path "$HOME/bin"
# EXPORT
fish_add_path "$HOME/.local/bin"

# rust
set -gx RUSTUP_HOME "$XDG_DATA_HOME"/rustup
set -gx CARGO_HOME "$XDG_DATA_HOME"/cargo
fish_add_path "$CARGO_HOME/bin"

# GOPATH
set -gx GOPATH "$XDG_DATA_HOME"/go

# ruby
fish_add_path "$HOME/.rvm/bin"
set -gx BUNDLE_USER_CONFIG "$XDG_CONFIG_HOME"/bundle
set -gx BUNDLE_USER_CACHE "$XDG_CACHE_HOME"/bundle
set -gx BUNDLE_USER_PLUGIN "$XDG_DATA_HOME"/bundle


# bash library
set -gx BASH_LIB "$HOME/.local/lib/bash"
