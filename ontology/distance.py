import logging
import rdflib
import time

logging.basicConfig()
logger = logging.getLogger('logger')
logger.warning('The system may break down')

ns = 'http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#'
start_time = time.time()

g = rdflib.Graph()
g.parse ('../data/ontologies/mara.owl', format='application/rdf+xml')
nif = rdflib.Namespace('http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#')
g.bind('mara', nif)
query = """
select ?super ?sub (count(?mid) as ?distance) { 
  ?super rdfs:subClassOf* ?mid .
  ?mid rdfs:subClassOf+ ?sub .
}
group by ?super ?sub 
order by ?super ?sub
        """
result = g.query(query)
with open("../output/mara_distances.csv", "w") as fout:
    for row in result:
        print(row.super[len(ns):] + "," +row.sub[len(ns):]+"," + row.distance, file=fout)


print("--- %s seconds ---" % (time.time() - start_time))