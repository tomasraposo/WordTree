# Word Tree

This project is about an extension of binary search trees that is useful for storing strings.

We define a word tree to be a tree where:
* each node has three children: left, right and next;
* each node contains a character (the data of the node) and a non-negative integer (the multiplicity of the stored data)
* the left child of a node, if it exists, contains a character that is smaller (alphabetically) than the character of the node
* the right child of a node, if it exists, contains a character that is greater than the character of the node
