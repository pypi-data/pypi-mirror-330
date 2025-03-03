#!/bin/bash

_tfa_completions() {
    local cur prev words cword
    _init_completion || return

    # Available commands
    local commands="add code list qr remove"
    
    # If we're completing the first argument or after an option
    if [[ ${cword} -eq 1 || ${prev} == --* ]]; then
        # Complete with the available commands
        COMPREPLY=($(compgen -W "${commands} --help" -- "${cur}"))
        return 0
    fi

    # Command-specific completions
    case "${words[1]}" in
        code|qr|remove)
            # All these commands need an account name
            # Get the list of available services from 'tfa list'
            local services=$(tfa list)
            COMPREPLY=($(compgen -W "${services}" -- "${cur}"))
            return 0
            ;;
        add)
            # No completion for add, as it likely requires a new account name
            return 0
            ;;
        list)
            # No additional arguments needed for list
            return 0
            ;;
    esac
}

# Register the completion function for the tfa command
complete -F _tfa_completions tfa
