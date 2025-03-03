#compdef tfa

_tfa() {
    local -a commands
    commands=(
        'add:Add a new account'
        'code:Show a TOTP code for a given account'
        'list:List all accounts'
        'qr:Display a QR code for an account'
        'remove:Remove an account'
        'completion:Generate shell completion script'
    )

    _arguments -C \
        '1: :->command' \
        '*: :->args'

    case $state in
        command)
            _describe 'command' commands
            ;;
        args)
            case ${words[2]} in
                code|qr|remove)
                    local -a accounts
                    accounts=(${(f)"$(tfa list 2>/dev/null)"})
                    _describe 'accounts' accounts
                    ;;
                completion)
                    _values 'shell' bash zsh
                    ;;
                add)
                    # No completion for the first argument (account name)
                    if [[ $CURRENT -eq 3 ]]; then
                        # No completion for account name
                        return 0
                    elif [[ $CURRENT -gt 3 ]]; then
                        # Complete options for the add command
                        _arguments \
                            '--issuer=[Specify the issuer]:issuer:' \
                            '(-f --force)'{-f,--force}'[Force overwrite if account exists]'
                    fi
                    ;;
            esac
            ;;
    esac
}

_tfa
