class CSVHandler:
    def create_csv(self, filename, words):
        f = open(filename, 'w')
        for word in words:
            f.write(word.to_csv())
        f.close()
