#  -d, --no-data           Do not load brushes, gradients, palettes, patterns, ...
#  -f, --no-fonts          Do not load any fonts
#  -i, --no-interface      Run without a user interface
#  --batch-interpreter=<procedure>
#                          The procedure to process batch commands with
#  -b, --batch=<commands>  Batch command to run (can be used multiple times)

gimp -i -b - < script.in

