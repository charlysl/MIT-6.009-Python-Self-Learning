#!/usr/bin/env python3
import lab
import unittest

class TestPanda(unittest.TestCase):
    def test_01(self):
        # play only unplayed song
        likes = [0]
        dislikes = []
        music = [[0], [1]]
        self.assertEqual(lab.next_song(likes, dislikes, music), 1)

    def test_02(self):
        # simple play next in lexicographic order (1/2)
        likes = [0]
        dislikes = []
        music = [[0],[1],[1],[1],[1],[1]]
        self.assertEqual(lab.next_song(likes, dislikes, music), 1)

    def test_03(self):
        # simple play next in lexicographic order (2/2)
        likes = [0,1,2]
        dislikes = []
        music = [[0],[1],[1],[1],[1],[1]]
        self.assertEqual(lab.next_song(likes, dislikes, music), 3)

    def test_04(self):
        # like distance with 1 gene
        likes = [0]
        dislikes = []
        music = [[1],[0],[1],[1],[0],[0]]
        self.assertEqual(lab.next_song(likes, dislikes, music), 2)

    def test_05(self):
        # like distance with 2 genes
        likes = [0]
        dislikes = []
        music = [[0,0],[1,1],[1,0],[0,1],[1,1]]
        self.assertEqual(lab.next_song(likes, dislikes, music), 2)

    def test_06(self):
        # like distance with 3 genes
        likes = [0]
        dislikes = []
        music = [[0,0,0],[1,1,1],[1,0,1],[0,1,1],[0,0,1]]
        self.assertEqual(lab.next_song(likes, dislikes, music), 4)

    def test_07(self):
        # dislike distance with 1 gene
        likes = []
        dislikes = [0]
        music = [[0],[0],[1],[1],[0],[0]]
        self.assertEqual(lab.next_song(likes, dislikes, music), 2)

    def test_08(self):
        # dislike distance with 2 genes
        likes = []
        dislikes = [0]
        music = [[0,0],[1,1],[1,0],[0,1],[1,1]]
        self.assertEqual(lab.next_song(likes, dislikes, music), 1)

    def test_09(self):
        # dislike distance with 3 genes
        likes = []
        dislikes = [0]
        music = [[0,0,0],[1,0,1],[1,0,1],[1,1,1],[1,1,0]]
        self.assertEqual(lab.next_song(likes, dislikes, music), 3)

    def test_10(self):
        # like and dislike distances
        likes = [1]
        dislikes = [0]
        music = [[0,0,0,0],[1,1,1,1],[0,0,0,1],[0,0,1,1],[1,1,0,1]]
        self.assertEqual(lab.next_song(likes, dislikes, music), 4)


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
