# From: https://github.com/KiCad/kicad-source-mirror/blob/master/eeschema/plugins/python_scripts/bom_csv_sorted_by_ref.py
# run command:
# $ python main.py PATH_TO_KICAD_XML.xml OUTPUT_FILENAME.csv
import kicad_netlist_reader
import csv
import sys
import json

net = kicad_netlist_reader.netlist(sys.argv[1])

try:
    f = open(sys.argv[2], 'w')
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout

out = csv.writer(f, lineterminator='\n', delimiter=';', quotechar='\"', quoting=csv.QUOTE_ALL)

# Write CSV header
# Refer to https://github.com/KiCad/kicad-source-mirror/blob/master/pcbnew/build_BOM_from_board.cpp#L106-L111
out.writerow([
    'Id', # increment
    'Designator', # E.g. U1, R1
    'Package', # E.g. SMD, 0805, SOT-23-5
    'Quantity', # Quantity of each part
    'Designation', # Column in PartsBox that matches E.g. MPN
    'Supplier and Ref'
])

grouped = net.groupComponents()
count = 0;
for group in grouped:
    refs = ""

    for component in group:
        refs += component.getRef() + ", "
        c = component

    count += 1
    out.writerow([
        count,
        refs,
        c.getFootprint(),
        len(group),
        c.getField("MPN"),
        c.getPartName() + ": " + c.getDescription()
    ])
