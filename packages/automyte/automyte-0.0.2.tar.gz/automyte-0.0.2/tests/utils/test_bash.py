from pathlib import Path

from automyte.utils import bash

FILEDIR = Path(__file__).parent


class TestBashExecute:
    def test_execute_returns_output_as_text(self):
        result = bash.execute(command="pwd", path=FILEDIR)
        assert result == str(FILEDIR)
