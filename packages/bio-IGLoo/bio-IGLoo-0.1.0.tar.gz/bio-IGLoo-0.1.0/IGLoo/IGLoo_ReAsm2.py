# Wrap up python file for the IGLoo 2nd module
import subprocess
import sys
import os
import argparse

# project modulesif __name__ == "__main__" and __package__ is None:
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# project modules
try :
    from IGLoo.scripts.utils import check_program_install, catch_assert  
    import IGLoo.IGLoo_asm as IGLoo_asm
    from IGLoo.scripts import ig_SV_typing
    from IGLoo.scripts import merge_personal_ref_2hap
    from IGLoo.scripts import find_upperCase
    from IGLoo.scripts import find_coverage_region
    from IGLoo.scripts import split_read_from_yak
    from IGLoo.scripts import force_polish
    from IGLoo.scripts import mask_case_n_depth
except ImportError:
    from scripts.utils import check_program_install, catch_assert  
    import IGLoo_asm
    from scripts import ig_SV_typing
    from scripts import merge_personal_ref_2hap
    from scripts import find_upperCase
    from scripts import find_coverage_region
    from scripts import split_read_from_yak
    from scripts import force_polish
    from scripts import mask_case_n_depth

def main(arguments=None):
    parser = argparse.ArgumentParser(description="The 2nd module (bam/fasta) file analyzer of IGLoo.")
    parser.add_argument('-rd', '--result_dir', help="Path to output directory ['result_dir'].", default="result_dir")
    parser.add_argument('-id', '--sample_id',  help="Sample ID ['sample_id'].", default="sample_id")

    parser.add_argument('-fa', '--preprocessed_fasta', help='input preprocessed file', required=True)
    parser.add_argument('-p1', '--parent_yak_1', help='input parent 1 file, should be yak format [result_dir/parent/pat.yak].')
    parser.add_argument('-p2', '--parent_yak_2', help='input parent 2 file, should be yak format [result_dir/parent/mat.yak].')
    parser.add_argument('-t', '--threads', help='number of threads to use', default=8)
    
    #parser.add_argument('--force', help="running the program without checking prerequisite programs.", action='store_true')
    args = parser.parse_args() if arguments is None else arguments
    
    ###### Parameters for IGLoo
    out_dir = args.result_dir
    sample_id  = args.sample_id
    
    input_fasta = args.preprocessed_fasta
    parent_yak_1 = args.parent_yak_1
    parent_yak_2 = args.parent_yak_2
    if parent_yak_1 == None:
        parent_yak_1 = out_dir+'/parent/pat.yak'
    if parent_yak_2 == None:
        parent_yak_2 = out_dir+'/parent/mat.yak'
    threads = args.threads

    
    ## Checking prerequisite programs are installed
    #if flag_force != True:
    check_program_install(["chromosome_scaffolder.sh", \
                           "splitScaffoldsAtNs.sh", \
                           "final_polish.sh", \
                           "samtools", \
                           "minimap2", \
                           "jasper.sh", \
                           "jellyfish", \
                           "yak"])

    # Prepare output directory
    subprocess.call("mkdir -p " + out_dir+'/ref_guide/', shell=True)


    # Run IGLoo_SV_typing
    command = ['-csv1', out_dir+'/asm_annotate/'+sample_id+'.contig_gene.1.csv', \
               '-csv2', out_dir+'/asm_annotate/'+sample_id+'.contig_gene.2.csv', \
               '-f1', out_dir+'/reassembly/'+sample_id+'/'+sample_id+'.IGH.asm.hap1.fa', \
               '-f2', out_dir+'/reassembly/'+sample_id+'/'+sample_id+'.IGH.asm.hap2.fa']
    ig_SV_typing.main(command)
    
    # Run merge_personal_ref_2hap
    script_dir = os.path.dirname(os.path.abspath(__file__))
    command = ['-base', os.path.join(script_dir, 'materials/personalized_ref/referece_base.fa'), \
               '-alt',  os.path.join(script_dir, 'materials/personalized_ref/referece_del.fa'), \
               '-csv1', out_dir+'/reassembly/'+sample_id+'/'+sample_id+'.IGH.asm.hap1.fa.rec.csv', \
               '-csv2', out_dir+'/reassembly/'+sample_id+'/'+sample_id+'.IGH.asm.hap2.fa.rec.csv', \
               '-out1', out_dir+'/reassembly/'+sample_id+'/'+sample_id+'.IGH.asm.hap1.ref.fa', \
               '-out2', out_dir+'/reassembly/'+sample_id+'/'+sample_id+'.IGH.asm.hap2.ref.fa']
    merge_personal_ref_2hap.main(command)


    # Run MaSuRCA
    command = ' '.join(['cp', out_dir+'/reassembly/'+sample_id+'/'+sample_id+'.IGH.asm.hap1.ref.fa', out_dir+'/ref_guide/'])
    subprocess.call(command, shell=True)
    command = ' '.join(['cp', out_dir+'/reassembly/'+sample_id+'/'+sample_id+'.IGH.asm.hap2.ref.fa', out_dir+'/ref_guide/'])
    subprocess.call(command, shell=True)
    
    old_dir = os.getcwd()
    os.chdir(out_dir+'/ref_guide/')

    # Arrange the contigs
    ref_pat = sample_id+'.IGH.asm.hap1.ref.fa'
    ref_mat = sample_id+'.IGH.asm.hap2.ref.fa'
    contigs_1 = sample_id+'.IGH.asm.hap1.fa'
    contigs_2 = sample_id+'.IGH.asm.hap2.fa'

    command = ' '.join(['chromosome_scaffolder.sh', '-r', ref_pat, '-c', '50000', '-i', '99', \
               '-m', '250000', '-q', '../reassembly/'+sample_id+'/'+contigs_1, '-t', str(threads), '-nb'])
    subprocess.call(command, shell=True)
    command = ' '.join(['chromosome_scaffolder.sh', '-r', ref_mat, '-c', '50000', '-i', '99', \
               '-m', '250000', '-q', '../reassembly/'+sample_id+'/'+contigs_2, '-t', str(threads), '-nb'])
    subprocess.call(command, shell=True)

    # split alignments
    arrange_contigs_1 = ref_pat + '.' + contigs_1 + '.split.reconciled.fa'
    arrange_contigs_2 = ref_mat + '.' + contigs_2 + '.split.reconciled.fa'
    command = ' '.join(['splitScaffoldsAtNs.sh', arrange_contigs_1, '1', '>', arrange_contigs_1+'.split'])
    subprocess.call(command, shell=True)
    command = ' '.join(['splitScaffoldsAtNs.sh', arrange_contigs_2, '1', '>', arrange_contigs_2+'.split'])
    subprocess.call(command, shell=True)

    # final polishing
    subprocess.call("mkdir -p " + 'draft_polish_H1', shell=True)
    subprocess.call("mkdir -p " + 'draft_polish_H2', shell=True)
    os.chdir('draft_polish_H1')
    command = ' '.join(['final_polish.sh', '14', '../'+ref_pat, '../'+ref_pat, '../'+arrange_contigs_1])
    subprocess.call(command, shell=True)
    #check if the draft_polish_H1/threshold.txt exists
    if os.path.exists('threshold.txt') == False:
        command = ' '.join(['echo', '2', '>', 'threshold.txt'])
        subprocess.call(command, shell=True)

    os.chdir('../draft_polish_H2')
    command = ' '.join(['final_polish.sh', '14', '../'+ref_mat, '../'+ref_mat, '../'+arrange_contigs_2])
    subprocess.call(command, shell=True)
    #check if the draft_polish_H2/threshold.txt exists
    if os.path.exists('threshold.txt') == False:
        command = ' '.join(['echo', '2', '>', 'threshold.txt'])
        subprocess.call(command, shell=True)
    

    # separate reads
    os.chdir(old_dir)
    command = ' '.join(['yak', 'triobin', parent_yak_1, parent_yak_2, input_fasta, '>', out_dir+'/ref_guide/'+sample_id+'.triobin.log'])
    subprocess.call(command, shell=True)
    command = ['--input_fasta', input_fasta, '--input_yak', out_dir+'/ref_guide/'+sample_id+'.triobin.log', '--output', out_dir+'/ref_guide/'+sample_id+'.separate.read']
    split_read_from_yak.main(command)
    
    
    # Run Jasper for final polishing
    os.chdir(out_dir+'/ref_guide/draft_polish_H1')
    command = ' '.join(['jasper.sh', '-t', '16', '-b', '800000000', '-a', '14.dir/14.all.polished.fa', \
                        '-r', '../'+sample_id+'.separate.read.H1.fasta', '-k', '25', '-p', '3'])
    subprocess.call(command, shell=True)

    os.chdir('../draft_polish_H2')
    command = ' '.join(['jasper.sh', '-t', '16', '-b', '800000000', '-a', '14.dir/14.all.polished.fa', \
                        '-r', '../'+sample_id+'.separate.read.H2.fasta', '-k', '25', '-p', '3'])
    subprocess.call(command, shell=True)
    
    
    # Final masking
    os.chdir('../')

    command = ' '.join(['cp', 'draft_polish_H1/14.all.polished.fa.polished.fasta', './'+sample_id+'.polished_H1.fa'])
    subprocess.call(command, shell=True)
    command = ' '.join(['cp', 'draft_polish_H2/14.all.polished.fa.polished.fasta', './'+sample_id+'.polished_H2.fa'])
    subprocess.call(command, shell=True)

    # read coverage information
    command = ' '.join(['minimap2 -ax map-pb '+sample_id+'.polished_H1.fa '+sample_id+'.separate.read.H1.fasta | \
                        samtools sort -o '+sample_id+'.polished.realign.H1.bam'])
    subprocess.call(command, shell=True)
    command = ' '.join(['minimap2 -ax map-pb '+sample_id+'.polished_H2.fa '+sample_id+'.separate.read.H2.fasta | \
                        samtools sort -o '+sample_id+'.polished.realign.H2.bam'])
    subprocess.call(command, shell=True)
    command = ' '.join(['samtools index', sample_id+'.polished.realign.H1.bam'])
    subprocess.call(command, shell=True)
    command = ' '.join(['samtools index', sample_id+'.polished.realign.H2.bam'])
    subprocess.call(command, shell=True)
    command = ' '.join(['samtools mpileup -aa -d 1000 -f '+sample_id+'.polished_H1.fa '+sample_id+'.polished.realign.H1.bam > '+sample_id+'.polished.realign.H1.mpileup'])
    subprocess.call(command, shell=True)
    command = ' '.join(['samtools mpileup -aa -d 1000 -f '+sample_id+'.polished_H2.fa '+sample_id+'.polished.realign.H2.bam > '+sample_id+'.polished.realign.H2.mpileup'])
    subprocess.call(command, shell=True)
    
    # force polish
    command = ['--mpileup', sample_id+'.polished.realign.H1.mpileup', '--genome', sample_id+'.polished_H1.fa', '--out', sample_id+'.force_polished_H1.fa']
    force_polish.main(command)
    command = ['--mpileup', sample_id+'.polished.realign.H2.mpileup', '--genome', sample_id+'.polished_H2.fa', '--out', sample_id+'.force_polished_H2.fa']
    force_polish.main(command)

    # Then perform cropping based on realignment depth and upper case region
    command = ' '.join(['minimap2 -ax map-pb '+sample_id+'.force_polished_H1.fa '+sample_id+'.separate.read.H1.fasta | \
                        samtools sort -o '+sample_id+'.force.realign.H1.bam'])
    subprocess.call(command, shell=True)
    command = ' '.join(['minimap2 -ax map-pb '+sample_id+'.force_polished_H2.fa '+sample_id+'.separate.read.H2.fasta | \
                        samtools sort -o '+sample_id+'.force.realign.H2.bam'])
    subprocess.call(command, shell=True)
    
    command = ' '.join(['samtools depth '+sample_id+'.force.realign.H1.bam -a -g 0x100 -J > '+sample_id+'.force.realign.rd.H1.log'])
    subprocess.call(command, shell=True)
    command = ' '.join(['samtools depth '+sample_id+'.force.realign.H2.bam -a -g 0x100 -J > '+sample_id+'.force.realign.rd.H2.log'])
    subprocess.call(command, shell=True)
    command = ['-rd', sample_id+'.force.realign.rd.H1.log', '-out', sample_id+'.force.realign.rd.H1.bed']
    find_coverage_region.main(command)
    command = ['-rd', sample_id+'.force.realign.rd.H2.log', '-out', sample_id+'.force.realign.rd.H2.bed']
    find_coverage_region.main(command)


    # find upper case region
    command = ['-fasta', sample_id+'.force_polished_H1.fa', '-out', sample_id+'.force.H1.upperCase.bed']
    find_upperCase.main(command)
    command = ['-fasta', sample_id+'.force_polished_H2.fa', '-out', sample_id+'.force.H2.upperCase.bed']
    find_upperCase.main(command)

    # crop the assembly
    command = ['-rd', sample_id+'.force.realign.rd.H1.bed', '-up', sample_id+'.force.H1.upperCase.bed', \
                        '-fa', sample_id+'.force_polished_H1.fa', '-out', sample_id+'.force_polished_H1.mask.fa']
    mask_case_n_depth.main(command)
    command = ['-rd', sample_id+'.force.realign.rd.H2.bed', '-up', sample_id+'.force.H2.upperCase.bed', \
                        '-fa', sample_id+'.force_polished_H2.fa', '-out', sample_id+'.force_polished_H2.mask.fa']
    mask_case_n_depth.main(command)

    # make the mask assembly directory
    subprocess.call("mkdir -p " + old_dir+'/'+out_dir+'/mask_assembly/', shell=True)

    command = ' '.join(['cp '+sample_id+'.force_polished_H1.mask.fa ../mask_assembly/'+sample_id+'.mask.1.fa'])
    subprocess.call(command, shell=True)
    command = ' '.join(['cp '+sample_id+'.force_polished_H2.mask.fa ../mask_assembly/'+sample_id+'.mask.2.fa'])
    subprocess.call(command, shell=True)

    ## Run IGLoo_asm annotation for the draft assembly
    os.chdir(old_dir)
    #command = ['-rd', out_dir+'/mask_annotate/', '-id', sample_id, \
    #           '-a1', out_dir+'/mask_assembly/'+sample_id+'.mask.1.fa', \
    #            '-a2', out_dir+'/mask_assembly/'+sample_id+'.mask.2.fa']
    input_arguments = argparse.Namespace(result_dir=out_dir+'/mask_annotate/', \
                                         sample_id=sample_id, \
                                         assembly_1=out_dir+'/mask_assembly/'+sample_id+'.mask.1.fa', \
                                         assembly_2=out_dir+'/mask_assembly/'+sample_id+'.mask.2.fa')
    IGLoo_asm.main(input_arguments)
        
    
    



    
if __name__ == "__main__":
    main()


