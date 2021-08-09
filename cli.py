#!/usr/bin/env python3

"""
The plan:
	call updaters:
		py -m my_trello updater <something>

		daily update friends
			py -m my_trello updater friends_date

	edit data
		py -m my_trello editor <something>

		edit friends data
			py -m my_trello editor friends $argv
			send $argv to friend_cli
"""


import os
import sys
import click
import datetime


@click.group()
def cli():
	pass

@click.command()
def updater():
	click.echo("updating")
	click.echo("\te.g. updating friends date")
	click.echo("\te.g. synching reading boards")

@click.command()
def editor():
	click.echo("editing")
	click.echo("\te.g. edditing date for a friend")

cli.add_command(updater)
cli.add_command(editor)

def main():
	print("[*] I'm in cli.main")
	cli()

def test(args=None, debug=False):
	print("[*] test")

	import ipdb; ipdb.set_trace()

