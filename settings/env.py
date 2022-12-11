from pathlib import Path

import environ


PROJECT_ROOT = Path(__file__).parent.parent.absolute()


root = environ.Path(PROJECT_ROOT)
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(root('.env'))
