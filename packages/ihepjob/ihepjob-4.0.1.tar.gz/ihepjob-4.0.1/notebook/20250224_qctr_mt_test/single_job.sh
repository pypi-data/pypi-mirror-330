#!/bin/bash
###############################################################################
# Author: Xuefeng DING <dingxf@ihep.ac.cn> @ IHEP-CAS
#
# Project: Qctr3 reco MT check
# Date: 2025 February 23th
# Description:
#   submit jobs at IHEP @ lxlogin.ihep.ac.cn
#
# History:
# v1.0 2025.02.23 dingxf@ihep.ac.cn first version, a default template
#
# Maintainer:
#   Xuefeng Ding <dingxf@ihep.ac.cn>
#
# All rights reserved. 2024 copyrighted.
###############################################################################

output=$1
shift
args=$@

touch $output
echo "rest args <${args}>"
