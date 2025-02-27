from common.build_env import build_env, EnvType

def test_default_build_env():
    assert build_env == EnvType.DEV
    