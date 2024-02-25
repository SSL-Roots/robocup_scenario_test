# Copyright 2024 Roots
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
import threading
import signal
import os
import glob


class Recorder:
    def __init__(self, command_name: str = "./ssl-log-recorder"):
        self._command_name = command_name
        self._process = None
        self._thread = None

    def check_command_available(self):
        try:
            subprocess.run([self._command_name, "--help"], check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            return False

    def start(self):
        # Start the recording in a separate thread.
        def _recording():
            self._process = subprocess.Popen(
                [self._command_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_IGN)
            )
            self._process.communicate()

        if not self.check_command_available():
            print(f"Command '{self._command_name}' is not available.")
            return

        self._thread = threading.Thread(target=_recording)
        self._thread.start()

    def stop(self, file_name: str = "recording", save=True):
        # Stop the recording and rename the latest log file.
        if self._process:
            self._process.send_signal(signal.SIGINT)
            self._process.wait()  # Wait for the process to finish.
            self._process = None

            # If the file name is empty, use the default name.
            if not file_name.strip():
                file_name = "recording"

            self._rename_latest_log_file(file_name)
            if not save:
                self.remove_log_file(file_name)

    def _rename_latest_log_file(self, new_file_name: str):
        # Find the latest log file and rename it.
        # Note: This method finds the latest log file in the current directory.
        new_file_name += ".log.gz"
        list_of_files = glob.glob('*.log.gz')
        if not list_of_files:
            print("log file not found.")
            return

        latest_file = max(list_of_files, key=os.path.getctime)
        os.rename(latest_file, new_file_name)
        print("Renamed the latest log file {} to {}.".format(
            latest_file, new_file_name))

    def remove_log_file(self, filename: str):
        if os.path.exists(filename):
            os.remove(filename)
            print("Removed the log file {}.".format(filename))
        else:
            print("The file {} does not exist.".format(filename))
