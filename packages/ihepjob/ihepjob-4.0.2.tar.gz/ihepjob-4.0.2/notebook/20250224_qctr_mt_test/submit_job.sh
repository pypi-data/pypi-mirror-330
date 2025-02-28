#!/bin/bash
###############################################################################
# Author: Xuefeng DING <dingxf@ihep.ac.cn> @ IHEP-CAS
#
# Project: Qctr3 reco MT check
# Date: 2025 February 19th
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
# Submission script for

PYTHON_EXE=/hpcfs/juno/junogpu/dingxf/neutrino-physics/ihep-analysis-framework/ihepjob/.venv/bin/python
CONFIG_YAML=/hpcfs/juno/junogpu/dingxf/neutrino-physics/ihep-analysis-framework/ihepjob/notebook/20250224_qctr_mt_test/config.yaml
JOBS_YAML=/hpcfs/juno/junogpu/dingxf/neutrino-physics/ihep-analysis-framework/ihepjob/notebook/20250224_qctr_mt_test/jobs.yaml



OUT=/hpcfs/juno/junogpu/dingxf/log/20250224_qctr_mt_test/log/out_task_1.log
ERR=/hpcfs/juno/junogpu/dingxf/log/20250224_qctr_mt_test/log/err_task_1.log
JOB_ID=0

ARGU="-m ihepjob.single_job --project-config $CONFIG_YAML --jobs-config $JOBS_YAML --job-id $JOB_ID --proc-id %{ProcId}"
hep_submit -argu "$ARGU" \
    -o ${OUT}.%{ClusterId}.%{ProcId} \
    -e ${ERR}.%{ClusterId}.%{ProcId} \
    -cpu 1 -mem 3000 -g juno $PYTHON_EXE


OUT=/hpcfs/juno/junogpu/dingxf/log/20250224_qctr_mt_test/log/out_task_2.log
ERR=/hpcfs/juno/junogpu/dingxf/log/20250224_qctr_mt_test/log/err_task_2.log
JOB_ID=1

ARGU="-m ihepjob.single_job --project-config $CONFIG_YAML --jobs-config $JOBS_YAML --job-id $JOB_ID --proc-id %{ProcId}"
hep_submit -argu "$ARGU" \
    -o ${OUT}.%{ClusterId}.%{ProcId} \
    -e ${ERR}.%{ClusterId}.%{ProcId} \
    -cpu 1 -mem 3000 -g juno $PYTHON_EXE


OUT=/hpcfs/juno/junogpu/dingxf/log/20250224_qctr_mt_test/log/out_task_3.log
ERR=/hpcfs/juno/junogpu/dingxf/log/20250224_qctr_mt_test/log/err_task_3.log
JOB_ID=2

ARGU="-m ihepjob.single_job --project-config $CONFIG_YAML --jobs-config $JOBS_YAML --job-id $JOB_ID --proc-id %{ProcId}"
hep_submit -argu "$ARGU" \
    -o ${OUT}.%{ClusterId}.%{ProcId} \
    -e ${ERR}.%{ClusterId}.%{ProcId} \
    -cpu 1 -mem 3000 -g juno $PYTHON_EXE
