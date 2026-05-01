{
  lib,
  buildPythonPackage,
  hatch,
  pytestCheckHook,
  pydantic,
  distutils,
}:
buildPythonPackage {
  pname = "eso";
  version = "1.0.0";
  pyproject = true;

  src = ./.;

  build-system = [
    hatch
  ];

  dependencies = [
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
