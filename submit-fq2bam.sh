#!/bin/bash
timestr=$(date "+%Y%m%d%H%M%S")

pbrun fq2bam --ref /paradata/parabricks_sample/Ref/Homo_sapiens_assembly38.fasta --in-fq /paradata/parabricks_sample/Data/sample_1.fq.gz /paradata/parabricks_sample/Data/sample_2.fq.gz --out-bam /paradata/output$timestr.bam

