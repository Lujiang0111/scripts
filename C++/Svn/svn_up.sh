#!/bin/bash
SHELL_FOLDER=$(cd "$(dirname "${0}")";pwd)/
svn revert -R ${SHELL_FOLDER}
svn update ${SHELL_FOLDER}
