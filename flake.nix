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

            propagatedBuildInputs = with pythonPackages; [
              setuptools
            ];
          };
        };
      }
    );
}
