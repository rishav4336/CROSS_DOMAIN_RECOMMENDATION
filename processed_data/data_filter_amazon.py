import sys
import os
import json
import pickle
import numpy as np
import csv
from tqdm import tqdm

# amazon-[Movie and Book], amazon2-[Movie and Music], amazon3-[Music and Book]
# Movie---ratings_Movies_and_TV.csv, Book---ratings_Books.csv, Music---ratings_CDs_and_Vinyl.csv

data_file = 'amazon3'
# set right file names for each dataset,
file1 = 'ratings_CDs_and_Vinyl.csv'  # rating file of domain1
file2 = 'ratings_Books.csv'  # rating file of domain2


class Dataset:
    def __init__(self):
        self.peo2movie = dict()
        self.peo2book = dict()
        self.movie2peo = dict()
        self.book2peo = dict()
        self.peo2movie_final = dict()
        self.peo2book_final = dict()

    def read_data(self):
        peo2movie = {}
        peo2book = {}
        with open(os.path.join(data_file, file1), 'r') as f:
            moviereader = csv.reader(f)
            for line in moviereader:
                user, movie, rank = line[0], line[1], float(line[2])
                if rank>=3:
                    if user not in peo2movie:
                        peo2movie[user] = []
                    peo2movie[user] += [[movie, rank]]

        with open(os.path.join(data_file, file2), 'r') as f:
            bookreader = csv.reader(f)
            for line in bookreader:
                user, book, rank = line[0], line[1], float(line[2])
                if rank>=3:
                    if user not in peo2book:
                        peo2book[user] = []
                    peo2book[user] += [[book, rank]]

        movie_count = 0
        book_count = 0
        both_count = 0
        both = []
        user = []
        movie = []
        book = []

        #data filtering

        #filter users

        for item in tqdm(peo2movie.keys()):
            if len(peo2movie[item]) > 5:
                self.peo2movie[item] = peo2movie[item]

        for item in tqdm(peo2book.keys()):
            if len(peo2book[item]) > 5:
                self.peo2book[item] = peo2book[item]

        temp_keys = list(self.peo2book.keys())
        for item in tqdm(temp_keys):
            if item not in self.peo2movie:
                self.peo2book.pop(item)

        temp_keys = list(self.peo2movie.keys())
        for item in tqdm(temp_keys):
            if item not in self.peo2book:
                self.peo2movie.pop(item)

        print('user:', len(self.peo2movie), len(self.peo2book), len(both))

        # construct item dictionary
        for item in tqdm(self.peo2movie.keys()):
            for each in self.peo2movie[item]:
                if each[0] not in self.movie2peo:
                    self.movie2peo[each[0]] = []
                self.movie2peo[each[0]] += [[item, each[1]]]

        for item in tqdm(self.peo2book.keys()):
            for each in self.peo2book[item]:
                if each[0] not in self.book2peo:
                    self.book2peo[each[0]] = []
                self.book2peo[each[0]] += [[item, each[1]]]

        print('movie #:', len(self.movie2peo), 'book #:', len(self.book2peo))

        # filter items
        temp_keys = list(self.movie2peo.keys())
        for item in temp_keys:
            if len(self.movie2peo[item]) <= 5:
                self.movie2peo.pop(item)

        temp_keys = list(self.book2peo.keys())
        for item in temp_keys:
            if len(self.book2peo[item]) <= 5:
                self.book2peo.pop(item)

        print('after filter: movie #:', len(self.movie2peo), 'book #:', len(self.book2peo))

        for item in self.movie2peo.keys():
            for each in self.movie2peo[item]:
                if each[0] not in self.peo2movie_final:
                    self.peo2movie_final[each[0]] = []
                self.peo2movie_final[each[0]] += [[item, each[1]]]

        for item in self.book2peo.keys():
            for each in self.book2peo[item]:
                if each[0] not in self.peo2book_final:
                    self.peo2book_final[each[0]] = []
                self.peo2book_final[each[0]] += [[item, each[1]]]
        print('user:', len(self.peo2book_final), len(self.peo2movie_final))

        temp_keys = list(self.peo2book_final.keys())
        for item in tqdm(temp_keys):
            if item not in self.peo2movie_final:
                self.peo2book_final.pop(item)

        temp_keys = list(self.peo2movie_final.keys())
        for item in tqdm(temp_keys):
            if item not in self.peo2book_final:
                self.peo2movie_final.pop(item)
        print('user:', len(self.peo2book_final), len(self.peo2movie_final))

        movie = []
        book = []

        for item in self.peo2movie_final.keys():
            movie += self.peo2movie_final[item]

        for item in self.peo2book_final.keys():
            book += self.peo2book_final[item]

        user = self.peo2book_final.keys()
        movie_inter = len(movie)
        book_inter = len(book)

        print('movie inter reserved:', len(movie), 'book inter reserved:', len(book))

        movie = list(set(k[0] for k in movie))
        book = list(set(k[0] for k in book))

        print('user #:', len(self.peo2movie_final),len(user),  'movie #:', len(self.movie2peo), len(movie), 'book #:', len(self.book2peo), len(book))
        print('movie density:', movie_inter*1.0/len(movie)/len(user), 'book density:', book_inter*1.0/len(book)/len(user))


        #dictionary saving

        movie = self.movie2peo.keys()
        book = self.book2peo.keys()
        movie2id = dict()
        book2id = dict()
        user2id = dict()

        for id, item in enumerate(movie):
            movie2id[item] = id
        for id, item in enumerate(book):
            book2id[item] = id
        for id, item in enumerate(user):
            user2id[item] = id


        pickle.dump(self.peo2movie_final, open(os.path.join(data_file, 'peo2movie.pkl'), 'wb'))
        pickle.dump(self.peo2book_final, open(os.path.join(data_file, 'peo2book.pkl'), 'wb'))
        pickle.dump(movie2id, open(os.path.join(data_file, 'movie2id.pkl'), 'wb'))
        pickle.dump(book2id, open(os.path.join(data_file, 'book2id.pkl'), 'wb'))
        pickle.dump(user2id, open(os.path.join(data_file, 'user2id.pkl'), 'wb'))

        for ele in ['movie', 'book']:
            peo2book = pickle.load(open(os.path.join(data_file, 'peo2{}.pkl'.format(ele)), 'rb'))
            book2id = pickle.load(open(os.path.join(data_file, '{}2id.pkl'.format(ele)), 'rb'))
            user2id = pickle.load(open(os.path.join(data_file, 'user2id.pkl'), 'rb'))
            peo2book_id, book2peo_id = {}, {}
            for user in tqdm(peo2book):
                peo2book_id[user2id[user]] = []
                for each in peo2book[user]:
                    peo2book_id[user2id[user]].append(book2id[each[0]])

            for user in tqdm(peo2book_id):
                for each in peo2book_id[user]:
                    if each not in book2peo_id.keys():
                        book2peo_id[each] = [user]
                    else:
                        book2peo_id[each].append(user)

            pickle.dump(peo2book_id, open(os.path.join(data_file, 'peo2{}_id.pkl'.format(ele)), 'wb'))
            pickle.dump(book2peo_id, open(os.path.join(data_file, '{}2peo_id.pkl'.format(ele)), 'wb'))



data = Dataset()
data.read_data()
