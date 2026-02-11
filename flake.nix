{
  description = "Psychoanalyze";

  inputs = {
    nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0.1";
  };

  outputs = { self, nixpkgs }:
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
    in
    {
      packages.x86_64-linux = {
        default = pkgs.gcc;
      };

      devShells.x86_64-linux.default = pkgs.mkShell {
        buildInputs = [ pkgs.allure pkgs.nushell ];
        shellHook = ''exec ${pkgs.nushell}/bin/nu'';
      };

    };
}
