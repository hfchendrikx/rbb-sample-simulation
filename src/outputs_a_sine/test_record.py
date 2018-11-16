#!/usr/bin/env python
import os
import time
import shlex
import subprocess32 as subprocess
import yaml
import signal


class Command:
    def __init__(self, cmd, env=None, cwd=None):
        self._cmd = shlex.split(cmd)
        self._env = os.environ.copy()
        self._cwd = cwd
        self._popen = None
        if env is None:
            env = {}

        for key, value in env.iteritems():
            self._env[key] = value

    def run(self):
        self._popen = subprocess.Popen(self._cmd, env=self._env, cwd=self._cwd)

    def ensure_terminated(self, status=""):
        if self._popen:
            self._popen.poll()

            if self._popen.returncode is None:
                self._popen.send_signal(signal.SIGINT)
                time.sleep(0.2)
                self._popen.poll()

            while self._popen.returncode is None:
                time.sleep(1)
                if status:
                    print(status)
                self._popen.poll()

# Important parameters get passed through the environment variables.
# Every script/program that writes an output.yaml file and rosbags to
# the SIMULATOR_OUTPUT directory qualifies as a simulator setup.
SIMULATOR_OUTPUT = os.environ.get('SIMULATOR_OUTPUT', os.getcwd())

print("Run 1: 1 Hz")
roslaunch_1 = Command("roslaunch outputs_a_sine launch_and_record.launch", {
    'BAG_NAME': SIMULATOR_OUTPUT + '/1.bag',
    'FREQUENCY': '1'
})
roslaunch_1.run()
time.sleep(20)
roslaunch_1.ensure_terminated()

print("Run 2: 5 Hz")
roslaunch_2 = Command("roslaunch outputs_a_sine launch_and_record.launch", {
    'BAG_NAME': SIMULATOR_OUTPUT + '/2.bag',
    'FREQUENCY': '5'
})
roslaunch_2.run()
time.sleep(20)
roslaunch_2.ensure_terminated()

results = {
    'title': "TestSimulationEnvironment",
    'repetitions': {
        'Test run 1Hz': {
            'bag': '1.bag',
            'pass': True,
            'duration': 20.0,
            'results': {"some-result": "good"}
        },
        'Test run 5Hz': {
            'bag': '2.bag',
            'pass': True,
            'duration': 20.0,
            'results': {"some-result": "good"}
        }
    }
}

# Write results
with open(SIMULATOR_OUTPUT + "/output.yaml", 'w') as f:
    yaml.safe_dump(results, f, default_flow_style=False)