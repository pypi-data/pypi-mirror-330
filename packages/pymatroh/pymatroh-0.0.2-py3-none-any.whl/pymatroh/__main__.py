# The main function provides a commandline interface for the package.
# This way you can use it via python -m modulename.

# Include necessary modules.
# User defined modules.
from pymatroh import Matrix
# Std modules.
import argparse

def main():
    """Parameter declaration."""
    # Declaring parameters.
    parser = argparse.ArgumentParser()
    arggroup = parser.add_argument_group(title = "Matrix")
    arggroup.add_argument("-row", "--row", type=int, help=("Row count."))
    arggroup.add_argument("-col", "--column", type=int, help=("Column count."))
    arggroup.add_argument("-rnge", "--range", type=int, default= 100, help=("Integer range. Default = 100."))
    arggroup.add_argument("-mtype", "--matrixtype", type=str, default="int", help=("Type of matrix. You can specify int,float,complex or binary."))
    arggroup.add_argument("-round", "--round", type=bool, default=False, help=("Rounds the result by 3 digits."))

    args = parser.parse_args()

    #Catching parameters.
    if args.row and args.column and not args.matrixtype:
        im = Matrix(args.row, args.column, args.range)
        print(im.create_int_matrix())
    elif args.row and args.column and args.matrixtype:
        im = Matrix(args.row, args.column, args.range, args.round)
        if args.matrixtype == "int":
            print(im.create_int_matrix())
        elif args.matrixtype == "float":
            print(im.create_float_matrix())
        elif args.matrixtype == "complex":
            print(im.create_complex_matrix())
        elif args.matrixtype == "binary":
            print(im.create_binary_matrix())
        else: 
            raise ValueError("Wrong matrixtype on parameter --matrixtype. You can specify int,float,complex or binary.")

if __name__ == '__main__':
    main()