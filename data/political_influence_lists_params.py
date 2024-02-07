import os

root = os.path.dirname(os.path.abspath(__file__))

donations = {'path': root + '/donations.csv',
             'reference_cols': ['Donor']
             }


lists = [donations]