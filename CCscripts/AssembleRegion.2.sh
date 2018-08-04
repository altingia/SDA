#!/usr/bin/env bash
grep -v "^@" $1 | awk '{ print ">"$1;print $10;}' > reads.fasta
make -f /net/eichler/vol5/home/mchaisso/projects/PacBioSequencing/scripts/local_assembly/CanuSamAssembly.mak assembly.consensus.fasta SAM=$1 


#
#~chrismh/src/canu-repo/Linux-amd64/bin/canu -p asm -d canu  genomeSize=30k  -pacbio-raw reads.fasta  useGrid=0
#gunzip canu/asm.correctedReads.fasta.gz
#~chrismh/src/amos-3.1.0/bin/toAmos -s canu/asm.correctedReads.fasta -o canu/asm.amos.afg
#~chrismh/src/amos-3.1.0/bin/minimus2 canu/asm.amos -D OVERLAP=500 -D MINID=97
#cp canu/asm.amos.fasta assembly.fasta

if [ ! -s assembly.consensus.fasta ]; then
		QuiverDir=/net/eichler/vol5/home/mchaisso/software/quiver
		unset QRSH_COMMAND && source $QuiverDir/setup_quiver.sh
		
		/net/eichler/vol5/home/mchaisso/projects/blasr/cpp/pbihdfutils/bin/samtobas $1 reads.bas.h5 -defaultToP6
		blasr reads.bas.h5 ../ref.fasta -sam -bestn 1 -nproc 4 -out /dev/stdout -clipping soft | samtools view -bS - | samtools sort -T tmp -o reads.to_ref.bam
		samtools index reads.to_ref.bam
		covStart=`samtools depth reads.to_ref.bam | head -1 | cut -f 1`
		covEnd=`samtools depth reads.to_ref.bam | tail -1 | cut -f 1`
		refName=`head -1 ../ref.fasta | tr -d ">\n"`
		/net/eichler/vol5/home/mchaisso/software/quiver/bin/quiver  -j8 --minCoverage 1 --noEvidenceConsensusCall nocall --referenceFilename ../ref.fasta reads.to_ref.bam -o assembly.quiver.orig.fasta
		/net/eichler/vol5/home/mchaisso/projects/AssemblyByPhasing/scripts/abp/RemoveFlankingNs.py assembly.quiver.orig.fasta assembly.quiver.fasta

fi
		
		



