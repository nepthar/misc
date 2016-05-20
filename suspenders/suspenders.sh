# Suspenders: Keep your pants on
#
# Install:
# 1) Put suspenders.{py, sh} somewhere that makes sense for you
# 2) Set $suspenders_cache and $suspenders_py appropriately
# 3) Source this file
#
# Use:
# 1) susp command (see below for what it does)
# 2) Pants tab completion. Will complete available targets and goals


readonly suspenders_cache="./.cache/pants/susp"
readonly suspenders_py="${HOME}/Code/misc/suspenders/suspenders.py"
readonly suspenders_build_search_depth=2


# Remove : and @ and maybe something else. I can't remember.
export COMP_WORDBREAKS="\"'><;|&( "
complete -o bashdefault -o default -o nospace -F _complete_pants pants
complete -o bashdefault -o default -o nospace -F _complete_susp susp


_check_for_pants() { test -e ./pants; }


# All of these functions need to run after _ceck_pants
_pants_cached() {
  # Cache the output of a command in .pants.d/
  local cache_file="${suspenders_cache}/$1"
  shift 1

  mkdir -p "$suspenders_cache"

  # Update the cache if ./pants is updated
  if [[ "$cache_file" -nt ./pants ]]; then
    cat "$cache_file"
  else
    if "$@" > "$cache_file"; then
      cat $cache_file;
    else
      return 1
    fi
  fi
}

_sus_list_pants_goals() {
  while read line; do
    if [[ $line != "Installed goals:" ]]; then
      echo ${line/:*}
    fi
  done < <(./pants goals 2>/dev/null)
}

_sus_list_pants_targets() {
  local path="${1:-.}"
  local depth="${2:-$suspenders_build_search_depth}"

  for build in $(find "$path" -name 'BUILD' -maxdepth $depth); do
    echo -e "${build/\/BUILD/:}"
  done
}

_complete_pants_target() {
  local cur="$1"

  case $cur in
    *::) # Double colon - Do nothing, already complete.
      return 0;
      ;;

    *:*) # Single colon - complete targets listed in a BUILD file
      compgen -W "$($suspenders_py $cur)" -- $cur
      ;;

    *) # No colon - Generate a list of dir completions, with colons for ones that contain BUILDs
      for dircomp in $(compgen -d "$cur"); do
        echo $dircomp
        _sus_list_pants_targets "$dircomp"
      done
      ;;
  esac
  return 0
}

_complete_pants_goal() {
  compgen -W "$(_pants_cached "goals" _sus_list_pants_goals)" -- $1
}

_complete_pants() {
  local cur=${COMP_WORDS[COMP_CWORD]}

  _check_for_pants || return 124;

  case $COMP_CWORD in
    1) COMPREPLY=($(_complete_pants_goal $cur)); return 0; ;;
    2) COMPREPLY=($(_complete_pants_target $cur)); return 0; ;;
    *) return 124; ;; # Allow bash to fall back to whatever else was there.
  esac
}

_complete_susp() {
  local cur=${COMP_WORDS[COMP_CWORD]}
  local comps="flush goals targets compgen-debug"
  COMPREPLY=($(compgen -W "$comps" -- $cur))
}

susp() {
  local cmd="$1"
  shift 1

  if ! _check_for_pants; then
    echo "Not wearing any pants. (no ./pants file)"
    return 1
  fi


  case $cmd in
    flush)
      echo "Flushing $suspenders_cache"
      rm -fr "$suspenders_cache"
      ;;

    goals)
      _pants_cached "goals" _sus_list_pants_goals
      ;;

    targets) # for playing around with find depth
      _sus_list_pants_targets "$@"
      ;;

    compgen-debug)
      DEBUG=true _complete_pants_target "$@"
      ;;

    *)
      return 1
      ;;
  esac
}
