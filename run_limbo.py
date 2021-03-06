#!/usr/bin/env python
import limbo
print(limbo.__file__)
#from limbo import main
import argparse

parser = argparse.ArgumentParser(description="Run the limbo chatbot for Slack")
parser.add_argument('--test', '-t', dest='test', action='store_true', required=False,
                    help='Enter command line mode to enter a limbo repl')
parser.add_argument('--hook', dest='hook', action='store', default='message',
                    help='Specify the hook to test. (Defaults to "message")')
parser.add_argument('-c', dest="command", help='run a single command')
parser.add_argument('--database', '-d', dest='database_name', default='limbo.sqlite3',
                    help="Where to store the limbo sqlite database. Defaults to limbo.sqlite")
parser.add_argument('--pluginpath', '-pp', dest='pluginpath', default=None,
                    help="The path where limbo should look to find its plugins")
args = parser.parse_args()

limbo.main(args)

