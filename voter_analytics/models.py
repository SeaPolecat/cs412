from django.db import models


class Voter(models.Model):
    """Store/represent the data from one registered voter in Newton, MA."""

    last_name = models.TextField()
    first_name = models.TextField()

    street_number = models.TextField()
    street_name = models.TextField()
    apt_number = models.TextField()
    zip = models.TextField()

    birth_date = models.TextField()
    birth_year = models.TextField()
    registration_date = models.TextField()
    party = models.TextField()
    precinct = models.TextField()

    v20state = models.TextField()
    v21town = models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()
    score = models.TextField()

    def __str__(self):
        """Return a string representation of this Voter instance."""

        return f'{self.first_name} {self.last_name} (voter score: {self.score})'
    

def load_data():
    """Function to load data records from CSV file into the Django database."""

    # open the CSV file containing the data
    filename = '/Users/waynewang/Downloads/CS412/data/newton_voters.csv'
    f = open(filename, 'r')

    # for i in range(2):
    #     line = f.readline()

    #     fields = line.strip().split(',')

    #     for j in range(len(fields)):
    #         print(f'fields[{j}] = {fields[j]}')

    # Voter.objects.all().delete()

    # discard the first line containing the column headers
    f.readline()

    # add each line as a separate Voter instance to the database
    for line in f:
        try:
            # get a list of the fields
            fields = line.strip().split(',')

            # create a new Voter instance using the fields 
            # and save it to the db
            voter = Voter(
                last_name = fields[1],
                first_name = fields[2],

                street_number = fields[3],
                street_name = fields[4],
                apt_number = fields[5],
                zip = fields[6],

                birth_date = fields[7],
                birth_year = fields[7][0:4],
                registration_date = fields[8],
                party = fields[9],
                precinct = fields[10],

                v20state = fields[11],
                v21town = fields[12],
                v21primary = fields[13],
                v22general = fields[14],
                v23town = fields[15],
                
                score = fields[16],
            )
            voter.save()

        # skip the line if there was an error
        except Exception as e:
            print(f'AAAAAAAAAAA AN ERROR!!! in line: {line}\n')
            print(e)

    print(f'Done! Created {len(Voter.objects.all())} voters.')


# fields[0] = Voter ID Number
# fields[1] = Last Name
# fields[2] = First Name
# fields[3] = Residential Address - Street Number
# fields[4] = Residential Address - Street Name
# fields[5] = Residential Address - Apartment Number
# fields[6] = Residential Address - Zip Code
# fields[7] = Date of Birth
# fields[8] = Date of Registration
# fields[9] = Party Affiliation
# fields[10] = Precinct Number
# fields[11] = v20state
# fields[12] = v21town
# fields[13] = v21primary
# fields[14] = v22general
# fields[15] = v23town
# fields[16] = voter_score

# fields[0] = 10WLA0879000
# fields[1] = W*
# fields[2] = *I**
# fields[3] = 17
# fields[4] = CIRCUIT AVE
# fields[5] = 3
# fields[6] = 2461
# fields[7] = 1980-01-03
# fields[8] = 2022-11-26
# fields[9] = U 
# fields[10] = 1
# fields[11] = FALSE
# fields[12] = FALSE
# fields[13] = FALSE
# fields[14] = FALSE
# fields[15] = FALSE
# fields[16] = 0