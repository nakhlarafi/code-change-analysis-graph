import os
import javalang
from graphviz import Digraph
import json
import pickle
from tqdm import tqdm
import numpy as np
import json
from copy import deepcopy
import time
import io
import subprocess
import traceback
import pdb
linenode = ['WhileStatement', 'IfStatement', 'ConstructorDeclaration', 'ThrowStatement', 'Statement_ter', 'BreakStatement_ter', 'ReturnStatement_ter', 'ContinueStatement', 'ContinueStatement_ter', 'LocalVariableDeclaration', 'control', 'BreakStatement', 'ContinueStatement', 'ReturnStatement', "parameters", 'StatementExpression', 'return_type']
class Node:
    def __init__(self, name, d):
        self.name = name
        self.id = d
        self.father = None
        self.child = []
        self.sibiling = None
        self.expanded = False
        self.fatherlistID = 0
        self.treestr = ""
        self.block = ""
        self.num = 0
        self.fname = ""
        self.position = None
        self.isunique = ''
        self.possibility = 0
    def printTree(self, r):
      s = r.name + "" + " "
      if len(r.child) == 0:
        s += "^ "
        return s

      for c in r.child:
        s += self.printTree(c)
      s += "^ "
      return s
    def getNum(self):
        return len(self.getTreestr().strip().split())
    def getTreeProb(self, r):
      ans = [r.possibility]
      if len(r.child) == 0:
        return ans
      for c in r.child:
        ans += self.getTreeProb(c)
      return ans
    def getTreestr(self):
        if self.treestr == "":
            self.treestr = self.printTree(self)
            return self.treestr
        else:
            return self.treestr
    def printTreeWithVar(self, node, var):
        ans = ""
        if node.name in var:
            ans += var[node.name] + " "
        else:
            ans += node.name + " "
        for x in node.child:
            ans += self.printTreeWithVar(x, var)
        ans += '^ '  
        return ans
    def printTreeWithLine(self, node):
        ans = ""
        if node.position:
            ans += node.name + "-" + str(node.position.line)
        else:
            print(node.name)
            ans += node.name + "-"
        for x in node.child:
            ans += self.printTreeWithLine(x)
        ans += '^ '  
        return ans
    def printprob(self):
        ans = self.name + str(self.possibility) + ' '
        for x in self.child:
            ans += x.printprob()
        ans += '^ '
        return ans
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.name.lower() != other.name.lower():
            return False
        if len(self.child) != len(other.child):
            return False
        if True:
            return self.getTreestr().strip() == other.getTreestr().strip() 
def getroottree(tokens, isex=False):
    root = Node(tokens[0][0], 0)
    currnode = root
    idx = 1
    for i, x in enumerate(tokens[1:]):
        if x != "^":
            if isinstance(x, tuple):
                #assert(0)
                nnode = Node(x[0], idx)
                nnode.position = x[1]
            else:
                nnode = Node(x, idx)
            nnode.father = currnode
            currnode.child.append(nnode)
            currnode = nnode
            idx += 1
        else:
            currnode = currnode.father
    return root
def generateAST(tree):
    sub = []
    if not tree:
        return ['None', '^']
    if isinstance(tree, str):
        tmpStr = tree
        tmpStr = tmpStr.replace(" ", "").replace(":", "")
        if "\t" in tmpStr or "'" in tmpStr or "\"" in tmpStr:
            tmpStr = "<string>"
        if len(tmpStr) == 0:
            tmpStr = "<empty>"
        if tmpStr[-1] == "^":
            tmpStr += "<>"
        sub.append(tmpStr)
        sub.append("^")
        return sub
    if isinstance(tree, list):
        if len(tree) == 0:
            sub.append("empty")
            sub.append("^")
        else:
            for ch in tree:
                subtree = generateAST(ch)
                sub.extend(subtree)
        return sub
    position = None
    if hasattr(tree, 'position'):
        position = tree.position
    curr = type(tree).__name__
    if True:
        if False:
            assert(0)
        else:
            sub.append((curr, position))
            try:
                for x in tree.attrs:
                    if x == "documentation":
                        continue
                    if not getattr(tree, x):
                        continue
                    sub.append(x)
                    node = getattr(tree, x)
                    if isinstance(node, list):
                        if len(node) == 0:
                            sub.append("empty")
                            sub.append("^")
                        else:
                            for ch in node:
                                subtree = generateAST(ch)
                                sub.extend(subtree)
                    elif isinstance(node, javalang.tree.Node):
                        subtree = generateAST(node)
                        sub.extend(subtree)
                    elif not node:
                        continue
                    elif isinstance(node, str):
                        tmpStr = node
                        tmpStr = tmpStr.replace(" ", "").replace(":", "")
                        if "\t" in tmpStr or "'" in tmpStr or "\"" in tmpStr:
                            tmpStr = "<string>"
                        if len(tmpStr) == 0:
                            tmpStr = "<empty>"
                        if tmpStr[-1] == "^":
                            tmpStr += "<>"
                        sub.append(tmpStr)
                        sub.append("^")
                    elif isinstance(node, set):
                        for ch in node:
                            subtree = generateAST(ch)
                            sub.extend(subtree)
                    elif isinstance(node, bool):
                        sub.append(str(node))
                        sub.append("^")
                    else:
                        print(type(node))
                        assert(0)
                    sub.append("^")
            except AttributeError:
                assert(0)
                pass
        sub.append('^')
        return sub
    else:
        print(curr)
    return sub
