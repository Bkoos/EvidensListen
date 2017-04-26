#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from math import ceil
import requests
from pprint import pprint

class OdaWrapper(object):
	"""
	OdaWrapper er et lille script til på nemmere møde at aggregere
	data fra oda.ft.dk. Odata er servicen hvor Borgen lægger deres
	stemmer, sager og personer mv. op.
	De har nok med vilje gjort det lidt uoverskuelig, og dette
	script kræver stadig at man kender de forskellige tabeller.
	"""
	def __init__(self):
		self.base_url = u"http://oda.ft.dk/api/"
		self.all_url = u"?$inlinecount=allpages"
		self.filter_url = u"&$filter="

	def getAll(self, table, filterering=None, relation=None):
		""" getAll funktionen itererer igennem alle resultater fra forspørgslen
		Bruges til at hente alle elementer i en tabel fra oda.ft.dk

		Eksempel på at hente aktører fra perioden med id'et 144:
			$ getAll("Aktør", filter=["periodeid", "144"])

		Eksempel på at hente stemmer med ralation til aktør med id'et 12:
			$ getAll("Aktør", relation={id:"aktørid", table:"Stemme"})

		Atributter:
    		table (str): Tabel navn som 'Afstemning', 'Aktør', 'Sag', 'Møde', osv

			filter (list): filter er en liste af to strenge hvor den første
			er feltet og den anden er betingelsen: filter[0] eq filter[1]

			relation (dict): {id, table} hvor begge er strenge. "id" er den ralaterede
			tabels "foreign key" til den nuværende, og "tabel" er navnet på den
			relaterede tabel.
		"""

		url = u"%s%s%s" % (self.base_url, table, self.all_url)
		if relation is not None:
			url = u"%s%s(%i)/%s%s" % (self.base_url, table, relation["id"], relation["table"], self.all_url)
		if filterering is not None and isinstance(filtering, list):
			add = u"%s%s eq %s" % (self.filter_url, filtering[0], filtering[1])
			url += add
		elif filtering is not None and isinstance(filtering, str):
			url += self.filter_url + filtering
		result = requests.get(url).json()
		final = []
		for res in result['value']:
			final.append(res)
		if 'odata.count' in result:
			url_range = range(int(ceil(int(result['odata.count'])/20)+1))
			for u in url_range:
				skip = u"&$skip=%i" % (u*20)
				next_url = requests.get(url+skip).json()
				for res in next_url['value']:
					final.append(res)
		return final

	def getOne(self, table, t_id):
		"""Funktionen getOne henter én enkelt specificeret post.

		Eksempel:
		$ getOne("Forslag", 70764)

		Atributter:
			table (str): Tabel hvor der skal hentes et element
        	id (int): id på elementet. Lars Løkke har Aktør id 145
        """
		url = u"%s%s(%i)" % (self.base_url, table, t_id)
		return requests.get(url).json()

