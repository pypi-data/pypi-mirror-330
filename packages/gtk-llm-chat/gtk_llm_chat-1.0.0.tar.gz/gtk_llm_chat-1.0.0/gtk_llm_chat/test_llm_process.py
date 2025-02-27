import unittest
from unittest.mock import MagicMock, call
from gtk_llm_chat.llm_process import LLMProcess, Message
from gi.repository import Gio
from gi.repository import GLib

class TestLLMProcess(unittest.TestCase):

    def test_initialize(self):
        # Mock Gio.SubprocessLauncher and GLib.Bytes
        #launcher_mock = MagicMock()
        #process_mock = MagicMock()
        #Gio.SubprocessLauncher.new = MagicMock(return_value=launcher_mock)
        #launcher_mock.spawnv.return_value = process_mock # Set return value here
        #process_mock.get_stdout_pipe.return_value.read_bytes_async.side_effect = lambda *args: args[-1](process_mock.get_stdout_pipe.return_value, MagicMock(), callback_mock)
        #process_mock.get_stdout_pipe.return_value.read_bytes_async = MagicMock()

        # Patch the Gio and GLib objects
        GLib.Bytes = MagicMock()

        llm_process = LLMProcess()
        callback_mock = MagicMock() # Mock the callback

        llm_process.initialize(callback_mock)

        # Assertions
        #launcher_mock.spawnv.assert_called_once()
        #callback_mock.assert_called_once()

    def test_execute(self):

        # Mock necessary objects
        llm_process = LLMProcess()
        llm_process.process = MagicMock()
        llm_process.stdin = MagicMock()
        llm_process._read_response = MagicMock()

        messages = [Message("Test message", sender="test_user")]
        callback_mock = MagicMock()

        llm_process.execute(messages, callback_mock)

        # Assertions
        llm_process.stdin.write_bytes.assert_called_once()
        llm_process._read_response.assert_called_once_with(callback_mock)
        expected_message = b"test_user: Test message\n"
        actual_call = llm_process.stdin.write_bytes.call_args
        actual_bytes = actual_call[0][0]
        self.assertEqual(bytes(actual_bytes.get_data()), expected_message)

    def test_handle_initial_output(self):
        # Mock necessary objects
        llm_process = LLMProcess()
        stdout_mock = MagicMock()
        result_mock = MagicMock()
        bytes_mock = MagicMock()
        callback_mock = MagicMock()

        # Case 1: Output contains "Chatting with"
        stdout_mock.read_bytes_finish.return_value = bytes_mock
        bytes_mock.get_data.return_value = b"Chatting with TestModel\n"
        llm_process._handle_initial_output(stdout_mock, result_mock, callback_mock)
        callback_mock.assert_called_once_with("TestModel")

        # Case 2: Output does not contain "Chatting with"
        callback_mock.reset_mock()
        bytes_mock.get_data.return_value = b"Some other output\n"
        llm_process._handle_initial_output(stdout_mock, result_mock, callback_mock)
        callback_mock.assert_called_once_with(None)

    def test_handle_response(self):
        # Mock necessary objects
        llm_process = LLMProcess()
        stdout_mock = MagicMock()
        result_mock = MagicMock()
        bytes_mock = MagicMock()
        callback_mock = MagicMock()

        # Case 1: Simple response
        stdout_mock.read_bytes_finish.return_value = bytes_mock
        bytes_mock.get_data.return_value = b"Test response"
        llm_process._handle_response(stdout_mock, result_mock, (callback_mock, ""))
        callback_mock.assert_called_once_with("Test response")

        # Case 2: Empty response
        callback_mock.reset_mock()
        bytes_mock.get_data.return_value = b""
        llm_process._handle_response(stdout_mock, result_mock, (callback_mock, ""))
        callback_mock.assert_not_called()

        # Case 3: Response ends with ">"
        callback_mock.reset_mock()
        bytes_mock.get_data.return_value = b"Test response >"
        llm_process._handle_response(stdout_mock, result_mock, (callback_mock, ""))
        callback_mock.assert_called_once_with("Test response >")

if __name__ == '__main__':
    unittest.main()