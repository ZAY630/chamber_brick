import sys
import pandas as pd
from os.path import join
import brickschema

sys.path.append(join('./', 'brick-builder'))

import make as brick


def expand_brick_model(brick_schema_file, bldg_brick_model_file, brick_extensions_file=None, expanded_brick_model_file=None):
    """
    Combine building model with the Brick Schema and expand classes and relationships

    brick_schema_file: file path of Brick ttl
    bldg_brick_model_file: file path of building's brick model
    brick_extensions_file: list of file paths for any Brick extensions
    expanded_brick_model_file: save file path of expanded brick model
    """

    g = brickschema.Graph()
    # import pdb; pdb.set_trace()
    g.load_file(brick_schema_file)
    [g.load_file(fext) for fext in brick_extensions_file]
    g.load_file(bldg_brick_model_file)
    
    # expand Brick graph
    print(f"Starting graph has {len(g)} triples")

    g.expand(profile="owlrl")

    print(f"Inferred graph has {len(g)} triples")

    # serialize inferred Brick to output
    if expanded_brick_model_file is None:
        expanded_brick_model_file = 'expanded_bldg_brick_model.ttl'
    
    with open(expanded_brick_model_file, "wb") as fp:
        fp.write(g.serialize(format="turtle").rstrip().encode('utf-8'))
        fp.write(b"\n")


if __name__ == "__main__":
    readfile_folder = 'readfiles'

    brick_schema_file = join(readfile_folder, 'Brick.ttl')
    brick_extensions_file = [join(readfile_folder, 'bacnet_extension.ttl')]
    expanded_brick_model_file = join(readfile_folder, 'chamber_alt.ttl')

    chamber_point_list_filename = 'cleaned_points-20240311_CBECh_bacnet_scan_output.csv'
    chamber_point_list = pd.read_csv(join(readfile_folder, chamber_point_list_filename))

    chamber_point_list[['BACnetType', 'BACnetInstance']] = chamber_point_list.loc[:, 'object_identifier'].str.split(':', expand=True)

    post_process_pointlist_file = join(readfile_folder, 'chamber_pointlist_postprocess.csv')
    chamber_point_list.to_csv(post_process_pointlist_file, index=False)

    template_pairs = [
        (join(readfile_folder, 'chamber_brick_map_tmp.txt'), post_process_pointlist_file)
    ]

    g = brick.generate(template_pairs)
    bldg_brick_model_file = join(readfile_folder, 'chamber_update.ttl')
    g.serialize(bldg_brick_model_file, format='ttl')

    print('\n******Finished making brick model from point list!******\n')

    print('\n******Now expanding/infering brick model!******\n')

    expand_brick_model(brick_schema_file, bldg_brick_model_file, brick_extensions_file, expanded_brick_model_file)

    print('\n******Finished expanding/infering brick model!******\n')
