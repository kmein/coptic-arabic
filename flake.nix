{
  description = "scriptalign: discover letter-level correspondences between two orthographies, with Coptic-Arabic as an example client.";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs systems;

      mkPackages = pkgs:
        let
          python = pkgs.python3;
          fs = pkgs.lib.fileset;

          # Minimal source for the library — only the files setuptools actually needs.
          scriptalignSrc = fs.toSource {
            root = ./.;
            fileset = fs.unions [
              ./pyproject.toml
              ./README.md
              ./src/scriptalign
            ];
          };

          # Minimal source for the example client.
          copticArabicSrc = fs.toSource {
            root = ./examples/coptic_arabic;
            fileset = fs.unions [
              ./examples/coptic_arabic/pyproject.toml
              ./examples/coptic_arabic/src
            ];
          };

          scriptalign = python.pkgs.buildPythonPackage {
            pname = "scriptalign";
            version = "0.1.0";
            pyproject = true;
            src = scriptalignSrc;
            build-system = with python.pkgs; [ setuptools ];
            dependencies = with python.pkgs; [ numpy ];
            # Tests live in the consuming repo, not in the library source tarball.
            doCheck = false;
          };

          coptic-arabic = python.pkgs.buildPythonApplication {
            pname = "coptic-arabic";
            version = "0.1.0";
            pyproject = true;
            src = copticArabicSrc;
            build-system = with python.pkgs; [ setuptools ];
            dependencies = [ scriptalign ];
            doCheck = false;
          };
        in {
          inherit scriptalign coptic-arabic;
          default = coptic-arabic;
        };
    in
    {
      packages = forAllSystems (system: mkPackages nixpkgs.legacyPackages.${system});

      apps = forAllSystems (system: {
        coptic-arabic = {
          type = "app";
          program = "${self.packages.${system}.coptic-arabic}/bin/coptic-arabic";
        };
        default = self.apps.${system}.coptic-arabic;
      });

      devShells = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python3;
        in {
          default = pkgs.mkShell {
            packages = [
              (python.withPackages (ps: with ps; [ numpy pytest pyperclip ]))
            ];
            shellHook = ''
              echo "scriptalign dev shell."
              echo "For editable installs run:"
              echo "  python -m venv --system-site-packages .venv"
              echo "  .venv/bin/pip install -e . -e examples/coptic_arabic"
            '';
          };
        });
    };
}
