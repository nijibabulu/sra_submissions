# Checking for UniVec matches to assembled transcriptomes

Unfortunately NCBI does a check on all known illumina/nextera etc. vector and primer sequences which may be contaminating a transcriptome assembly when submitting to the TSA database. In order to get rid of these, the best procedure would be to remove all such sequences from the originating reads, but this is unfortunately not possible at the end of a project. Therefore it might be possible to remove the assemblies themselves, but this might be too many: 

```
blastn -num_threads 16 -task blastn -reward 1 -penalty -3 -evalue 700 -searchsp 1750000000000 -dust yes -gapopen 3 -gapextend 3 -query /export/home/dnyansagar/1/blastdb/Edwardsiella_carnea.transcriptome.trinity130912_V2.fasta -db univecdb/UniVec  -outfmt 6 > Edwardsiella_carnea.transcriptome.trinity130912_V2.UniVecMatches.txt
awk '{print $1}' Edwardsiella_carnea.transcriptome.trinity130912_V2.UniVecMatches.txt | sort -u > Edwardsiella_carnea.transcriptome.trinity130912_V2.UniVecContaminatedSequences.txt
blastn -num_threads 16 -task blastn -reward 1 -penalty -3 -evalue 700 -searchsp 1750000000000 -dust yes -gapopen 3 -gapextend 3 -query /export/home/dnyansagar/1/blastdb/Edwarsiella_lineata_Eu_parasite.fasta -db univecdb/UniVec  -outfmt 6 > Edwarsiella_lineata_Eu_parasite.UniVecMatches.txt
awk '{print $1}' Edwarsiella_lineata_Eu_parasite.UniVecMatches.txt | sort -u > Edwarsiella_lineata_Eu_parasite.UniVecContaminatedSequences.txt
blastn -num_threads 16 -task blastn -reward 1 -penalty -3 -evalue 700 -searchsp 1750000000000 -dust yes -gapopen 3 -gapextend 3 -query 06_Met_trim_trinity_assembly.Trinity.fasta -db univecdb/UniVec  -outfmt 6 > 06_Met_trim_trinity_assembly.Trinity.UniVecMatches.txt
awk '{print $1}' 06_Met_trim_trinity_assembly.Trinity.UniVecMatches.txt | sort -u > 06_Met_trim_trinity_assembly.Trinity.UniVecContaminatedSequences.txt
blastn -num_threads 16 -task blastn -reward 1 -penalty -3 -evalue 700 -searchsp 1750000000000 -dust yes -gapopen 3 -gapextend 3 -query Scol_combined_assemblies_Trinity.fasta -db univecdb/UniVec  -outfmt 6 > Scol_combined_assemblies_Trinity.UniVecMatches.txt
awk '{print $1}' Scol_combined_assemblies_Trinity.UniVecMatches.txt | sort -u > Scol_combined_assemblies_Trinity.UniVecContaminatedSequences.txt
```

`Edwardsiella_carnea.transcriptome.trinity130912_V2.UniVecMatches.txt` has 43275 of 296463 transcripts with matches and `Edwarsiella_lineata_Eu_parasite.UniVecMatches.txt` has 22545 of 186572 with matches. It might be possible to either remove the sequences altogether if they were never used in the analysis, or to trim the actual transcripts.


After checking for vector sequences, the TSA submission server then searches for sequences which are (probably) in nr. I could download these contaminated IDs.

```
grep carnea Edwardsiella_carnea_transcriptome_trinity130912_V2.Contamination.txt | awk '{print $1}' > Edwardsiella_carnea_transcriptome_trinity130912_V2.MegablastContaminatedSequences.txt
grep '^TR' Edwarsiella_lineata_Eu_parasite.Contamination.txt | sed -e 's/_/|/' | awk '{print $1}' > Edwarsiella_lineata_Eu_parasite.MegablastContaminatedSequences.txt
grep '^TR' 06_Met_trim_trinity_assembly_Trinity.Contamination.txt |  awk '{print $1}' > 06_Met_trim_trinity_assembly_Trinity.MegablastContaminatedSequences.txt
grep '^TR' Scol_combined_assemblies_Trinity_clean_fixed.Contamination.txt |  awk '{print $1}' > Scol_combined_assemblies_Trinity_clean_fixed.MegablastContaminatedSequences.txt

```

According to Rohit, those sequences are not included in the analysis (I haven't checked about Dani's Metredium or Scolanthus sequences yet though), so I removed them. In order to extract the uncontaminated sequences, I used

