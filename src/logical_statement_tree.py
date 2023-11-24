###
# ╭╴logical_statement_tree
# ╰--> A Tkinter GUI App that shows the prefix tree of a logical statement in 
#      A window, and creates a .svg file of the logical circuit of said logical statement
# ╭╴Oportunitas (Taib Izzat Samawi); 12/Nov/2023
# ╰--> @if_its | @its_surabaya
###

## Import all necessary packages
import ast
import re
import tkinter as tk
from schemdraw.parsing import logicparse
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
from matplotlib import image as mpimg

####---------------->Global-scope Entities<----------------####
## Create a global postfix var, this variable can be local, but is global for simplicity purposes
global postfix

## Create a global final_infix var. Final_infix is the one to be displayed in the window
global final_infix
final_infix = []

## Create global vars for the Graphical user interface
root_window = tk.Tk()
entry = tk.Entry(root_window)
app_label = tk.Label(
    root_window, 
    text="Logical Statement (+arithmetics!) Graphical User Interface", 
    font=("Readex Pro", 24, "bold")
)
sub_label = tk.Label(
    root_window, 
    text="*simplification rules are not implemented in this gui for continuity reasons. Also, circuit creation are not supported for arithmetic operations (pakek nanya 😅)", 
    font=("Readex Pro", 8, "italic")
)
name_label = tk.Label(
    root_window, text="5025221085 | Taib Izzat Samawi", font=("Readex Pro", 16, "bold")
)
entry_label = tk.Label(
    root_window, text="Please enter the statement in the box below:", font=("Readex Pro", 12)
)
canvas = tk.Canvas(root_window, width=1300, height=720)
####---------------->Global-scope Entities<----------------####

####---------------->General Methods<----------------####
## Check if a char is an operator
def isOperator(c):
    return (not c.isalpha()) and (not c.isdigit())

## Get the priority of the operators.
def getPriority(c):
    if c == '∨':
        return 3
    elif c == '∧':
        return 4
    elif c == '+' or c == '-':
        return 9
    elif c == '*' or c == '/' or c == '%':
        return 10
    elif c == '!' or c == '¬' or c == '~':
        return 11
    elif c == '→' or c == '^':
        return 12
    elif c == '↔':
        return 13
    return 0

## Convert a list into a tuple
def to_tuple(lst):
    return tuple(to_tuple(i) if isinstance(i, list) else i for i in lst)
####---------------->General Methods<----------------####

####---------------->Logical & Arithmetic Statement Manipulations<----------------####
## Return the postfix form of an infix/standard logical/arithmetic statement (basic data structures)
def infixToPostfix(infix):
    infix = '(' + infix + ')'
    l = len(infix)
    char_stack = []
    output = []
    
    for i in range(l):
        if infix[i].isalpha() or infix[i].isdigit():
            output += infix[i]
        elif infix[i] == '(':
            char_stack.append(infix[i])
        elif infix[i] == ')':
            while char_stack[-1] != '(':
                output += char_stack.pop()
            char_stack.pop()
        
        else:
            if isOperator(char_stack[-1]):
                if infix[i] == '^':
                    while getPriority(infix[i]) <= getPriority(char_stack[-1]):
                        output += char_stack.pop()
                else:
                    while getPriority(infix[i]) < getPriority(char_stack[-1]):
                        output += char_stack.pop()
                char_stack.append(infix[i])
        
    while len(char_stack) != 0:
        output += char_stack.pop()
    
    return output

