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

    {
      nixosModules.default = self.nixosModules.valorant-match-history;
      nixosModules.valorant-match-history = { lib, pkgs, config, ... }:
        with lib;

        let cfg = config.services.valorant-match-history;
        in
        {

          options.services.valorant-match-history = {

            enable = mkEnableOption "valorant match history";

            dataDir = mkOption {
              type = types.str;
              default = "/var/lib/valorant";
              description = ''
                The directory where valorant-match-history stores it's data files. If left as the default value this directory will automatically be created before the server starts, otherwise the sysadmin is responsible for ensuring the directory exists with appropriate ownership and permissions.
              '';
            };

            user = mkOption {
              type = types.str;
              default = "valorant";
              description = "User account under which valorant services run.";
            };

            group = mkOption {
              type = types.str;
              default = "valorant";
              description = "Group under which which valorant services run.";
            };

          };

          config = mkIf cfg.enable {

            systemd.timers.valorant-match-history = {
              wantedBy = [ "timers.target" ];
              partOf = [ "valorant-match-history.service" ];
              timerConfig.OnCalendar = "*-*-* *:00:00";
            };

            systemd.services.valorant-match-history = {
              serviceConfig = mkMerge [
                {
                  User = cfg.user;
                  Group = cfg.group;
                  WorkingDirectory = cfg.dataDir;
                  Type = "oneshot";
                  ExecStart = "${self.packages."${pkgs.system}".valorant-match-history}/bin/valorant-match-history";
                }
                (mkIf (cfg.dataDir == "/var/lib/valorant") {
                  StateDirectory = "valorant";
                })
              ];
            };


            users.users = mkIf
              (cfg.user == "valorant")
              {
                valorant = {
                  isSystemUser = true;
                  group = cfg.group;
                  description = "valorant system user";
                };
              };

            users.groups =
              mkIf
                (cfg.group == "valorant")
                { valorant = { }; };

          };
          meta = { maintainers = with lib.maintainers; [ mayniklas ]; };
        };
    }

    //

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
