# -*- coding: utf-8 -*-
# -*- test-case-name: pytils.test.test_translit -*-
# pytils - russian-specific string utils
# Copyright (C) 2006-2009  Yury Yurevich
#
# http://pyobject.ru/projects/pytils/
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

TRANSTABLE = (
	# three-symbols replacements
	("Щ", "Shс"),
	# two-symbol replacements
	("Ё", "Yo"),
	("Ё", "YO"),
	("Ж", "Zh"),
	("Ж", "ZH"),
	("Ц", "Ts"),
	("Ц", "TS"),
	("Ч", "Ch"),
	("Ч", "CH"),
	("Ш", "Sh"),
	("Ш", "SH"),
	("Ы", "Y"),
	("Ы", "Y"),
	("Ю", "U"),
	("Ю", "U"),
	("Я", "Ya"),
	("Я", "YA"),
	# one-symbol replacements
	("А", "A"),
	("Б", "B"),
	("В", "V"),
	("Г", "G"),
	("Д", "D"),
	("Е", "E"),
	("З", "Z"),
	("И", "I"),
	("Й", "J"),
	("К", "K"),
	("Л", "L"),
	("М", "M"),
	("Н", "N"),
	("О", "O"),
	("П", "P"),
	("Р", "R"),
	("С", "S"),
	("Т", "T"),
	("У", "U"),
	("Ф", "F"),
	("Х", "H"),
	("Э", "E"),
	("Ъ", "`"),
	("Ь", "'"),
	## lower
	# three-symbols replacements
	("щ", "shc"),
	# two-symbols replacements
	("ё", "yo"),
	("ж", "zh"),
	("ц", "ts"),
	("ч", "ch"),
	("ш", "sh"),
	("ы", "y"),
	("ю", "u"),
	("я", "ya"),
	# one-symbol replacements
	("а", "a"),
	("б", "b"),
	("в", "v"),
	("г", "g"),
	("д", "d"),
	("е", "e"),
	("з", "z"),
	("и", "i"),
	("й", "j"),
	("к", "k"),
	("л", "l"),
	("м", "m"),
	("н", "n"),
	("о", "o"),
	("п", "p"),
	("р", "r"),
	("с", "s"),
	("т", "t"),
	("у", "u"),
	("ф", "f"),
	("х", "h"),
	("э", "e"),
	("ъ", "`"),
	("ь", "'"),
	) #: Translation table

def translify(in_string):
	translit = in_string
	for symb_in, symb_out in TRANSTABLE:
		translit = translit.replace(symb_in, symb_out)
	return translit