## Convert given postfix array into the value of the global final_infix variable.
## The logic is the reverse of the one used in infixToPostfix(), 
## note that this uses Recursion instead of Stack/Queues looping
def postfixToFinalInfix(postfix_arr):
    ## If the postfix array is a 2-operand statement (a∨b | p∧q | etc)
    if len(postfix_arr) == 3:
        final_infix.append('(')
        ## Add the first operand into the final infix,
        ## if the first operand is a statement, break down that operand first using recursion.
        final_infix.append(
            postfixToFinalInfix(postfix_arr[2]) if len(postfix_arr[2]) > 1 else postfix_arr[2]
        )

        ## Add the operator in the middle of the current infix instance
        final_infix.append(postfix_arr[0])

        ## Add the second operand into the final infix,
        ## if the second operand is a statement, break down that operand first using recursion.
        final_infix.append(
            postfixToFinalInfix(postfix_arr[1]) if len(postfix_arr[1]) > 1 else postfix_arr[1]
        )
        final_infix.append(')')
    
    ## Else if the postfix array is a not/negation statement
    elif len(postfix_arr) == 2:
        final_infix.append('(')
        final_infix.append(postfix_arr[0]) #append the negation operator
        ## Add the first operand into the final infix,
        ## if the first operand is a statement, break down that operand first using recursion.
        final_infix.append(
            postfixToFinalInfix(postfix_arr[1]) if len(postfix_arr[1]) > 1 else postfix_arr[1]
        )
        final_infix.append(')')
    
    ## Else if the postfix array is a single operand/operator
    elif len(postfix_arr) == 1:
        final_infix.append(postfix_arr)

## Convert the final infix (global) into a string
def stringifyFinalInfix():
    string = ""
    final_infix_tup = to_tuple(final_infix)
    for i in final_infix_tup:
        if i != None:
            string += i
    return string
####---------------->Logical & Arithmetic Statement Manipulations<----------------####

####---------------->Binary Trees<----------------####
## Tree Node Data Type
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

## Create a binary tree (basic data structures implementation)
def createBinaryTree(node_data):
    if node_data is None:
        return None
    if (type(node_data) != tuple):
        value = node_data
        node = TreeNode(value)
    elif node_data[0] == '¬' or node_data[0] == '~' or node_data[0] == '!':
        value, left_data = node_data
        node = TreeNode(value)
        node.left = createBinaryTree(left_data)
    else:
        value, left_data, right_data = node_data
        node = TreeNode(value)
        node.left = createBinaryTree(left_data)
        node.right = createBinaryTree(right_data)
    return node

## Create a nested tree-tuple data type (parent, left_child, right_child) from the global postfix
def getTreeTup():
    output = []
    if isOperator(postfix[0]):
        if isOperator(postfix[1]):
            output.append(postfix[0])
            postfix.pop(0)
            output.append(getTreeTup())
        else:
            if postfix[0] == '!' or postfix[0] == '¬' or postfix[0] == '~':
                output.append(postfix[0])
                postfix.pop(0)
                output.append(postfix[0])
                postfix.pop(0)
                return output
            else:
                output.append(postfix[0])
                postfix.pop(0)
                output.append(postfix[0])
                postfix.pop(0)
    else:
        output.append(postfix[0])
        postfix.pop(0)
    
    if len(postfix) > 0:
        if isOperator(postfix[0]):
            output.append(getTreeTup())
        else:
            output.append(postfix[0])
            postfix.pop(0)
    return output

## Draw the binary tree on the given tkinter canvas (recursive)
def drawTree(node, x, y, canvas, level=1):
    if node is not None:
        ## Draw left child if exists
        if node.left:
            canvas.create_line(x, y, x + (600 / (2 ** level)), y + 75, fill="#CCC", width=3)
            drawTree(node.left, x + (600 / (2 ** level)), y + 75, canvas, level + 1)
        
        ## Draw right child if exists
        if node.right:
            canvas.create_line(x, y, x - (600 / (2 ** level)), y + 75, fill="#CCC", width=3)
            drawTree(node.right, x - (600 / (2 ** level)), y + 75, canvas, level + 1)
        
        ## Label the parent node (this is done last to ensure the label is on top of any child elem)
        canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="", width=2)
        canvas.create_text(x, y, text=str(node.value), font=("Readex Pro", 16))

