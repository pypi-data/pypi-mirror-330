from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING

from pytest import mark, raises

from tests.unit import UnitTest
from vtex._config import VTEXConfig
from vtex._constants import (
    ACCOUNT_NAME_ENV_VAR,
    APP_KEY_ENV_VAR,
    APP_TOKEN_ENV_VAR,
    DEFAULT_LOG_1XX,
    DEFAULT_LOG_2XX,
    DEFAULT_LOG_3XX,
    DEFAULT_LOG_4XX,
    DEFAULT_LOG_5XX,
    DEFAULT_LOG_RETRIES,
    DEFAULT_RAISE_FOR_STATUS_CODE,
    DEFAULT_RETRY_ATTEMPTS,
    DEFAULT_RETRY_BACKOFF_MAX,
    DEFAULT_RETRY_BACKOFF_MIN,
    DEFAULT_RETRY_STATUS_CODES,
    DEFAULT_TIMEOUT,
    LOG_1XX_ENV_VAR,
    LOG_2XX_ENV_VAR,
    LOG_3XX_ENV_VAR,
    LOG_4XX_ENV_VAR,
    LOG_5XX_ENV_VAR,
    LOG_RETRIES_ENV_VAR,
    RAISE_FOR_STATUS_CODE_ENV_VAR,
    RETRY_ATTEMPTS_ENV_VAR,
    RETRY_BACKOFF_MAX_ENV_VAR,
    RETRY_BACKOFF_MIN_ENV_VAR,
    RETRY_STATUS_CODES_ENV_VAR,
    TIMEOUT_ENV_VAR,
)
from vtex._utils import str_to_bool


