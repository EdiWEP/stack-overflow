import docker
import subprocess
import os
import re
import shutil

from tempfile import NamedTemporaryFile, mkdtemp, gettempdir
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import HttpResponseBadRequest, JsonResponse
import docker.errors

class CompilationFailed(Exception):
    """Raised when the submitted code has a compilation error"""

    def __init__(self, stdout: str, stderr: str):
        super().__init__()
        self.stdout = stdout
        self.stderr = stderr


class ExecutionFailed(Exception):
    """Raised when the submitted code has a runtime error"""
    def __init__(self, stdout: str, stderr: str):
        super().__init__()
        self.stdout = stdout
        self.stderr = stderr


class InvalidJavaCode(Exception):
    """Raised when the submitted java code is invalid"""


class CodeRunView(LoginRequiredMixin, View):
    """View for handling code run operations"""

    def post(self, request, language: str):
        """Handles POST requests for running the given language"""

        valid_programming_languages = {
            "python": self._run_python,
            "cpp": self._run_cpp,
            "java": self._run_java,
        }

        if language not in valid_programming_languages:
            return HttpResponseBadRequest(f"Invalid programming language '{language}'")

        code_runner_func = valid_programming_languages.get(language)

        code = request.body.decode("utf-8")

        try:
            stdout, stderr = code_runner_func(code)
        except CompilationFailed as exc:
            return JsonResponse(data={"stdout": exc.stdout, "stderr": exc.stderr, "message": "Code resulted in compilation error"})
        except ExecutionFailed as exc:
            return JsonResponse(data={"stdout": exc.stdout, "stderr": exc.stderr, "message": "Code execution encountered runtime error"})
        except InvalidJavaCode as exc:
            return JsonResponse(data={"stdout": "", "stderr": "", "message": "Only java programs with a single top level class can be run"})

        return JsonResponse(data={"stdout": stdout, "stderr": stderr, "message": "Code run was successful"})

    def _run_python(self, code) -> tuple[str, str]:
        """Runs Python code and returns stdout and stderr"""

        temp_file_name = self.__create_temporary_file(code, "py")

        if "import" in code:
            return self._run_in_docker_sandbox(
                temp_file_name=temp_file_name,
                image="python:3.10-slim",
                command=f"python /code/{os.path.basename(temp_file_name)}",
            )

        try:
            result = subprocess.run(
                ["python", temp_file_name],
                capture_output=True,
                text=True,
                shell=True,
            )

            if result.returncode != 0:
                raise ExecutionFailed(result.stdout, result.stderr)

            return result.stdout, result.stderr
        finally:
            self.__remove_file(temp_file_name)

    def _run_cpp(self, code) -> tuple[str, str]:
        """Runs C++ code and returns stdout and stderr"""

        temp_file_name = self.__create_temporary_file(code, "cpp")

        if "include" in code:
            return self._run_in_docker_sandbox(
                temp_file_name=temp_file_name,
                image="gcc:14",
                command=f"g++ {os.path.basename(temp_file_name)} -o code && ./code"
            )

        try:
            binary_name = temp_file_name.replace(".cpp", ".exe")
            compile_result = subprocess.run(
                ["g++", temp_file_name, "-o", binary_name],
                capture_output=True,
                text=True,
                shell=True,
            )

            if compile_result.returncode != 0:
                raise CompilationFailed(compile_result.stdout, compile_result.stderr)

            result = subprocess.run(
                [binary_name],
                capture_output=True,
                text=True,
                shell=True,
            )

            if result.returncode != 0:
                raise ExecutionFailed(result.stdout, result.stderr)
        finally:
            self.__remove_file(temp_file_name)

        return result.stdout, result.stderr

    def _run_java(self, code) -> tuple[str, str]:
        """Runs Java code and returns stdout and stderr"""

        def extract_class_name(code: str) -> str:
            """Extracts the java class name from the code
            Each java program should only have one top level class"""

            match = re.search(r'class\s+(\w+)', code)
            if match:
                return match.group(1)
            else:
                raise InvalidJavaCode

        temp_file_name = self.__create_temporary_file(code, "java")
        class_name = extract_class_name(code)

        if "import" in code:
            return self._run_in_docker_sandbox(
                temp_file_name=temp_file_name,
                image="openjdk:23-jdk-slim",
                command=f"javac {os.path.basename(temp_file_name)} && java -cp /code {class_name}"
            )

        try:

            compile_result = subprocess.run(
                ["javac", temp_file_name],
                capture_output=True,
                text=True,
                shell=True,
            )

            if compile_result.returncode != 0:
                raise CompilationFailed(compile_result.stdout, compile_result.stderr)

            result = subprocess.run(
                ["java", "-cp", temp_file_name.rsplit("\\", 1)[0], class_name],
                capture_output=True,
                text=True,
                shell=True,
            )

            if result.returncode != 0:
                raise ExecutionFailed(result.stdout, result.stderr)
        finally:
            self.__remove_file(temp_file_name)

        return result.stdout, result.stderr

    def _run_in_docker_sandbox(self, temp_file_name: str, image: str, command: str) -> tuple[str, str]:

        try:
            docker_client = docker.from_env()

            container = docker_client.containers.run(
                image=image,
                command=["/bin/bash", "-c", command],
                volumes={os.path.dirname(temp_file_name): {"bind": "/code", "mode": "rw"}},
                stdout=True,
                stderr=True,
                working_dir="/code",
                remove=True
            )

            stdout = container.decode("utf-8")
            return stdout, ""

        except docker.errors.ContainerError as exc:
            return "", exc.stderr.decode("utf-8")

        finally:
            self.__remove_file(temp_file_name)
            pass

    def __create_temporary_file(self, code, extension) -> str:
        """Creates a temporary file in a temporary directory, then returns the path"""
        temp_dir = mkdtemp(prefix="so_code_run_", dir=gettempdir())
        temp_file_path = os.path.join(temp_dir, f"code.{extension}")

        with open(temp_file_path, "w") as temp_file:
            temp_file.write(code)

        return temp_file_path

    def __remove_file(self, file_name: str):
        if os.path.exists(file_name):
            os.remove(file_name)
            shutil.rmtree(os.path.dirname(file_name))
