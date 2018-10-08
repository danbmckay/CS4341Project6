import networkx as nx
import sys

def main():
    network_file = sys.argv[1]
    query_file = sys.argv[2]
    num_samples = sys.argv[3]

    with open(network_file, 'r') as f:
        for line in f:
            for word in line.split():
                print(word)

if __name__ == "__main__":
    main()
