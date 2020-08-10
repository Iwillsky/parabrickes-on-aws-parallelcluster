#!/bin/bash
timestr=$(date "+%Y%m%d%H%M%S")

pbrun germline --ref /paradata/parabricks_sample/Ref/Homo_sapiens_assembly38.fasta --in-fq /paradata/parabricks_sample/Data/sample_1.fq.gz /paradata/parabricks_sample/Data/sample_2.fq.gz --knownSites /paradata/parabricks_sample/Ref/Homo_sapiens_assembly38.known_indels.vcf.gz --out-bam /paradata/output$timestr.bam --out-variants /paradata/output$timestr.vcf --out-recal-file /paradata/report$timestr.txt

