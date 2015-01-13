#
# Copyright (c) 2015 CNRS
# Author: Florent Lamiraux
#
#
# This file is part of robot_time
# robot_time is free software: you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# robot_time is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Lesser Public License for more details.  You should have
# received a copy of the GNU Lesser General Public License along with
# robot_time  If not, see
# <http://www.gnu.org/licenses/>.

CMAKE_MINIMUM_REQUIRED (VERSION 2.6)

MACRO (FINDPYTHON)
  INCLUDE(FindPythonLibs)
  IF (NOT ${PYTHONLIBS_FOUND} STREQUAL TRUE)
    MESSAGE(FATAL_ERROR "Python has not been found.")
  ENDIF (NOT ${PYTHONLIBS_FOUND} STREQUAL TRUE)

  INCLUDE(FindPythonInterp)
  IF (NOT ${PYTHONINTERP_FOUND} STREQUAL TRUE)
    MESSAGE(FATAL_ERROR "Python executable has not been found.")
  ENDIF (NOT ${PYTHONINTERP_FOUND} STREQUAL TRUE)

  # Find PYTHON_LIBRARY_DIRS
  GET_FILENAME_COMPONENT(PYTHON_LIBRARY_DIRS ${PYTHON_LIBRARIES} PATH)

  # Default Python packages directory
  SET(PYTHON_PACKAGES_DIR site-packages)

  # Use either site-packages (default) or dist-packages (Debian
  # packages) directory
  OPTION(PYTHON_DEB_LAYOUT "Enable Debian-style Python package layout" OFF)

  IF (PYTHON_DEB_LAYOUT)
    SET(PYTHON_PACKAGES_DIR dist-packages)
  ENDIF (PYTHON_DEB_LAYOUT)

  EXECUTE_PROCESS(
    COMMAND "${PYTHON_EXECUTABLE}" "-c" "import sys, os; print(os.sep.join(['lib', 'python' + sys.version[:3], '${PYTHON_PACKAGES_DIR}']))"
    OUTPUT_VARIABLE PYTHON_SITELIB)
  # Remove final \n of the variable PYTHON_SITELIB
  STRING(REPLACE "\n" "" PYTHON_SITELIB "${PYTHON_SITELIB}")
ENDMACRO ()

PROJECT (robot_time CXX)
SET (PROJECT_VERSION 0.1)

FINDPYTHON ()

SET (CMAKE_INSTALL_BINDIR bin CACHE STRING "binary installation")

INSTALL (FILES
  activity.py
  work_sheet.py
  __init__.py
  DESTINATION ${PYTHON_SITELIB}/robot_time
  )

INSTALL (FILES
  start_or_stop_hrp2.py
  DESTINATION ${CMAKE_INSTALL_BINDIR}
  )