def getMethodByline(filename, lineid):
    try:
        lines1 = open(filename, "r", encoding='iso-8859-1').read().strip()
        tokens = javalang.tokenizer.tokenize(lines1)
        parser = javalang.parser.Parser(tokens)
        # print(filename, lineid)
        tree = parser.parse()
        tmproot = getroottree(generateAST(tree))
        mnode = None
        index = 0
        while mnode is None and index < len(lineid):
            line = int(lineid[index].split(":")[1])
            currroot = getNodeById(tmproot, line)
            lnode, mnode = getSubroot(currroot)
            index += 1
        return mnode
    except:
        print(filename, lineid)
        return None
def getNodeById(root, line):
    if root.position:
        if root.position.line == line and root.name != 'IfStatement' and root.name != 'ForStatement' and root.name != 'WhileStatement' and root.name != 'SwitchStatement':
            return root
    for x in root.child:
        t = getNodeById(x, line)
        if t:
            return t
    return None
def getSubroot(treeroot):
    currnode = treeroot
    lnode = None
    mnode = None
    while currnode:
        if currnode.name in linenode:
            lnode = currnode
            break
        currnode = currnode.father
    currnode = treeroot
    while currnode:
        if currnode.name == 'MethodDeclaration' or currnode.name == 'ConstructorDeclaration':
            mnode = currnode
            break
        currnode = currnode.father
    return lnode, mnode
def getLnode(treeroot):
    currnode = treeroot
    lnode = None
    while currnode:

        if currnode.name in linenode:
            lnode = currnode
            break
        currnode = currnode.father
    return lnode
def getMask(mnode, masked):
    if mnode.position is not None:
        if mnode.position.line not in masked:
            masked[mnode.position.line] = mnode
    for x in mnode.child:
        getMask(x, masked)
    return
def simpleGraph(node):
    x = node
    if x.isunique == "" and not (x.father == 'IfStatement' and x.name != 'condition'):
        tnode = x.father
        c = []
        for ch in tnode.child:
            if ch == x:
                c.extend(x.child)
            else:
                c.append(ch)
        tnode.child = c
        for s in x.child:
            s.father = tnode
    for s in x.child:
        simpleGraph(s)
    return
def getEdge(node, edge, liness):
    if node.isunique != 'method':
        for x in node.child:
            if x.isunique in liness and node.isunique in liness:
                edge.append((liness[x.isunique], liness[node.isunique]))

    for x in node.child:
        getEdge(x, edge, liness)
def conEdge(mnode, root):
    ans = []
    if root != mnode:
        ans.append(root.isunique)
    for x in root.child:
        ans.extend(conEdge(mnode, x))
    return ans

prlist = ['Lang']
idss = [14, 19, 20, 21, 22, 24, 27, 29, 39, 41, 45, 51, 52]

ids = [[7]+ idss]

err = []

