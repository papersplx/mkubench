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
