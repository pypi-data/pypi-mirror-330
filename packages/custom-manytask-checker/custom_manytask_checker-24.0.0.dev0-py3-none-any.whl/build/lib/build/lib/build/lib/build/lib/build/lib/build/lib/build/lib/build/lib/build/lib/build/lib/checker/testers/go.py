from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from checker.exceptions import (
    BuildFailedError,
    ExecutionFailedError,
    StylecheckFailedError,
    TestsFailedError,
    TimeoutExpiredError,
)

IGNORE_FILE_PATTERNS = ['go.mod', 'go.sum', '.tester.json']

from checker.utils.files import check_files_contains_regexp, copy_files
from checker.utils.print import print_info
from checker.testers.tester import Tester

class GoTester(Tester):

    @dataclass
    class TaskTestConfig(Tester.TaskTestConfig):
        module_name: str = ''
        
        allow_change: list[str] = field(default_factory=list)
        forbidden_regexp: list[str] = field(default_factory=list)
        copy_to_build: list[str] = field(default_factory=list)

        is_crash_me: bool = False

        tests: list[str] = field(default_factory=list)
        input_file: str = ''
        args: list[str] = field(default_factory=list)
        timeout: float = 60.
        capture_output: bool = True

        def __post_init__(
                self,
        ) -> None:
            assert self.allow_change
            assert self.copy_to_build
            pass

    def _gen_build(  # type: ignore[override]
            self,
            test_config: TaskTestConfig,
            build_dir: Path,
            source_dir: Path,
            public_tests_dir: Path | None,
            private_tests_dir: Path | None,
            tests_root_dir: Path,
            sandbox: bool = True,
            verbose: bool = False,
            normalize_output: bool = False,
    ) -> None:
        verbose = True
        check_files_contains_regexp(
            source_dir,
            regexps=test_config.forbidden_regexp,
            patterns=test_config.allow_change,
            raise_on_found=True,
        )
        task_dir = private_tests_dir
        self._executor(
            copy_files,
            source=source_dir,
            target=task_dir,
            patterns=test_config.allow_change,
            verbose=verbose,
        )
        self._executor(
            copy_files,
            source=task_dir,
            target=build_dir,
            patterns=test_config.copy_to_build,
            ignore_patterns=IGNORE_FILE_PATTERNS,
            verbose=verbose,
        )

        try:
            print_info('Init GO module ...', color='orange')
            self._executor(
                ['go', 'mod', 'init', test_config.module_name],
                cwd=build_dir,
                verbose=verbose,
            )
            print_info('Tidy GO module ...', color='orange')
            self._executor(
                ['go', 'mod', 'tidy'],
                cwd=build_dir,
                verbose=verbose,
            )
            self._executor(
                ['ls', '-al'],
                cwd=build_dir,
                verbose=verbose,
            )
        except ExecutionFailedError:
            print_info('ERROR', color='red')
            raise BuildFailedError('can\'t init GO module')

    def _clean_build(  # type: ignore[override]
            self,
            test_config: TaskTestConfig,
            build_dir: Path,
            verbose: bool = False,
    ) -> None:
        # self._executor(
        #     ['rm', '-rf', str(build_dir)],
        #     check=False,
        #     verbose=verbose,
        # )
        pass

    def _run_tests(  # type: ignore[override]
            self,
            test_config: TaskTestConfig,
            build_dir: Path,
            sandbox: bool = False,
            verbose: bool = False,
            normalize_output: bool = False,
    ) -> float:
        stdin = None
        verbose = True
        try:
            print_info(f'Testing {test_config.module_name}...', color='orange')
            # args = test_config.args
            args = []
            # if test_config.input_file != '':
            #     stdin = open(build_dir / test_config.input_file, 'r')
            self._executor(
                ['ls', '-al'],
                cwd=build_dir,
                verbose=verbose,
            )
            self._executor(
                ['go', 'test', *args],
                cwd=build_dir,
                verbose=verbose,
                # capture_output=test_config.capture_output,
                timeout=test_config.timeout,
                # stdin=stdin
            )
            if test_config.is_crash_me:
                print_info('ERROR', color='red')
                raise TestsFailedError('Program has not crashed')
            print_info('OK', color='green')
        except TimeoutExpiredError:
            print_info('ERROR', color='red')
            message = f'Your solution exceeded time limit: {test_config.timeout} seconds'
            raise TestsFailedError(message)
        except ExecutionFailedError:
            if not test_config.is_crash_me:
                print_info('ERROR', color='red')
                raise TestsFailedError("Test failed (wrong answer or sanitizer error)")
        finally:
            if stdin is not None:
                stdin.close()

        if test_config.is_crash_me:
            print_info('Program has crashed', color='green')
        else:
            print_info('All tests passed', color='green')
        return 1.