for i, xss in enumerate(prlist):
    res = []
    for idx in ids[i]:
        if idx == -1:
            continue
        try:
            timecurr = time.time()
            x = xss
            '''locationdir = 'location/ochiai/%s/%d.txt' % (x.lower(), idx)
            if not os.path.exists(locationdir):
                continue'''
            #print(open(locationdir, 'r').read())
            if xss == 'Closure':
                if not os.path.exists("0.2/%d.txt"%idx):
                    continue
                ms = open("0.2/%d.txt"%idx, "r").readlines()
                avaiableM = []
                for y in ms:
                    avaiableM.append(y.strip())        
            dirs = os.popen('defects4j export -p dir.src.classes -w lang_%d_copy'%idx).readlines()[-1]
            for methodnamess in [1]:
                tmp = {}
                patchdict = {}
                testcase = {}
                allmethods = {}
                line2method = {}
                tests = {}
                liness = {}
                ltype = {}
                f = open('FailedTests/%s.txt' % (idx))
                methods = open('AllMethods_grace/%s.txt' % (idx)).readlines()
                bmethods = []
                for x in methods:
                    lst = x.strip().split(":")
                    fname = lst[0] + ":" + lst[2] 
                    methodname = lst[0] + ":" + lst[1]
                    if  xss == "Closure" and methodname not in avaiableM:
                        continue
                    line2method[fname] = methodname
                buggypackage = {}
                for x in f:
                    if x.strip().replace("::", ".") not in tests:
                        tests[x.strip().replace("::", ".")] = len(tests)
                        name = ".".join(x.split("::")[0].split("."))
                        buggypackage[name] = 1
                f = open('CoverageFiles/%s.txt' % (idx), 'r')
                lines = f.readlines()
                methods = {}
                v = {}
                edge2 = []
                edge = []
                edge3 = []
                method2line = {}
                for x in lines:
                    lst = x.strip().split()
                    if '(' in lst[0]:
                        name = lst[0][:lst[0].index('(')]
                    else:
                        name = lst[0]
                    if name not in tests:
                        continue
                    for x in lst[1:]:
                        
                        lsts = x.strip().split(":")
                        fname = lsts[0] + ":" + lsts[2]
                        if fname not in line2method:
                            continue
                        if fname not in liness:
                            liness[fname] = len(liness)
                        methodname = line2method[fname]
                        if methodname not in methods:
                            methods[methodname] = len(methods)
                        edge2.append((liness[fname], tests[name]))
                        method2line.setdefault(methodname, []).append(fname)
                buggymethods = open('BugMethod/Lang/%s.txt' % (idx)).readlines() 
                print(methods)
                for x in buggymethods:
                    fname = x.strip()[6:]
                    x = fname
                    lst = x.strip().split(":")
                    fname = fname.replace('$','.')
                    if fname not in methods:
                        print("****%******")
                        print(fname)
                        continue
                    bmethods.append(methods[fname])
                if len(bmethods) == 0:
                    print('ho bhai')
                    assert(0)
                correctnum = {}
                rrdic = {}
                for x in line2method:
                    rrdic.setdefault(line2method[x], []).append(x)
                for xs in liness:
                    edge.append((methods[line2method[xs]], liness[xs]))
                for x in tqdm(methods):
                    print(x)
                    fpath = 'lang_%d_copy/'%idx + dirs + '/' + x.split(':')[0].split('$')[0].replace('.', '/') + ".java"
                    lineid = list(set(method2line[x]))
                    # print(fpath,lineid)
                    mnode = getMethodByline(fpath, lineid)
                    if mnode is None:
                        continue
                    for xs in lineid:
                        tnode = getNodeById(mnode, int(xs.split(":")[1]))
                        tnode = getLnode(tnode)
                        if tnode is None:
                            print(xs)
                            continue
                        ltype[liness[xs]] = tnode.name
                        tnode.isunique = xs
                    mnode.isunique = 'method'
                    simpleGraph(mnode)
                    print(mnode.printTree(mnode))
                    getEdge(mnode, edge3, liness)
                    ans = conEdge(mnode, mnode)
                    for xs in ans:
                        edge.append((methods[x], liness[xs]))
                    for j in range(len(mnode.child)):
                        if j == 0:
                            continue
                        edge3.append((liness[mnode.child[j].isunique], liness[mnode.child[j - 1].isunique]))
                lcorrect = {}
                rtest = {}
                edge10 = []
                for x in tqdm(lines):
                    lst = x.strip().split()
                    if '(' in lst[0]:
                        name = lst[0][:lst[0].index('(')]
                    else:
                        name = lst[0]
                    if name in tests:
                        continue
                    cnum = 0
                    if xss == 'Closure' and len(rtest) >= 300:
                        break
                    for x in lst[1:]:
                        lst2 = x.strip().split(":")
                        fname = lst2[0] + ":" + lst2[2]
                        if fname not in line2method:
                            continue
                        if fname in liness:
                            if fname not in lcorrect:
                                lcorrect[liness[fname]] = 0
                            lcorrect[liness[fname]] += 1
                            if name not in rtest:
                                rtest[name] = len(rtest)
                            edge10.append((liness[fname], rtest[name]))
                            cnum += 1
                        methodname = line2method[fname]
                        if methodname in methods:
                            if methods[methodname] in correctnum:
                                correctnum[methods[methodname]] += 1
                            else:
                                correctnum[methods[methodname]] = 0
                tmp['ftest'] = tests
                tmp['edge'] = set(edge2)
                tmp['edge2'] = set(edge)
                tmp['edge3'] = set(edge3)
                tmp['edge10'] = set(edge10)
                print(len(tmp['edge10']), len(liness), len(tmp['edge']), len(tmp['edge10']), len(tmp['edge2']), len(tmp['edge3']))
                tmp['proj'] = xss + str(idx)
                tmp['correctnum'] = correctnum
                tmp['ans'] = bmethods
                tmp['methods'] = methods
                tmp['lines'] = liness
                tmp['ltype'] = ltype
                tmp['lcorrectnum'] = lcorrect
                tmp['rtest'] = rtest
                print(len(rtest))
                res.append(tmp)
        except:
            print(traceback.print_exc(), xss, str(idx))
            err.append(xss + str(idx))
            assert(0)
            continue
        open('PklFiles_test_new/%s%d.pkl' % (xss, idx), 'wb').write(pickle.dumps(res))
print(err)
        
