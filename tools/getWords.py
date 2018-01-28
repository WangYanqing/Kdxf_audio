#!/usr/python
#coding: utf8


from xml.dom import minidom
import re

path = r'/Users/wangyanqing/AndroidStudioProjects/WAudioTest/app/src/main/assets/gs_dbs_fs_goodsbaseinfo.xml'
path_out_txt = 'words.txt'
path_out_abnf = 'words.abnf'

words = []
print '------start---------'
doc = minidom.parse(path)
goods_list = doc.getElementsByTagName('goods')

# doc_out = minidom.Document()
# element0 = doc_out.createElement('root')
# doc_out.appendChild(element0)
# element1 = doc_out.createElement('goodslist')
# element0.appendChild(element1)


def getStrippedName(word):
	if word == None or word == '' or word.strip() == '':
		return None

	word = unicode(word)
	#Keep the prev part before *
	idx_asterisk = word.find('*')
	if idx_asterisk > 0:
		word = word[:idx_asterisk]

	#Keep the prev part before （
	idx_left_parenthese = word.find(unicode('（', 'utf8'))
	if idx_left_parenthese > 0:
		word = word[:idx_left_parenthese]

	idx_left_half_parenthese = word.find('(')
	if idx_left_half_parenthese > 0:
		word = word[:idx_left_half_parenthese]

	word = word.replace('!', '')
	word = word.replace(',', '')
	word = word.replace('?', '')
	word = word.replace('&', '')

	return word


def makeFile(words, bAnbf = True):
	out_file = open(bAnbf and path_out_abnf or path_out_txt, 'w')
	if bAnbf:
		out_file.write('#ABNF 1.0 UTF-8;\n'
			+ 'language zh-CN;\n'
			+ 'mode voice;\n'
			+ 'root $main;\n'
			+ '$main = $place1;\n'
			+ '$place1 = '
			)

	for i in range(len(words)):
		if bAnbf:
			if i == len(words) - 1:
				out_file.write(words[i].encode('utf8') + ';')
			else:
				out_file.write(words[i].encode('utf8') + '|')
		else:
			out_file.write(words[i].encode('utf8') + '\n')
	out_file.flush()
	out_file.close()


print '------Parse------'

for g in goods_list:
	id = g.getAttribute('ID')
	name = g.getAttribute('name')
	type = g.getAttribute('TypeID')

	type = int(type)
	if type == 26 or type == 43 or type == 36: #23礼包，43宝箱
		continue

	name = getStrippedName(name)
	sch0 = re.search('\d+', name)
	sch1 = re.search('[a-zA-Z]+', name)
	if (name != None and name != '') \
		and sch0 == None \
		and sch1 == None \
		and not (name in words):
		# words.append(getStrippedName(name))
		words.append(name)
	# if type == 14:
	# 	g0 = doc_out.createElement(g.tagName)
	# 	element1.appendChild(g0)
	# 	for k in g._attrs.keys():
	# 		g0.setAttribute(k, g.getAttribute(k))
	# 	break


print('--#words=%d' % len(words))
# print(words)
# print(doc_out.toprettyxml())

print '------Write------'
# out_file = open(path_out, 'w')
# for w in words:
# 	out_file.write(w.encode('utf8') + '\n')
# out_file.flush()
# out_file.close()
makeFile(words, False)
print '------End------'