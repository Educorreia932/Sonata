{
  lib,
  python3Packages,
}:

python3Packages.buildPythonPackage rec {
  pname = "lyricsgenius";
  version = "3.7.0";

  src = python3Packages.fetchPypi {
    inherit pname version;
    sha256 = "sha256-yvZEoiX6H5zaIEPlgauGy+i510xwtO4trOtV7yPrTP0=";
  };

  pyproject = true;
  build-system = with python3Packages; [ hatchling ];

  propagatedBuildInputs = with python3Packages; [
    beautifulsoup4
    requests
  ];

  doCheck = false;

  meta = with lib; {
    description = "Python API for the Genius.com song lyrics database";
    homepage = "https://github.com/johnwmillr/LyricsGenius";
    license = licenses.mit;
    maintainers = with maintainers; [
      educorreia932
    ];
  };
}
