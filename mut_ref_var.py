from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
import read_reference

def mut_ref(df,loc,ref_file,complement,transcript,translate,table_def,based):
	chromosome=loc.split(":")[0]
	ref=read_reference.read_reference_sequence(ref_file,chromosome)
	coordinates=loc.split(":")[1]
	start=int(coordinates.split("-")[0])-based 
	end=int(coordinates.split("-")[1])-based

	line3=""
	for i in range(0,df.shape[0]):
		if i==0:
			if start<int(df.loc[i,"Position"])-based: 
				mut_seq=ref[start:int(df.loc[i,"Position"])-based]
			elif start==int(df.loc[i,"Position"])-based:		
				mut_seq=""
			mut_seq_T=df.loc[i,"ALT"]
			mut_seq=mut_seq+mut_seq_T
			line3=line3+df.loc[i,"Chromosome"]+"_"+df.loc[i,"Position"]+"_"+df.loc[i,"REF"]+"_"+df.loc[i,"ALT"]+"_"+df.loc[i,"Genotype"]+" / "
			start_Next = int(df.loc[i,"Position"])-based+len(df.loc[i,"REF"])
			if (i+1)==df.shape[0]:
				if start_Next>end:
					end = start_Next
				elif start_Next==end:
					mut_seq_T2=ref[start_Next]
					mut_seq=mut_seq+mut_seq_T2
				elif start_Next<end:
					mut_seq_T2=ref[start_Next:end+1]
					mut_seq=mut_seq+mut_seq_T2
					mut_seq=mut_seq.upper()

		else:
			mut_seq_T2=ref[start_Next:int(df.loc[i,"Position"])-based]
			mut_seq=mut_seq+mut_seq_T2			
			
			mut_seq_T=df.loc[i,"ALT"]
			mut_seq=mut_seq+mut_seq_T
			line3=line3+df.loc[i,"Chromosome"]+"_"+df.loc[i,"Position"]+"_"+df.loc[i,"REF"]+"_"+df.loc[i,"ALT"]+"_"+df.loc[i,"Genotype"]+" / "			
			start_Next = int(df.loc[i,"Position"])-1+len(df.loc[i,"REF"])
		
			if i==df.shape[0]-1:
				if start_Next>end:
					end = start_Next
				elif start_Next==end:
					mut_seq_T2=ref[start_Next]
					mut_seq=mut_seq+mut_seq_T2
				elif start_Next<end:
					mut_seq_T2=ref[start_Next:end+1]
					mut_seq=mut_seq+mut_seq_T2
					mut_seq=mut_seq.upper()
	
	records = []
	rec1 = SeqRecord(Seq(ref[start:end+1].upper(),),id="Ref_seq",description=loc,)
	rec2 = SeqRecord(Seq(mut_seq),id="Mut_seq",description=line3,)
	records.append(rec1)
	records.append(rec2)

	if complement=="1":
		rec3 = SeqRecord(Seq(mut_seq).reverse_complement(),id="Reverse_complement_Mut_seq",description="Reverse complement of mutated sequence",)
		mut_seq = str(rec3.seq)
		records.append(rec3)		

	if transcript=="1":
		rec4 = SeqRecord(Seq(mut_seq).transcribe(),id="Transcription_Mut_seq",description="Transcription of coding strand",)
		records.append(rec4)	
	
	if translate=="1":	
		if table_def!="":
			Table=int(table_def) 
		else:
			Table=1
		rec5 = SeqRecord(Seq(mut_seq).translate(table=Table),id="Translation_Mut_seq",description="Translation of coding strand",)
		records.append(rec5)
	
	SeqIO.write(records, "Mutation_sequence.fa", "fasta")


































































