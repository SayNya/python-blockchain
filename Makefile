include Makefile.variable

build-local:
	/bin/bash ${build_path} ${python_version_path}
debug:
	sh ${debug_path} ${python_path} ${environment}