class TestVTEXConfig(UnitTest):
    default_account_name = "account_name"
    default_app_key = "app_key"
    default_app_token = "app_token"  # noqa: S105

    def test_no_account_name_argument_or_env_var_raises_error(self):
        with raises(ValueError):
            VTEXConfig(
                app_key=self.default_app_key,
                app_token=self.default_app_token,
            )

    @mark.parametrize("account_name", ["account_name1", "account_name2"])
    def test_valid_account_name_argument_is_set_correctly(self, account_name):
        config = VTEXConfig(
            account_name=account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.account_name == account_name

    @mark.parametrize("account_name", ["account_name1", "account_name2"])
    def test_valid_account_name_env_var_is_set_correctly(
        self,
        account_name,
        monkeypatch,
    ):
        monkeypatch.setenv(ACCOUNT_NAME_ENV_VAR, account_name)

        config = VTEXConfig(
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.account_name == account_name

    @mark.parametrize("account_name", [None, False, True, "", -0.001, 0, 0.0, 0.001, 1])
    def test_invalid_account_name_argument_raises_error(self, account_name):
        with raises(ValueError):
            VTEXConfig(
                account_name=account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
            )

    @mark.parametrize("account_name", [""])
    def test_invalid_account_name_env_var_raises_error(
        self,
        account_name,
        monkeypatch,
    ):
        monkeypatch.setenv(ACCOUNT_NAME_ENV_VAR, account_name)

        with raises(ValueError):
            VTEXConfig(
                app_key=self.default_app_key,
                app_token=self.default_app_token,
            )

    def test_no_app_key_argument_or_env_var_raises_error(self):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_token=self.default_app_token,
            )

    @mark.parametrize("app_key", ["app_key1", "app_key2"])
    def test_valid_app_key_argument_is_set_correctly(self, app_key):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=app_key,
            app_token=self.default_app_token,
        )

        assert config.app_key.get_secret_value() == app_key

    @mark.parametrize("app_key", ["app_key1", "app_key2"])
    def test_valid_app_key_env_var_is_set_correctly(self, app_key, monkeypatch):
        monkeypatch.setenv(APP_KEY_ENV_VAR, app_key)

        config = VTEXConfig(
            account_name=self.default_account_name,
            app_token=self.default_app_token,
        )

        assert config.app_key.get_secret_value() == app_key

    @mark.parametrize("app_key", [None, False, True, "", -0.001, 0, 0.0, 0.001, 1])
    def test_invalid_app_key_argument_raises_error(self, app_key):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=app_key,
                app_token=self.default_app_token,
            )

    @mark.parametrize("app_key", [""])
    def test_invalid_app_key_env_var_raises_error(self, app_key, monkeypatch):
        monkeypatch.setenv(APP_KEY_ENV_VAR, app_key)

        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_token=self.default_app_token,
            )

    def test_no_app_token_argument_or_env_var_raises_error(self):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
            )

    @mark.parametrize("app_token", ["app_token1", "app_token2"])
    def test_valid_app_token_argument_is_set_correctly(self, app_token):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=app_token,
        )

        assert config.app_token.get_secret_value() == app_token

    @mark.parametrize("app_token", ["app_token1", "app_token2"])
    def test_valid_app_token_env_var_is_set_correctly(self, app_token, monkeypatch):
        monkeypatch.setenv(APP_TOKEN_ENV_VAR, app_token)

        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
        )

        assert config.app_token.get_secret_value() == app_token

    @mark.parametrize("app_token", [None, False, True, "", -0.001, 0, 0.0, 0.001, 1])
    def test_invalid_app_token_argument_raises_error(self, app_token):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=app_token,
            )

    @mark.parametrize("app_token", [""])
    def test_invalid_app_token_env_var_raises_error(self, app_token, monkeypatch):
        monkeypatch.setenv(APP_TOKEN_ENV_VAR, app_token)

        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
            )

    def test_no_timeout_argument_or_env_var_sets_default(self):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.timeout == DEFAULT_TIMEOUT

    @mark.parametrize("timeout", [None, 0.001, 1])
    def test_valid_timeout_argument_is_set_correctly(self, timeout):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
            timeout=timeout,
        )

        assert (
            config.timeout is None
            if timeout is None
            else config.timeout == float(timeout)
        )

    @mark.parametrize("timeout", ["", "null", "0.001", "1"])
    def test_valid_timeout_env_var_is_set_correctly(self, timeout, monkeypatch):
        monkeypatch.setenv(TIMEOUT_ENV_VAR, timeout)

        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert (
            config.timeout is None
            if timeout.lower() in {"", "none", "null"}
            else config.timeout == float(timeout)
        )

    @mark.parametrize("timeout", ["test", -0.001, 0, 0.0])
    def test_invalid_timeout_argument_raises_error(self, timeout):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
                timeout=timeout,
            )

    @mark.parametrize("timeout", ["test", "-0.001", "0", "0.0"])
    def test_invalid_timeout_env_var_raises_error(self, timeout, monkeypatch):
        monkeypatch.setenv(TIMEOUT_ENV_VAR, timeout)

        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
            )

    def test_no_retry_attempts_argument_or_env_var_sets_default(self):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.retry_attempts == DEFAULT_RETRY_ATTEMPTS

    @mark.parametrize("retry_attempts", [0, 1, 2])
    def test_valid_retry_attempts_argument_is_set_correctly(self, retry_attempts):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
            retry_attempts=retry_attempts,
        )

        assert config.retry_attempts == int(retry_attempts)

    @mark.parametrize("retry_attempts", ["0", "1", "2"])
    def test_valid_retry_attempts_env_var_is_set_correctly(
        self,
        retry_attempts,
        monkeypatch,
    ):
        monkeypatch.setenv(RETRY_ATTEMPTS_ENV_VAR, retry_attempts)

        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.retry_attempts == int(retry_attempts)

    @mark.parametrize("retry_attempts", [None, "test", -1, 0.0, 1.1])
    def test_invalid_retry_attempts_argument_raises_error(self, retry_attempts):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
                retry_attempts=retry_attempts,
            )

    @mark.parametrize("retry_attempts", ["None", "test", "-1", "0.0", "1.1"])
    def test_invalid_retry_attempts_env_var_raises_error(
        self,
        retry_attempts,
        monkeypatch,
    ):
        monkeypatch.setenv(RETRY_ATTEMPTS_ENV_VAR, retry_attempts)

        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
            )

    def test_no_retry_backoff_min_argument_or_env_var_sets_default(self):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.retry_backoff_min == DEFAULT_RETRY_BACKOFF_MIN

    @mark.parametrize("retry_backoff_min", [0.001, 1, 1.1])
    def test_valid_retry_backoff_min_argument_is_set_correctly(
        self,
        retry_backoff_min,
    ):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
            retry_backoff_min=retry_backoff_min,
        )

        assert config.retry_backoff_min == float(retry_backoff_min)

    @mark.parametrize("retry_backoff_min", ["0.001", "1", "1.1"])
    def test_valid_retry_backoff_min_env_var_is_set_correctly(
        self,
        retry_backoff_min,
        monkeypatch,
    ):
        monkeypatch.setenv(RETRY_BACKOFF_MIN_ENV_VAR, retry_backoff_min)

        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.retry_backoff_min == float(retry_backoff_min)

    @mark.parametrize("retry_backoff_min", ["None", "test", -0.001, 0, 0.0])
    def test_invalid_retry_backoff_min_argument_raises_error(self, retry_backoff_min):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
                retry_backoff_min=retry_backoff_min,
            )

    @mark.parametrize("retry_backoff_min", ["None", "test", "-0.001", "0", "0.0"])
    def test_invalid_retry_backoff_min_env_var_raises_error(
        self,
        retry_backoff_min,
        monkeypatch,
    ):
        monkeypatch.setenv(RETRY_BACKOFF_MIN_ENV_VAR, retry_backoff_min)

        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
            )

    def test_no_retry_backoff_max_argument_or_env_var_sets_default(self):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.retry_backoff_max == DEFAULT_RETRY_BACKOFF_MAX

    @mark.parametrize("retry_backoff_max", [0.001, 1, 1.1])
    def test_valid_retry_backoff_max_argument_is_set_correctly(
        self,
        retry_backoff_max,
    ):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
            retry_backoff_max=retry_backoff_max,
        )

        assert config.retry_backoff_max == float(retry_backoff_max)

    @mark.parametrize("retry_backoff_max", ["0.001", "1", "1.1"])
    def test_valid_retry_backoff_max_env_var_is_set_correctly(
        self,
        retry_backoff_max,
        monkeypatch,
    ):
        monkeypatch.setenv(RETRY_BACKOFF_MAX_ENV_VAR, retry_backoff_max)

        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.retry_backoff_max == float(retry_backoff_max)

    @mark.parametrize("retry_backoff_max", ["None", "test", -0.001, 0, 0.0])
    def test_invalid_retry_backoff_max_argument_raises_error(self, retry_backoff_max):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
                retry_backoff_max=retry_backoff_max,
            )

    @mark.parametrize("retry_backoff_max", ["None", "test", "-0.001", "0", "0.0"])
    def test_invalid_retry_backoff_max_env_var_raises_error(
        self,
        retry_backoff_max,
        monkeypatch,
    ):
        monkeypatch.setenv(RETRY_BACKOFF_MAX_ENV_VAR, retry_backoff_max)

        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
            )

    def test_no_retry_status_codes_argument_or_env_var_sets_default(self):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.retry_status_codes == DEFAULT_RETRY_STATUS_CODES

    @mark.parametrize("retry_status_codes", [[], [200], [200, 400, 500]])
    def test_valid_retry_status_codes_argument_is_set_correctly(
        self,
        retry_status_codes,
    ):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
            retry_status_codes=retry_status_codes,
        )

        assert config.retry_status_codes == retry_status_codes

    @mark.parametrize("retry_status_codes", ["", "*", "200", "200,400,500"])
    def test_valid_retry_status_codes_env_var_is_set_correctly(
        self,
        retry_status_codes,
        monkeypatch,
    ):
        monkeypatch.setenv(RETRY_STATUS_CODES_ENV_VAR, retry_status_codes)

        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        if retry_status_codes == "*":
            assert config.retry_status_codes == list(range(100, 600))
        else:
            assert config.retry_status_codes == [
                int(value.strip())
                for value in retry_status_codes.split(",")
                if value.strip()
            ]

    @mark.parametrize(
        "retry_status_codes",
        ["None", "test", ["test1", "test2"], [99, 200], [200.1], [200, 600]],
    )
    def test_invalid_retry_status_codes_argument_raises_error(self, retry_status_codes):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
                retry_status_codes=retry_status_codes,
            )

    @mark.parametrize(
        "retry_status_codes",
        ["None", "test", "test1,test2", "99,200", "200.1", "200,600"],
    )
    def test_invalid_retry_status_codes_env_var_raises_error(
        self,
        retry_status_codes,
        monkeypatch,
    ):
        monkeypatch.setenv(RETRY_STATUS_CODES_ENV_VAR, retry_status_codes)

        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
            )

    def test_no_raise_for_status_argument_or_env_var_sets_default(self):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.raise_for_status_code is DEFAULT_RAISE_FOR_STATUS_CODE

    @mark.parametrize("raise_for_status_code", [True, False])
    def test_valid_raise_for_status_argument_is_set_correctly(
        self,
        raise_for_status_code,
    ):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
            raise_for_status_code=raise_for_status_code,
        )

        assert config.raise_for_status_code is raise_for_status_code

    @mark.parametrize("raise_for_status_code", ["True", "False", "y", "n", "0", "1"])
    def test_valid_raise_for_status_env_var_is_set_correctly(
        self,
        raise_for_status_code,
        monkeypatch,
    ):
        monkeypatch.setenv(RAISE_FOR_STATUS_CODE_ENV_VAR, raise_for_status_code)

        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.raise_for_status_code is str_to_bool(raise_for_status_code)

    @mark.parametrize("raise_for_status_code", [None, "test", -1, 0.0, 1.1])
    def test_invalid_raise_for_status_argument_raises_error(
        self,
        raise_for_status_code,
    ):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
                raise_for_status_code=raise_for_status_code,
            )

    @mark.parametrize("raise_for_status_code", ["None", "test", "-1", "0.0", "1.1"])
    def test_invalid_raise_for_status_env_var_raises_error(
        self,
        raise_for_status_code,
        monkeypatch,
    ):
        monkeypatch.setenv(RAISE_FOR_STATUS_CODE_ENV_VAR, raise_for_status_code)

        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
            )

    def test_no_log_retries_argument_or_env_var_sets_default(self):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.log_retries == DEFAULT_LOG_RETRIES

    @mark.parametrize("log_retries", [False, DEBUG, INFO, WARNING, ERROR, CRITICAL])
    def test_valid_log_retries_argument_is_set_correctly(self, log_retries):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
            log_retries=log_retries,
        )

        assert config.log_retries == log_retries

    @mark.parametrize("log_retries", ["False", "10", "20", "30", "40", "50"])
    def test_valid_log_retries_env_var_is_set_correctly(
        self,
        log_retries,
        monkeypatch,
    ):
        monkeypatch.setenv(LOG_RETRIES_ENV_VAR, log_retries)

        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        if log_retries == "False":
            assert config.log_retries is False
        else:
            assert config.log_retries == int(log_retries) and config.log_retries in {
                DEBUG,
                INFO,
                WARNING,
                ERROR,
                CRITICAL,
            }

    @mark.parametrize("log_retries", [None, True, "test", -1, 0.0, 1.1])
    def test_invalid_log_retries_argument_raises_error(self, log_retries):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
                log_retries=log_retries,
            )

    @mark.parametrize("log_retries", ["None", "True", "test", "-1", "0.0", "1.1"])
    def test_invalid_log_retries_env_var_raises_error(
        self,
        log_retries,
        monkeypatch,
    ):
        monkeypatch.setenv(LOG_RETRIES_ENV_VAR, log_retries)

        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
            )

    def test_no_log_1xx_argument_or_env_var_sets_default(self):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.log_1xx == DEFAULT_LOG_1XX

    @mark.parametrize("log_1xx", [False, DEBUG, INFO, WARNING, ERROR, CRITICAL])
    def test_valid_log_1xx_argument_is_set_correctly(self, log_1xx):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
            log_1xx=log_1xx,
        )

        assert config.log_1xx == log_1xx

    @mark.parametrize("log_1xx", ["False", "10", "20", "30", "40", "50"])
    def test_valid_log_1xx_env_var_is_set_correctly(
        self,
        log_1xx,
        monkeypatch,
    ):
        monkeypatch.setenv(LOG_1XX_ENV_VAR, log_1xx)

        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        if log_1xx == "False":
            assert config.log_1xx is False
        else:
            assert config.log_1xx == int(log_1xx) and config.log_1xx in {
                DEBUG,
                INFO,
                WARNING,
                ERROR,
                CRITICAL,
            }

    @mark.parametrize("log_1xx", [None, True, "test", -1, 0.0, 1.1])
    def test_invalid_log_1xx_argument_raises_error(self, log_1xx):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
                log_1xx=log_1xx,
            )

    @mark.parametrize("log_1xx", ["None", "True", "test", "-1", "0.0", "1.1"])
    def test_invalid_log_1xx_env_var_raises_error(
        self,
        log_1xx,
        monkeypatch,
    ):
        monkeypatch.setenv(LOG_1XX_ENV_VAR, log_1xx)

        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
            )

    def test_no_log_2xx_argument_or_env_var_sets_default(self):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.log_2xx == DEFAULT_LOG_2XX

    @mark.parametrize("log_2xx", [False, DEBUG, INFO, WARNING, ERROR, CRITICAL])
    def test_valid_log_2xx_argument_is_set_correctly(self, log_2xx):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
            log_2xx=log_2xx,
        )

        assert config.log_2xx == log_2xx

    @mark.parametrize("log_2xx", ["False", "10", "20", "30", "40", "50"])
    def test_valid_log_2xx_env_var_is_set_correctly(
        self,
        log_2xx,
        monkeypatch,
    ):
        monkeypatch.setenv(LOG_2XX_ENV_VAR, log_2xx)

        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        if log_2xx == "False":
            assert config.log_2xx is False
        else:
            assert config.log_2xx == int(log_2xx) and config.log_2xx in {
                DEBUG,
                INFO,
                WARNING,
                ERROR,
                CRITICAL,
            }

    @mark.parametrize("log_2xx", [None, True, "test", -1, 0.0, 1.1])
    def test_invalid_log_2xx_argument_raises_error(self, log_2xx):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
                log_2xx=log_2xx,
            )

    @mark.parametrize("log_2xx", ["None", "True", "test", "-1", "0.0", "1.1"])
    def test_invalid_log_2xx_env_var_raises_error(
        self,
        log_2xx,
        monkeypatch,
    ):
        monkeypatch.setenv(LOG_2XX_ENV_VAR, log_2xx)

        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
            )

    def test_no_log_3xx_argument_or_env_var_sets_default(self):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.log_3xx == DEFAULT_LOG_3XX

    @mark.parametrize("log_3xx", [False, DEBUG, INFO, WARNING, ERROR, CRITICAL])
    def test_valid_log_3xx_argument_is_set_correctly(self, log_3xx):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
            log_3xx=log_3xx,
        )

        assert config.log_3xx == log_3xx

    @mark.parametrize("log_3xx", ["False", "10", "20", "30", "40", "50"])
    def test_valid_log_3xx_env_var_is_set_correctly(
        self,
        log_3xx,
        monkeypatch,
    ):
        monkeypatch.setenv(LOG_3XX_ENV_VAR, log_3xx)

        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        if log_3xx == "False":
            assert config.log_3xx is False
        else:
            assert config.log_3xx == int(log_3xx) and config.log_3xx in {
                DEBUG,
                INFO,
                WARNING,
                ERROR,
                CRITICAL,
            }

    @mark.parametrize("log_3xx", [None, True, "test", -1, 0.0, 1.1])
    def test_invalid_log_3xx_argument_raises_error(self, log_3xx):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
                log_3xx=log_3xx,
            )

    @mark.parametrize("log_3xx", ["None", "True", "test", "-1", "0.0", "1.1"])
    def test_invalid_log_3xx_env_var_raises_error(
        self,
        log_3xx,
        monkeypatch,
    ):
        monkeypatch.setenv(LOG_3XX_ENV_VAR, log_3xx)

        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
            )

    def test_no_log_4xx_argument_or_env_var_sets_default(self):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.log_4xx == DEFAULT_LOG_4XX

    @mark.parametrize("log_4xx", [False, DEBUG, INFO, WARNING, ERROR, CRITICAL])
    def test_valid_log_4xx_argument_is_set_correctly(self, log_4xx):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
            log_4xx=log_4xx,
        )

        assert config.log_4xx == log_4xx

    @mark.parametrize("log_4xx", ["False", "10", "20", "30", "40", "50"])
    def test_valid_log_4xx_env_var_is_set_correctly(
        self,
        log_4xx,
        monkeypatch,
    ):
        monkeypatch.setenv(LOG_4XX_ENV_VAR, log_4xx)

        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        if log_4xx == "False":
            assert config.log_4xx is False
        else:
            assert config.log_4xx == int(log_4xx) and config.log_4xx in {
                DEBUG,
                INFO,
                WARNING,
                ERROR,
                CRITICAL,
            }

    @mark.parametrize("log_4xx", [None, True, "test", -1, 0.0, 1.1])
    def test_invalid_log_4xx_argument_raises_error(self, log_4xx):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
                log_4xx=log_4xx,
            )

    @mark.parametrize("log_4xx", ["None", "True", "test", "-1", "0.0", "1.1"])
    def test_invalid_log_4xx_env_var_raises_error(
        self,
        log_4xx,
        monkeypatch,
    ):
        monkeypatch.setenv(LOG_4XX_ENV_VAR, log_4xx)

        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
            )

    def test_no_log_5xx_argument_or_env_var_sets_default(self):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        assert config.log_5xx == DEFAULT_LOG_5XX

    @mark.parametrize("log_5xx", [False, DEBUG, INFO, WARNING, ERROR, CRITICAL])
    def test_valid_log_5xx_argument_is_set_correctly(self, log_5xx):
        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
            log_5xx=log_5xx,
        )

        assert config.log_5xx == log_5xx

    @mark.parametrize("log_5xx", ["False", "10", "20", "30", "40", "50"])
    def test_valid_log_5xx_env_var_is_set_correctly(
        self,
        log_5xx,
        monkeypatch,
    ):
        monkeypatch.setenv(LOG_5XX_ENV_VAR, log_5xx)

        config = VTEXConfig(
            account_name=self.default_account_name,
            app_key=self.default_app_key,
            app_token=self.default_app_token,
        )

        if log_5xx == "False":
            assert config.log_5xx is False
        else:
            assert config.log_5xx == int(log_5xx) and config.log_5xx in {
                DEBUG,
                INFO,
                WARNING,
                ERROR,
                CRITICAL,
            }

    @mark.parametrize("log_5xx", [None, True, "test", -1, 0.0, 1.1])
    def test_invalid_log_5xx_argument_raises_error(self, log_5xx):
        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
                log_5xx=log_5xx,
            )

    @mark.parametrize("log_5xx", ["None", "True", "test", "-1", "0.0", "1.1"])
    def test_invalid_log_5xx_env_var_raises_error(
        self,
        log_5xx,
        monkeypatch,
    ):
        monkeypatch.setenv(LOG_5XX_ENV_VAR, log_5xx)

        with raises(ValueError):
            VTEXConfig(
                account_name=self.default_account_name,
                app_key=self.default_app_key,
                app_token=self.default_app_token,
            )
