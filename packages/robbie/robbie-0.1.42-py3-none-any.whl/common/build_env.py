from enum import Enum
from importlib.resources import files
from common.logging_config import logger
from common.console import console

class EnvType(Enum):
    LOCAL = "local"
    DEV = "dev"
    ALPHA = "alpha"
    BETA = "beta"

class BuildEnvFile():
  """
  Plain text file that reflects which env this package was build for.
  This will drive the default values that can be overridden via config options.
  """
  value: EnvType = EnvType.DEV

  def __init__(self):
    self.value = self.get_type()

  def get_text(self) -> str:
    build_env_resource = files('common').joinpath('build_env')
    if (not build_env_resource.is_file()):
      logger.debug(f'"build_env" file not found, defaulting to "{self.value.value}"')
      return self.value.value
    try:
      contents = build_env_resource.read_text().strip()
    except Exception as e:
      logger.debug(f'Error reading build_env file: {e}, defaulting to "{self.value.value}"')
      return self.value.value
    if not contents:
      logger.debug(f'Empty build_env file, defaulting to "{self.value.value}"')
      return self.value.value
    return contents

  def get_type(self) -> EnvType:
    try:
      return EnvType(self.get_text())
    except ValueError as e:
      console.print(f"[yellow]There seems to be a problem with the build: {e}[/yellow]")
      console.print(f"[yellow]Defaulting to {self.value.value}[/yellow]")
      return self.value

build_env: EnvType = BuildEnvFile().value
"""
The type of env this package was built for.
Used when selecting default values for the package.
"""
