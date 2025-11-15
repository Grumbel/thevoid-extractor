{
  description = "File extractor for the game The Void";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonPackages = pkgs.python3Packages;
      in rec {
        packages = rec {
          default = thevoid-extractor;

          thevoid-extractor = pythonPackages.buildPythonPackage rec {
            name = "thevoid-extractor";
            version = "0.1.0";

            src = ./.;

            pyproject = true;
            build-system = [ pythonPackages.setuptools ];

            checkPhase = ''
              runHook preCheck
              flake8 --max-line-length 120 thevoid_extractor.py
              mypy --strict thevoid_extractor.py
              pylint thevoid_extractor.py
              runHook postCheck
            '';

            nativeCheckInputs = with pythonPackages; [
              flake8
              mypy
              pylint
              types-setuptools
              pip
            ];

            propagatedBuildInputs = with pythonPackages; [
              setuptools
            ];
          };
        };

        apps = rec {
          default = thevoid-extractor;

          thevoid-extractor = flake-utils.lib.mkApp {
            drv = packages.thevoid-extractor;
            exePath = "/bin/thevoid-extractor";
          };
        };
      }
    );
}
