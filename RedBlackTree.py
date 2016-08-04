# Red Black Tree
# Author: David Allen
#
# Written with easy crossover to C/C++ and Java in mind
# Most class fields should be treated as private
# Follows the standard Binary Tree invariant
# Allows for duplicate entries
# Cousin refers to Uncle/Aunt node

class RedBlackTree:

    class Node:

        def __init__(self, value, isRedBool=True, parent=None, left=None, right=None):
            self.value = value
            self.isRedBool = isRedBool
            self.parent = parent
            self.left = left
            self.right = right

        def setRed(self):
            self.isRedBool = True

        def setBlack(self):
            self.isRedBool = False

        def takeColorOf(self, node):
            if node != None and node.isRed():
                self.isRedBool = True
            else:
                self.isRedBool = False

        def isRed(self):
            return self.isRedBool

        def getValue(self):
            return self.value

        def setValue(self, value):
            self.value = value

        def getParent(self):
            return self.parent

        def setParent(self, parent):
            self.parent = parent

        def getSibling(self):
            if self.parent != None:
                if self == self.parent.left:
                    return self.parent.right
                else:
                    return self.parent.left
            return None

        def getGrandparent(self):
            if self.parent != None:
                return self.parent.parent
            return None

        def getCousin(self): # Should be get Uncle/Aunt
            if self.parent == None:
                return None
            gp = self.getGrandparent()
            if gp == None:
                return None

            if self.parent == gp.left:
                return gp.right
            else:
                return gp.left

            


    def __init__(self):
        self.root = None
        self.size = 0       # Size in number of Nodes

    def insert(self, value):
        toAdd = self.Node(value)
        self.size += 1

        if self.root == None:
            self.root = toAdd
            toAdd.setBlack()
            return

        trav = self.root
        
        while trav != None:         # Insert the new node and set its parent
            nodeVal = trav.getValue()
            if nodeVal > value:     # go left
                if trav.left != None:
                    trav = trav.left
                else:
                    trav.left = toAdd
                    toAdd.setParent(trav)
                    trav = None
            else:                   # go right
                if trav.right != None:
                    trav = trav.right
                else:
                    trav.right = toAdd
                    toAdd.setParent(trav)
                    trav = None

        parent = toAdd.getParent()
        if parent != None and parent.isRed():
            self.rebalance(toAdd)       # rebalance the tree

    # Rebalance the tree at the new @node
    def rebalance(self, node):
        cousin = node.getCousin()
        parent = node.getParent()
        grand = node.getGrandparent()

        while node.isRed() and parent != None and parent.isRed():
            # Case 1 - If Cousin is red then recolor
            if cousin != None and cousin.isRed():
                print("Case 1 - Uncle is red")
                parent.setBlack()
                cousin.setBlack()
                grand.setRed()
                node = grand
            # Case 2 - zig zag left child of right child
            elif parent == grand.right and node == parent.left:
                print("Case 2 - Left child of right child")
                self.rightRotate(node)
                node = node.right
            # Case 3 - zig zag right child of left child
            elif parent == grand.left and node == parent.right:
                print("Case 3 - right child of left child")
                self.leftRotate(node)
                node = node.left
            # Case 4 - zig zig left child of left child
            elif parent == grand.left and node == parent.left:
                print("Case 4 - left of left")
                self.rightRotate(parent)
                grand.setRed()
                parent.setBlack()
                node = parent
            # Case 5 - zig zig right child of right child
            elif parent == grand.right and node == parent.right:
                print("Case 5 - right of right")
                self.leftRotate(parent)
                grand.setRed()
                parent.setBlack()
                node = parent

            cousin = node.getCousin()
            parent = node.getParent()
            grand = node.getGrandparent()
            
        self.root.setBlack()



    # Find the first instance of @value in the tree and remove it
    def remove(self, value):
        node = self.find(value)
        if node == None:
            return

        print("Removing " + str(value))

        # Moves a @child up into the @node position, deleting the @node
        def moveChildUp(parent, node, child):
            if child == None:
                child = self.Node(None, isRedBool=False)

            if parent.left == node:
                parent.left = child
            else:
                parent.right = child

            child.setParent(parent)
            return child

        def removeNullNode(node):
            parent = node.getParent()

            if node == parent.left:
                parent.left = None
            else:
                parent.right = None


        # Replace the node with the successor if it exists
        suc = self.successor(node)
        if suc != None:
            node.setValue(suc.getValue())
            node = suc

        # Here is where the majik happens
        # Find the non-None child if it exists
        if node.left == None:
            child = node.right
        else:
            child = node.left

        parent = node.getParent()

        # If the node to be removed is red then just delete it
        if node.isRed():
            moveChildUp(parent, node, child)

        # If the node to be removed is black then things get hairy
        else:
            # We are at the root with one child
            if parent == None: 
                self.root = child
                if child != None:
                    child.setBlack()
                    child.setParent(None)

            # The child is a red child. Replace node with child and set child to black
            elif child != None and child.isRed(): 
                moveChildUp(parent, node, child)
                child.setBlack()

            # Node is black and Child is black
            # 
            else:
                print("Black on black node")
                unstable = True
                sibling = node.getSibling()
                node = moveChildUp(parent, node, child)
                

                while unstable and parent != None:
                    # The node is black, the parent is black and the sibling is red
                    if sibling != None and sibling.isRed():
                        print("1: Parent is black but sibling is red")
                        parent.setRed()
                        sibling.setBlack()
                        if sibling == parent.left:
                            self.leftRotate(sibling)
                        else:
                            self.rightRotate(sibling)
                    # The parent, sibling and the siblings children are all black
                    elif not parent.isRed() and not sibling.isRed() and \
                        (sibling.left == None or not sibling.left.isRed()) and \
                        (sibling.right == None or not sibling.right.isRed()):
                        print("2: Parent, sibling and siblings children are all black")
                        sibling.setRed()
                        if node.getValue() == None:
                            removeNullNode(node)
                        node = parent
                    # The parent is red and the sibling and its children are black
                    elif parent.isRed() and not sibling.isRed() and \
                        (sibling.left == None or not sibling.left.isRed()) and \
                        (sibling.right == None or not sibling.right.isRed()):
                        print("3: Parent is red and sibling and its children are black")
                        sibling.setRed()
                        parent.setBlack()
                        unstable = False
                    # The sibling is black but its left child is red and its right child is black
                    # and the node is on the left of its parent
                    elif parent.left == node and not sibling.isRed() and \
                        (sibling.left != None and sibling.left.isRed()) and \
                        (sibling.right == None or not sibling.right.isRed()):
                        print("4: Sibling is black, Sibling right is red, node is on left side")
                        sibling.setRed()
                        sibling.left.setBlack()
                        self.rightRotate(sibling.left)
                    # The mirror of the case above
                    elif parent.right == node and not sibling.isRed() and \
                        (sibling.left == None or not sibling.left.isRed()) and \
                        (sibling.right != None and sibling.right.isRed()):
                        print("5: Sibling is black, Sibling right is red, node is on right side")
                        sibling.setRed()
                        sibling.right.setBlack()
                        self.leftRotate(sibling.right)
                    # The sibling is black, the siblings right child is red, left child is black,  
                    # and the node is on the left of its parent
                    elif parent.left == node and not sibling.isRed() and \
                        (sibling.left == None or not sibling.left.isRed()) and \
                        (sibling.right != None and sibling.right.isRed()):
                        print("6: Sibling is black, Sibling right is red, node is on left side")
                        sibling.takeColorOf(parent)
                        parent.setBlack()
                        sibling.right.setBlack()
                        self.leftRotate(sibling)
                        unstable = False
                    # Mirror of the above case
                    elif parent.right == node and not sibling.isRed() and \
                        (sibling.left != None and sibling.left.isRed()) and \
                        (sibling.right == None or not sibling.right.isRed()):
                        print("7: Sibling is black, Sibling left is red, node is on right side")
                        sibling.takeColorOf(parent)
                        parent.setBlack()
                        sibling.left.setBlack()
                        self.rightRotate(sibling)
                        unstable = False

                    parent = node.getParent()
                    sibling = node.getSibling()

                if node.getValue() == None:
                    removeNullNode(node)

                if self.root != None:
                    self.root.setBlack()


    # Right Rotate the tree at @node
    # @node is the node that will move up into the root position
    def rightRotate(self, node):
        parent = node.getParent()
        grandparent = node.getGrandparent()
        if parent == None:          # This is the root, abandon ship
            return

        if grandparent != None:
            if grandparent.right == parent:
                grandparent.right = node
            else:
                grandparent.left = node
        else:
            self.root = node

        node.setParent(grandparent)
        parent.setParent(node)
        parent.left = node.right
        node.right = parent

    # Left Rotate the tree at @node
    # @node is the node that will move up into the root position
    def leftRotate(self, node):
        parent = node.getParent()
        grandparent = node.getGrandparent()
        if parent == None:          # This is the root, abandon ship
            return

        if grandparent != None:
            if grandparent.right == parent:
                grandparent.right = node
            else:
                grandparent.left = node
        else:
            self.root = node

        node.setParent(grandparent)
        parent.setParent(node)
        parent.right = node.left
        node.left = parent

    # Find the first instance of @value in the tree
    # Return the Node if found or None
    def find(self, value):
        trav = self.root
        
        while trav != None:
            nodeVal = trav.getValue()
            if nodeVal > value:     # go left
                trav = trav.left
            elif value > nodeVal:   # go right
                trav = trav.right
            else:                   # element found
                return trav

        return None

    # Finds the first successor to a @node
    # Returns None if there is no successor
    def successor(self, node):
        trav = node.right

        if trav != None:
            while trav.left != None:
                trav = trav.left
        
        return trav

    def printInorder(self):
        def helper(node):
            if node == None:
                return

            helper(node.left)
            parent = node.getParent()
            if node.isRed():
                redstr = " Red"
            else:
                redstr = " Black"
            if parent != None:
                print("Node - " + str(node.value) + redstr + " Child of - " + str(parent.value))
            else:
                print("Node - " + str(node.value) + redstr + " Child of - None")
            helper(node.right)

        if self.root != None:
            helper(self.root)
        else:
            print("Tree is Empty")


# # make sure the test cases flow through every possible case
# r = RedBlackTree()
# #insert tests
# r.insert(1)
# r.insert(10)
# r.insert(2)
# r.insert(-10)
# r.insert(-2)
# r.insert(-5)
# r.insert(5)
# r.printInorder()

# #remove tests
# r.remove(-2)
# r.remove(10)
# r.remove(1)
# r.remove(2)

# r.printInorder()
# r.remove(5)
# r.remove(-5)
# r.printInorder()
# r.remove(-10)
# r.printInorder()












        
