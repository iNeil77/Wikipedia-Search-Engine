class TrieNode():
    def __init__(self):
        self.data = None
        self.pointers={}
        self.indexlist = []


class Trie():
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        self.rec_insert(word, self.root)
        return

    def rec_insert(self, word, node):
        if word[:1] not in node.pointers:
            newNode=TrieNode()
            newNode.data=word[:1]
            node.pointers[word[:1]]=newNode
            self.rec_insert(word, node)
        else:
            nextNode = node.pointers[word[:1]]
            if len(word[1:])==0:
                nextNode.pointers[' ']='__END__'
                return
            return self.rec_insert(word[1:], nextNode)

    def search(self, word):
        if len(word)==0:
            return False
        return self.rec_search(word,self.root)

    def rec_search(self, word, node):
        if word[:1] not in node.pointers:
            return False
        else:
            nextNode = node.pointers[word[:1]]
            if len(word[1:])==0:
                if ' ' in nextNode.pointers:
                    return True
                else:
                    return False
            return self.rec_search(word[1:],nextNode)

    def startsWith(self, prefix):
        if len(prefix)==0:
            return True
        return self.rec_search_prefix(prefix,self.root)

    def rec_search_prefix(self, word, node):
        if word[:1] not in node.pointers:
            return False
        else:
            if len(word[1:])==0:#still have remaining in the prefix
                return True
            nextNode = node.pointers[word[:1]]
            return self.rec_search_prefix(word[1:],nextNode)



def main():
    string = input()
    WikiTrie = Trie()
    WikiTrie.insert(string)

if __name__ == "__main__":
    main()
