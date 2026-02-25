{
  lib,
  buildPythonPackage,
  hatch,
  pytestCheckHook,
  loguru,
  pydantic,
  distutils,
}:
buildPythonPackage {
  pname = "eso";
  version = "0.1.0";
  pyproject = true;

  src = ./.;

  build-system = [
    hatch
  ];

  dependencies = [
    loguru
    pydantic
    distutils
  ];

  nativeCheckInputs = [ pytestCheckHook ];

  pythonImportsCheck = [ "eso" ];

  meta = {
    description = "";
    homepage = "https://github.com/theobori/eso";
    license = lib.licenses.mit;
  };
}
