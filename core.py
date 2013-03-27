# -*- coding: utf-8 -*-
# Copyright (c) 2013 Molly White
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import codecs, logging, os
from tokenizer import Tokenizer
from tokenparser import Parser
from api import Document

def setup_logging():
    logger=logging.getLogger("W2L")
    logger.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s"
                                          ": %(message)s", datefmt="%I:%M:%S %p")
    consolehandler = logging.StreamHandler() 
    consolehandler.setFormatter(console_formatter)
    logger.addHandler(consolehandler)
    return logger

if __name__ == "__main__":
    logger = setup_logging()
    doc = Document()
    doc.organize()
    if not os.path.exists(os.curdir + '/raw'):
        logger.debug("Getting raw text files.")
        doc.call()
    if not os.path.exists(os.curdir + '/text'):
        logger.debug("Parsing JSON to TXT.")
        doc.json_to_text()
        
    # Open and read files
    tokenizer = Tokenizer()
    parser = Parser()
    if not os.path.exists(os.curdir + '/latex'):
        os.mkdir(os.curdir + '/latex')
    if not os.path.exists(os.curdir + '/latex'):
        os.mkdir(os.curdir + '/latex')
    #folders = sorted(os.listdir(path=(os.curdir + '/text')), key=int)
    folders = ['3']
    for folder in folders:
        files = ['0.txt']
#        files = sorted(os.listdir(path=(os.curdir + '/text/' + folder)), key=lambda x: int(x[0]))
        with codecs.open(os.curdir + '/latex/' + folder + '.tex', 'w+', 'utf-8') as outputfile:
            for file in files:
                logger.debug("Parsing " + folder + "/" + file + " to " + folder + ".tex.")
                with codecs.open(os.curdir + '/text/' + folder + '/' + file, 'r', 'utf-8') as f:
                    data = f.read()
                    token_list = tokenizer.analyze(data)
                    parser.begin(outputfile)
                    parser.dispatch(token_list)
    logger.debug("Parsing complete.")