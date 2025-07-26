from backend.model.exec_env import ExecEnv
from backend.utils.bash_utils import bash

CACHE = {}


def _get_cached(cache_key: str, command: str, force: bool) -> str:
    if not force:
        res = CACHE.get(cache_key)
        if res:
            return res
    res = bash(command=command)
    if not res:
        raise RuntimeError(f"Empty response: '{command}'")
    CACHE[cache_key] = res
    return res


def get_secret(exec_env: ExecEnv, key_name: str, force: bool = False) -> str:
    return _get_cached(
        cache_key=f"{exec_env}:{key_name}",
        command=f"az keyvault secret show "
                f"--vault-name MyVault{exec_env.value} "
                f"--name {key_name} "
                f"--query value "
                f"-o tsv",
        force=force,
    )

def get_app_config(exec_env: ExecEnv, key_name: str, force: bool = False) -> str:
    return _get_cached(
        cache_key=f"{exec_env}:{key_name}",
        command=f"az appconfig kv show "
                f"--name MyAppConfig{exec_env.value} "
                f"--key {key_name} "
                f"--query 'value' "
                f"--output tsv "
                f"--auth-mode login",
        force=force,
    )