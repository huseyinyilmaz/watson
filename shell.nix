{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  # this will make all the build inputs from hello and gnutar
  # available to the shell environment
  # inputsFrom = with pkgs; [ hello ];
  buildInputs = [ pkgs.python37Full ];
  # shellHook = ''
  # echo "Shell is created"
  # '';
}
# pkgs.mkShell {
#   # buildInputs = [
#   #   pkgs.fortune
#   # ];

#   shellHook = ''
#     echo "execute any bash commands when activating shell";
#   '';
# }
