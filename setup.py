# Copyright (c) 2026 defnlnotme
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from setuptools import setup, find_packages

setup(
    name="mkultra-benchmark",
    version="1.0.0",
    description="Automated LLM benchmark for MKULTRA evaluation (MMLU-style)",
    license="MIT",
    python_requires=">=3.8",
    packages=find_packages(include=["src*", "scripts*", "tests*"]),
    entry_points={
        "console_scripts": [
            "mkultra-bench=run_benchmark:main",
            "build-dataset=build_dataset:main",
            "fetch-youtube=fetch_yt_transcripts:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
        ],
    },
)
