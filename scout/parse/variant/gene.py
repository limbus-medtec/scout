#!/usr/bin/env python
# encoding: utf-8
"""
get_genes.py

Parse all information for genes and build mongo engine objects.

Created by Måns Magnusson on 2014-11-10.
Copyright (c) 2014 __MoonsoInc__. All rights reserved.

"""
import logging

from scout.constants import SO_TERMS

def parse_genes(transcripts):
    """Parse transcript information and get the gene information from there.
    
    Use hgnc_id as identifier for genes and ensembl transcript id to identify transcripts
    
    Args:
        transcripts(iterable(dict))

    Returns:
      genes (list(dict)): A list with dictionaries that represents genes
    
    """
    # Dictionary to group the transcripts by hgnc_id
    genes_to_transcripts = {}
    
    # List with all genes and there transcripts
    genes = []

    # Group all transcripts by gene
    for transcript in transcripts:
        # Check what hgnc_id a transcript belongs to
        hgnc_id = transcript['hgnc_id']
        hgnc_symbol = transcript['hgnc_symbol']

        # If there is a identifier we group the transcripts under gene
        if hgnc_id:
            if hgnc_id in genes_to_transcripts:
                genes_to_transcripts[hgnc_id].append(transcript)
            else:
                genes_to_transcripts[hgnc_id] = [transcript]
        else:
            if hgnc_symbol:
                if hgnc_symbol in genes_to_transcripts:
                    genes_to_transcripts[hgnc_symbol].append(transcript)
                else:
                    genes_to_transcripts[hgnc_symbol] = [transcript]

    # We need to find out the most severe consequence in all transcripts
    # and save in what transcript we found it
    
    # Loop over all genes
    for gene_id in genes_to_transcripts:
        # Get the transcripts for a gene
        gene_transcripts = genes_to_transcripts[gene_id]
        # This will be a consequece from SO_TERMS
        most_severe_consequence = None
        # Set the most severe score to infinity
        most_severe_rank = float('inf')
        # The most_severe_transcript is a dict
        most_severe_transcript = None
        
        most_severe_region = None
        
        most_severe_sift = None
        most_severe_polyphen = None
        
        # Loop over all transcripts for a gene to check which is most severe
        for transcript in gene_transcripts:
            hgnc_id = transcript['hgnc_id']
            hgnc_symbol = transcript['hgnc_symbol']
            # Loop over the consequences for a transcript
            for consequence in transcript['functional_annotations']:
                # Get the rank based on SO_TERM
                # Lower rank is worse
                new_rank = SO_TERMS[consequence]['rank']
                
                if new_rank < most_severe_rank:
                    # If a worse consequence is found, update the parameters
                    most_severe_rank = new_rank
                    most_severe_consequence = consequence
                    most_severe_transcript = transcript
                    most_severe_sift = transcript['sift_prediction']
                    most_severe_polyphen = transcript['polyphen_prediction']
                    most_severe_region = SO_TERMS[consequence]['region']

        gene = {
            'transcripts': gene_transcripts,
            'most_severe_transcript': most_severe_transcript,
            'most_severe_consequence': most_severe_consequence,
            'most_severe_sift': most_severe_sift,
            'most_severe_polyphen': most_severe_polyphen,
            'hgnc_id': hgnc_id,
            'hgnc_symbol': hgnc_symbol,
            'region_annotation': most_severe_region,
        }
        genes.append(gene)    

    return genes
