Development
===========



Set up environment
------------------

.. code-block:: bash

    git clone https://github.com/opentargets/OnToma.git
    python3 -m venv env
    source env/bin/activate
    pip install --editable .



Install development packages (optional)
---------------------------------------

.. code-block:: bash

    python3 -m pip install --upgrade pytest sphinx sphinx-rtd-theme



Adding a dependency
-------------------
Installation dependencies are stored in the ``setup.py`` file, in the ``install_requires`` section.



Releasing a new version
-----------------------
#. Modify the version in the ``VERSION`` file.
#. Add a tag: ``git tag $(cat VERSION) && git push origin --tags``.
#. Create a release on GitHub.



Performing a comparison benchmark
---------------------------------
This can be used in case of major updates to OnToma algorithm to make sure they don't break things significantly.

#. Call ``benchmark/sample.sh`` to create a random sample of input strings. This will fetch 100 random records each from ClinVar, PhenoDigm, and gene2phenotype sources. Together they are thought to cover a wide range of use case well. Due to deduplication, the final file ``sample.txt`` may contain slightly less than 300 records.
# Optionally, to add some additional samples from PanelApp JSON file, you can do: ``jq 'keys[]' diseaseToEfo_results.json | tr -d '"' | shuf -n 100 >> sample.txt; sort -uf -o sample.txt sample.txt``.
#. Process the file so that the final output format is a three column TSV file with the following columns: original query; full URI for an EFO term; label from EFO.

    * For OnToma pre-v1.0.0, use: ``time ontoma sample.txt - | awk -F$'\t' '{if (length($2) != 0) {print $1 "\t" $2 "\t" $3}}' | tail -n+2 > ontoma_old.txt``.
    * For OnToma v1.0.0+, use: ``time ontoma --cache-dir EFO_CACHE --columns query,id_full_uri,label <sample.txt >ontoma_new.txt``.
