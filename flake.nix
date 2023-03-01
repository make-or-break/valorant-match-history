{
  description = "valorant match history";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";

    valorant-utils = {
      url = "github:make-or-break/valorant-utils";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
    };

  };

  outputs = { self, nixpkgs, flake-utils, ... }:

    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in
      rec {

        # Use nixpkgs-fmt for `nix fmt'
        formatter = pkgs.nixpkgs-fmt;

        defaultPackage = packages.valorant-match-history;

        packages = flake-utils.lib.flattenTree rec {

          valorant-match-history = with pkgs.python3Packages;
            buildPythonPackage rec {
              pname = "valorant-match-history";
              version = "0.2.0";

              src = self;
              propagatedBuildInputs = [
                # flake inputs
                self.inputs.valorant-utils.packages.${system}.valorant-utils

                sqlalchemy
              ];

              doCheck = false;
              pythonImportsCheck = [
                "match_crawler"
              ];

              meta = with pkgs.lib; {
                description = "valorant match history";
                homepage = "https://github.com/make-or-break/valorant-match-history/";
                platforms = platforms.unix;
                maintainers = with maintainers; [ mayniklas ];
              };
            };

        };

      });
}
