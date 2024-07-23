import sys
import pandas as pd
from os.path import join
from brickschema import Graph
from functions import chamber
import pyshacl

sys.path.append(join('./', 'brick-builder'))

import make as brick


if __name__ == "__main__":
    # run chamber initial brick model
    chamber.make()

    # readfile path
    readfile_folder = 'readfiles'

    brick_schema_file = join(readfile_folder, 'Brick.ttl')
    bldg_brick_file = join(readfile_folder, 'chamber_brick.ttl')
    chamber_point_list_filename = 'cleaned_points-20240311_CBECh_bacnet_scan_output.csv'

    # process chamber bacnet point
    chamber_point_list = pd.read_csv(join(readfile_folder, chamber_point_list_filename))
    chamber_point_list[['object-type', 'object-id']] = chamber_point_list.loc[:, 'object_identifier'].str.split(':', expand=True)
    post_process_pointlist_file = join(readfile_folder, 'chamber_pointlist_postprocess.csv')
    chamber_point_list.to_csv(post_process_pointlist_file, index=False)

    string_template_pairs = [
        (join(readfile_folder, 'chamber_brick_map_tmp.txt'), 
         post_process_pointlist_file, True),
    ]

    parse_template_pairs = brick.parse_template_pairs(string_template_pairs)
    # import pdb; pdb.set_trace()

    # make brick from bacnet csv
    g = brick.generate(parse_template_pairs)
    bldg_bacnet_file = 'chamber_csv.ttl'
    g.serialize(join(readfile_folder, bldg_bacnet_file), format='ttl')

    # initialize a data model with latest Brick schema
    g = Graph(load_brick=True, load_brick_nightly=True)

    # load base building brick model
    g.load_file(join(readfile_folder, bldg_bacnet_file))
    g.load_file(bldg_brick_file)

    # load units schema
    g.load_file('https://qudt.org/2.1/vocab/unit')
    g.load_file('https://qudt.org/schema/qudt/')


    print(f'Before: {len(g)} triples')


    # infer/expand and validate brick model
    # g.expand(profile='owlrl')
    g.expand(profile='shacl', simplify=True)
    
    valid, _, report = g.validate()
    print(f"Graph is valid? {valid}")
    shacl_graph = Graph().parse(brick_schema_file, format="turtle")
    if not valid:
        conforms, results_graph, results_text = pyshacl.validate(
            data_graph=g,
            shacl_graph=shacl_graph,
            inference="rdfs",
            abort_on_first=False,
            meta_shacl=False,
            debug=False,
        )
        results_graph.serialize("validation_results.ttl", format="turtle")
        print("report generated")

    # g.expand(profile='owlrl+shacl+vbis+shacl')

    print(f'After: {len(g)} triples')

    exp_bldg_brick_file = 'chamber_shacl_expanded.ttl'
    g.serialize(exp_bldg_brick_file, format='ttl')

    # import pdb; pdb.set_trace()
