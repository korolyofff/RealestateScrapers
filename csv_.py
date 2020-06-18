import _csv as csv
import os

class csv_():
    def csv_new(self, filename):
        DATA = [['Type', 'URL', 'Listing Agent', 'Price', 'Address', 'Beds', 'Showers', 'Cars',
                'Location Type', 'Size of the property', 'Description', 'Features']]
        with open(filename, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in DATA:
                writer.writerow(line)



    def csv_writer(self, data, filename):
        if not os.path.isfile(filename) or os.stat(filename).st_size == 0:
            self.csv_new(filename)

        with open(filename, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in data:
                writer.writerow(line)


if __name__ == "__main__":
    print('python3 main.py ...')