## Convert any non-junction statement (if, if and only if) into (and, or, not) using de-morgan rule
def junctionizeBranch(logic_tree):
    print(f'start: {logic_tree}')
    for i in range(0, len(logic_tree)):
        print(logic_tree[i])
        print(type(logic_tree[i]))
        print()
        if type(logic_tree[i]) is list:
            print("list found, recursing")
            logic_tree[i] = junctionizeBranch(logic_tree[i])
        ## If found, convert (P→Q) into (¬P∨Q)
        if logic_tree[i] == '→':
            logic_tree[i] = '∨'
            if logic_tree[i + 2][0] == '¬':
                logic_tree[i + 2] = logic_tree[i + 2][1]
            else:
                logic_tree[i + 2] = ['¬', logic_tree[i + 2]]

        ## If found, convert (P↔Q) into ((P∧Q)∨¬(P∨Q))
        if (logic_tree[i] == '↔'):
            q = logic_tree[i + 1]
            p = logic_tree[i + 2]

            logic_tree[i] = '∨'
            logic_tree[i + 1] = ['¬', ['∨', q, p]]
            logic_tree[i + 2] = ['∧', q, p]
    return logic_tree

####---------------->Binary Trees<----------------####

####---------------->Graphical User Interface<----------------####
## Calculate
def getInputRaw():
    plt.close('all')
    input_text = entry.get()

    ## Delete all caches
    canvas.delete("all")
    global postfix
    postfix = None
    global final_infix 
    final_infix = []

    postfix = infixToPostfix(str(input_text))[::-1]
    postfix_arr = getTreeTup()
    postfixToFinalInfix(postfix_arr)
    final_infix.pop(len(final_infix) - 1)
    final_infix.pop(0)
    final_infix_str = stringifyFinalInfix()
    print(final_infix_str)

    canvas.create_text(650, 30, text=final_infix_str, font=("Readex Pro", 12))
    root = createBinaryTree(to_tuple(postfix_arr))
    drawTree(root, 650, 70, canvas)

## Junctionize then calculate
def getInputCirc():
    plt.close('all')
    input_text = entry.get()

    ## Delete all caches
    canvas.delete("all")
    global postfix
    postfix = None
    global final_infix 
    final_infix = []

    postfix = infixToPostfix(str(input_text))[::-1]

    postfix_arr = junctionizeBranch(getTreeTup())
    postfixToFinalInfix(postfix_arr)
    final_infix.pop(len(final_infix) - 1)
    final_infix.pop(0)
    final_infix_str = stringifyFinalInfix()
    print(final_infix_str)

    canvas.create_text(650, 30, text=final_infix_str, font=("Readex Pro", 12))
    with logicparse(final_infix_str, outlabel='$f$') as d:
        d.save('../bin/circuit.png')
        d.save('../bin/circuit.svg')

    root = createBinaryTree(to_tuple(postfix_arr))
    drawTree(root, 650, 70, canvas)
    
    img = mpimg.imread("../bin/circuit.png")
    plt.imshow(img)
    plt.show()
####---------------->Graphical User Interface<----------------####

####---------------->Main Function<----------------####
def main():
    app_label.pack()
    sub_label.pack()
    name_label.pack()
    entry_label.pack()
    entry.pack()
    entry_submit = tk.Button(
        root_window, text="find tree", command=getInputRaw, font=("Readex Pro", 8)
    )
    entry_submit.pack()
    entry_submit_1 = tk.Button(
        root_window, text="find tree and circuit", command=getInputCirc, font=("Readex Pro", 8))
    entry_submit_1.pack()
    canvas.pack()
    root_window.mainloop()

if __name__ == '__main__':
    main()
####---------------->Main Function<----------------####

## Testcases (feel free to use these to test the functionality of the app)
# (¬P∨S)→(Q∧R)
# (¬P∨S)
# (P∧P)↔P
# (P∨P)↔P
# P↔Q
# (P∧(R∨Q))↔((P∧R)∨(P∧Q))
# ((P∧R)∨(P∧Q))
# (F∧G)∧(F↔(¬G))
# (F∧G)∧(F∨(¬G))
# (F∧G)↔(F∨(¬G))
# (F↔G)↔(F↔(¬G))
# (F∧G)→(F∨(¬G))