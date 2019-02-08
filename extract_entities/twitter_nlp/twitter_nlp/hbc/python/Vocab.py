class Vocab:
    def __init__(self, vocabFile=None):
        self.nextId = 1
        self.word2id = {}
        self.id2word = {}
        if vocabFile:
            for line in open(vocabFile):
                line = line.rstrip('\n')
                (word, wid) = line.split('\t')
                self.word2id[word] = int(wid)
                self.id2word[wid] = word
                self.nextId = max(self.nextId, int(wid) + 1)

    def GetID(self, word):
        if not word in self.word2id:
            self.word2id[word] = self.nextId
            self.nextId += 1
        return self.word2id[word]

    def HasWord(self, word):
        return word in self.word2id

    def HasId(self, wid):
        return wid in self.id2word

    def GetWord(self, wid):
        return self.id2word[wid]

    def SaveVocab(self, vocabFile):
        fOut = open(vocabFile, 'w')
        for word in self.word2id.keys():
            fOut.write("%s\t%s\n" % (word, self.word2id[word]))

    def GetVocabSize(self):
        return self.nextId-1

