import sys

ENTRY_POINT = "entry_point"
LIBRARY = "library"
DEPENDENCIES = "dependencies"
REQUIREMENTS = "requirements"


def unpack_argv():
    # in any databricks job that uses parameters, sys.argv will contain strings like
    # [ "--entry_point=my.module:main", "--myarg=myval" ]
    job_parameters = {}
    for arg in sys.argv:
        # parameters of any other form are ignored
        if not arg.startswith("--"):
            continue
        if arg.find("=") < 0:
            continue

        k, v = arg[2:].split("=", 1)
        job_parameters[k] = v
    return job_parameters
