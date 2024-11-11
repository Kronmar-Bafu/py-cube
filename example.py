import pandas as pd
from math import pi
import py_cube
import yaml

import py_cube.lindas
from py_cube.lindas.upload import upload_ttl

mock_df = pd.read_csv("example/mock_data.csv")

with open("example/mock_cube.yml") as file:
    cube_yaml = yaml.safe_load(file)

cube = py_cube.Cube(dataframe=mock_df, cube_yaml=cube_yaml, environment="TEST", local=True)
cube.prepare_data()
cube.write_cube()
cube.write_observations()
cube.write_shape()
cube.serialize("example/mock-cube.ttl")
print(cube)

# upload_ttl(filename="./example/mock-cube.ttl", db_file="lindas.ini", environment="TEST")

modk_df_two_sided = pd.read_csv("py_cube/tests/test_data.csv")
with open("py_cube/tests/test.yml") as file:
    two_sided_yaml = yaml.safe_load(file)
cube_two_sided = py_cube.Cube(dataframe=modk_df_two_sided, cube_yaml=two_sided_yaml, environment="TEST", local=True)
cube_two_sided.prepare_data()
cube_two_sided.write_cube()
cube_two_sided.write_observations()
cube_two_sided.write_shape()

# realization: tests of strings and floats sind üüüüäääärch
sparql = sparql = (
            
            "ASK"
            "{"
            "  ?shape a cube:Constraint ;"
            "    sh:property ?prop ."
            "  ?prop sh:path mock:upperUncertainty ;"
            "    schema1:name 'Upper Unsicherheit'@de ;"
            "    sh:maxCount 1 ;"
            "    qudt:scaleType qudt:RatioScale ;"
            "    meta:dimensionRelation ["
            "      a relation:ConfidenceUpperBound ;"
            '      dct:type "Upper uncertainty" ;'
            "      meta:relatesTo mock:value ;"
            "    ] ."
            "}"
        )

result = cube_two_sided._graph.query(sparql)
cube_two_sided.serialize("dummy.ttl")
print(bool(result))