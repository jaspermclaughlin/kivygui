@echo off
python -c "import sys;from libtool._cmd_argv.cmd import parse ;parse('%*'.split())"
@echo on
