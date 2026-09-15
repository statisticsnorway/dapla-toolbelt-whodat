{
  description = "Provide development environment for dapla-toolbelt-whodat";
  inputs.nixpkgs.url = "https://channels.nixos.org/nixpkgs-unstable/nixexprs.tar.zst";

  outputs = {nixpkgs, ...}: let
    systems = [
      "x86_64-linux"
      "aarch64-linux"
      "aarch64-darwin"
    ];
    forAllSystems = function:
      nixpkgs.lib.genAttrs systems (system: function nixpkgs.legacyPackages.${system});
  in {
    devShells = forAllSystems (pkgs: {
      default = pkgs.mkShell {
        name = "dapla-toolbelt-whodat devel";
        packages = with pkgs; [
          actionlint
          pre-commit
          pipx
          python313Packages.ruff
          uv
          xz
          zlib
          stdenv.cc.cc.lib
        ];
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
          pkgs.zlib
          pkgs.stdenv.cc.cc.lib
        ];
      };
    });
    formatter = forAllSystems (pkgs: pkgs.alejandra);
  };
}
