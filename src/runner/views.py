from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import HttpResponseBadRequest, JsonResponse

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

        stdout, stderr = code_runner_func(code)

        return JsonResponse(data={"stdout": stdout, "stderr": stderr})

    def _run_python(self, code) -> tuple[str, str]:
        """Runs python code and returns stdout and stderr"""
        pass

    def _run_cpp(self, code) -> tuple[str, str]:
        """Runs c++ code and returns stdout and stderr"""
        pass

    def _run_java(self, code) -> tuple[str, str]:
        """Runs java code and returns stdout and stderr"""
        pass
