{
  description = "File extractor for the game The Void";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonPackages = pkgs.python310Packages;
      in rec {
        packages = rec {
          default = thevoid-extractor;

          thevoid-extractor = pythonPackages.buildPythonPackage rec {
            name = "thevoid-extractor";
            version = "0.1.0";

            src = ./.;

            doCheck = true;

            checkPhase = ''
              runHook preCheck
              flake8 --max-line-length 120 thevoid_extractor.py
              mypy --strict thevoid_extractor.py
              pylint thevoid_extractor.py
              runHook postCheck
            '';

            checkInputs = with pythonPackages; [
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
      }
    );
}
