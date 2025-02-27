================
FASTQ File Utils
================

A collection of Python scripts for working with FASTQ files.

Exported console scripts
------------------------

* validate-fastq-file
* analyze-fastq-file

.. code-block:: bash

    validate-fastq-file --infile ~/projects/fastq-file-utils/examples/sample_001_R1.fastq
    --outdir was not specified and therefore was set to '/tmp/sundaram/fastq-file-utils/validate_fastq_file/2025-02-26-101734'
    Created output directory '/tmp/sundaram/fastq-file-utils/validate_fastq_file/2025-02-26-101734'
    --logfile was not specified and therefore was set to 
    '/tmp/sundaram/fastq-file-utils/validate_fastq_file/2025-02-26-101734/validate_fastq_file.log'
    Valid FASTQ file with 3 records.
    Detected Phred Encoding: Phred+33
    Total Records: 3
