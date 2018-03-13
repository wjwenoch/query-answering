# query-answering

## Virtuoso management for LUBM
Use the interactive SQL interface: http://localhost:8890/conductor/isql_main.vspx
### Load data
To load a single file, use the following

```SPARQL LOAD <path-to-file-wo-file-protocol> into graph <graph-name>```

+Note that D:/ontologies must be in the **DirsAllowed** in virtuoso.ini file.  
+Make sure the memory options in virtuoso has been properly set to allow for quick loading of large datasets 

To load multiple files in a dir, use this:

```ld_dir('D:/ontologies/lubm/data/','*.owl','http://swat.cse.lehigh.edu/onto/univ-bench/data')```

+If the graph uri is not present, a single filed named 'global.graph' with the default graph name can be put in the dir.

Now verify the list of files to be uploaded by the command:

```select * from DB.DBA.load_list;```

Now load the files by running:
```rdf_loader_run();```

Verify the list of files again to check if the state is 2 (success)

Test a query to check the number of triple loaded:
```
SPARQL 
select count(*) from <http://swat.cse.lehigh.edu/onto/univ-bench/data>
where {?s ?p ?o}
```

-After uploading some files, if the load_lst table is not cleared, you may run into problems. Clear the rows:
```DELETE FROM DB.DBA.load_list```   
-Delete a graph with all its triples by ```SPARQL CLEAR GRAPH <named graph id>```  
-Check all the named graphs in the databases:
```
sparql 
SELECT  DISTINCT ?g 
WHERE  { GRAPH ?g {?s ?p ?o} }
```

### Load schema for inferences
First load a schema file:
```
SPARQL LOAD <http://swat.cse.lehigh.edu/onto/univ-bench.owl> into <http://swat.cse.lehigh.edu/onto/univ-bench.owl>
```
**Note that the above command, for some reason, only works with http protocol. If the schema is a local file, try the other command from DB. E.g., [RDF_LOAD_RDFXML_MT](http://docs.openlinksw.com/virtuoso/fn_rdf_load_rdfxml_mt/)**

Make a ruleset from it:
```
rdfs_rule_set ('lubm:schema', 'http://swat.cse.lehigh.edu/onto/univ-bench.owl') ;
```
Verify if the schema has been properly set:
```
SELECT *
FROM sys_rdf_schema
```
### Issue queries with inference support
An example:
```
sparql
DEFINE input:inference 'lubm:schema'
PREFIX ub:<http://swat.cse.lehigh.edu/onto/univ-bench.owl#> 
select ?x 
from <http://swat.cse.lehigh.edu/onto/univ-bench/data>
where { ?x rdf:type ub:Person . <http://www.University0.edu> ub:hasAlumnus ?x }
```
### Major issues with Virtuoso: the automatic inference support did not get correct answers!
To obtain correct answers for LUBM, manual modifications to the data or queries are [necessary](https://virtuoso.openlinksw.com/dataspace/doc/dav/wiki/Main/VOSArticleLUBMBenchmark).
In particular, the **Entailment** section. 

We chose the materialization approach, in which first the data is materialized manually using the [file](./virtuosoFix.txt)

Then the query text is obtained from the 'Query Text With Materialized Entailed Triples' using the [file](./lubmVirtuosoQueries.txt)
