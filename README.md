# Configutor

Configutor is a tool helping you __dispatching your configurations everywhere__ without __worrying about compatibility.__

## Motivation

1. I wrote a lot of configurations, they are modulized.
2. I also work on a bunch of different machines.
3. I mainly work on my host machine, and edit configurations there quite often.
4. I want my configuration to be everywhere.
5. Some configuration are not good in some environments.
6. I don't want to edit my configuration on other machines, and take care of whether fetching those changes back to main machine.
7. I am a neovim user.

## Solution

1. For 1, A tool to aggregate those modulized configurations.
2. For 2-4 and 6, a tool to generate configurations from my main machine's configurations.
3. For 5, a tool to drop some configurations with information inside the configuration's comments.
4. Add up point 7, use a vim modline-like syntax and treesitter to parse and generate config.

## TODO

- [ ] Parse and generate `lua` configurations.
- [ ] Parse and generate `bash` configurations.
- [ ] Remove hardcoded.
- [ ] Receive command line args.
- [ ] Update python tree-sitter bindings to newest version, however compiled __fish__ parser python bindings seem __NOT TO WORK __ on newest version.


## Resources

- [Treesitter parsers collection copied from __nvim-treesitter__ repo](./grammer.md)
