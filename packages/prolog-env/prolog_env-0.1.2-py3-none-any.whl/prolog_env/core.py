import re
import tempfile
import traceback
import subprocess
import gymnasium as gym
from gymnasium.spaces import Text
import janus_swi as janus

DEFAULT_CONFIG = {
    "max_input_output_len": 32000,    # longest length of the code
    "exception_reward": -9
}
TEST_FAIL_PATTERN = r"ERROR:\s*(\d+)\s*test failed\s*\n%\s*(\d+)\s*tests passed"

class SimpleEvaluator(gym.Env):
    def __init__(self, config=DEFAULT_CONFIG):
        self.action_space = Text(config["max_input_output_len"])
        self.exception_reward = config["exception_reward"]
        assert self.exception_reward < 0, "Exception reward must be negative"
        self.observation_space = self.action_space
        self.reward = 0

    def reset(self, *, seed=None, options=None):
        """
        Resets the environment.

        Returns:
            tuple: A tuple containing the initial observation (empty string) and an info dictionary
                   with the key "env_state" set to "reset".
        """
        self.reward = 0
        return "", {"env_state": "reset"}

    def step(self, code, query:str=None,test:str=None):
        observation = "OK"
        reward = 0
        try:
            janus.consult("trains", code)
            if query:
                observation = str(list(janus.query(query)))
                reward = -self.exception_reward
            if test:
                assert test.startswith(":- begin_tests"), "Test format is not correct, it should begin with ':- begin_tests'"
                assert test.endswith(":- end_tests"), "Test format is not correct, it should end with ':- end_tests'"
                with tempfile.NamedTemporaryFile(mode='w', suffix='.pl') as tmp_file:
                    tmp_file_name = tmp_file.name
                    tmp_file.write(test)
                    tmp_file.seek(0)
                    result = subprocess.run(
                        ["swipl", "-g", "run_tests", "-t", "halt", tmp_file_name],
                        capture_output=True, text=True)
                    observation = f"## stdout:\n{result.stdout}\n\n"
                    observation += f"## stderr:\n{result.stderr}"
                match = re.search(TEST_FAIL_PATTERN,
                                  observation,
                                  re.MULTILINE)
                if match:
                    failed_tests = int(match.group(1))
                    passed_tests = int(match.group(2))
                    total_tests = failed_tests + passed_tests
                    reward = failed_tests / total_tests
                    reward *= self.exception_reward
                else:
                    reward = -self.exception_reward
        except:
            observation = traceback.format_exc()
            reward = self.exception_reward
        terminated = False
        truncated = False
        infos = {}
        return (
            observation,
            reward,
            terminated,
            truncated,
            infos,
        )