```
comm -23 <(grep '^>' /export/home/dnyansagar/1/blastdb/Edwarsiella_lineata_Eu_parasite.fasta | cut -d ' ' -f 1  | sed -e 's/>//' | sort -u) <(cat Edwarsiella_lineata_Eu_parasite.MegablastContaminatedSequences.txt Edwarsiella_lineata_Eu_parasite.UniVecContaminatedSequences.txt | sort -u)  > Edwarsiella_lineata_Eu_parasite.Clean.txt
comm -23 <(grep '^>' /export/home/dnyansagar/1/blastdb/Edwardsiella_carnea.transcriptome.trinity130912_V2.fasta | cut -d ' ' -f 1  | sed -e 's/>//' | sort -u) <(cat Edwardsiella_carnea_transcriptome_trinity130912_V2.MegablastContaminatedSequences.txt Edwardsiella_carnea.transcriptome.trinity130912_V2.UniVecContaminatedSequences.txt | sort -u) > Edwardsiella_carnea.transcriptome.trinity130912_V2.Clean.txt
comm -23 <(grep '^>' 06_Met_trim_trinity_assembly.Trinity.fasta | cut -d ' ' -f 1 | sed -e 's/>//' | sort -u ) <(cat 06_Met_trim_trinity_assembly_Trinity.MegablastContaminatedSequences.txt 06_Met_trim_trinity_assembly.Trinity.UniVecContaminatedSequences.txt | sort -u) > 06_Met_trim_trinity_assembly.Trinity.Clean.txt
comm -23 <(grep '^>' Scol_combined_assemblies_Trinity.fasta | cut -d ' ' -f 1 | sed -e 's/>//' | sort -u )  Scol_combined_assemblies_Trinity.UniVecContaminatedSequences.txt > Scol_combined_assemblies_Trinity.Clean.txt
```
It is also necessary to have headers of a specified format (and length), below:

```
sed -e 's/^\(>[0-9a-zA-Z_|]*\)[[:space:]].*$/\1 [moltype=transcribed_RNA]/; s/|/_/g' /export/home/dnyansagar/1/blastdb/Edwarsiella_lineata_Eu_parasite.fasta > Edwarsiella_lineata_Eu_parasite.fsa
sed -e 's/^\(>[0-9a-zA-Z_|]*\)[[:space:]].*$/\1 [moltype=transcribed_RNA]/' /export/home/dnyansagar/1/blastdb/Edwardsiella_carnea.transcriptome.trinity130912_V2.fasta > Edwardsiella_carnea.transcriptome.trinity130912_V2.fsa
sed -e 's/^\(>[0-9a-zA-Z_|]*\)[[:space:]].*$/\1 [moltype=transcribed_RNA]/' 06_Met_trim_trinity_assembly.Trinity.fasta > 06_Met_trim_trinity_assembly.Trinity.fsa
sed -e 's/^\(>[0-9a-zA-Z_|]*\)[[:space:]].*$/\1 [moltype=transcribed_RNA]/' Scol_combined_assemblies_Trinity.fasta > Scol_combined_assemblies_Trinity.fsa
```

Now, get the cleaned transcripts (I rewrote `fasta_extract` in python in order to accommodate the fact that the Clean.txt files won't be allowed on a command line):
```
 python fasta_extract.py Edwarsiella_lineata_Eu_parasite.fsa <(sed -e 's/|/_/' Edwarsiella_lineata_Eu_parasite.Clean.txt) > Edwarsiella_lineata_Eu_parasite.clean_v2.fsa
 python fasta_extract.py Edwardsiella_carnea.transcriptome.trinity130912_V2.fsa Edwardsiella_carnea.transcriptome.trinity130912_V2.Clean.txt > Edwardsiella_carnea.transcriptome.trinity130912_V2.clean_v2.fsa
 python fasta_extract.py 06_Met_trim_trinity_assembly.Trinity.fsa 06_Met_trim_trinity_assembly.Trinity.Clean.txt > 06_Met_trim_trinity_assembly.Trinity.clean_v3.fsa
 python fasta_extract.py Scol_combined_assemblies_Trinity.fsa Scol_combined_assemblies_Trinity.Clean.txt > Scol_combined_assemblies_Trinity.clean.fsa
```

In order to update the name of the file to be comiserate with the discovery of the paper, we did the following:

```
ln -s Edwarsiella_lineata_Eu_parasite.clean.fsa Edwarsiella_carnea_Eu_parasite.clean.fsa
```

Additionally, the Scolanthus transcriptome had repeated IDs. I wrote a custom script, `fix_scol_ids.py`, to fix this problem:

```
python fix_scol_ids.py Scol_combined_assemblies_Trinity.clean.fsa > Scol_combined_assemblies_Trinity.clean.fixed.fsa
```

additionally we have to exclude the sequences which were found by MegaBLAST in the NCBI pipeline. This has to be done after fixing the IDs because the submitted version had the modified IDs.

```
python fasta_extract.py --exclude Scol_combined_assemblies_Trinity.clean.fixed.fsa Scol_combined_assemblies_Trinity_clean_fixed.MegablastContaminatedSequences.txt > Scol_combined_assemblies_Trinity.clean_v2.fixed.fsa
```

For `06_Met_trim_trinity_assembly.Trinity.fasta` there were matches to UniVec (not detected above) to `TRINITY_DN11994_c0_g1_i1` and `TRINITY_DN11994_c0_g2_i1`. I removed these manually and resubmitted.

