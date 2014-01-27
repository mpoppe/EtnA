#
# Copyright (c) 2013 Marian Poppe (marian.poppe@uni-bielefeld.de)
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
#

from path import path
import codecs
import os

csv2txt = path.getcwd().files("*.CSV")
for path in csv2txt:
	print(path)
	parts = path.split('.')
	new_name = format(parts[0]) + ".txt"
	os.rename(path, new_name)

# processes all files in the working folder starting with 20, change path in accordance to your needs
filepaths = path.getcwd().files("20*.txt")

# list of conditions, change in accordance to your needs
code_eventtype = "14"
code_countrycode = ["AV", "AC", "AA", "BF", "BB", "VI", "CJ", "CU" ,"DO", "DR", "GJ", "GP", "HA", "JM", "MB", "MH", "RQ", "SC", "ST", "RN", "VC", "TD", "TK", "VQ", "BH", "CS", "ES", "GT", "HO", "MX", "NU", "PM", "AR", "BL", "BR", "CI", "CO", "EC", "FK", "FG", "GY", "PA", "PE", "NS", "UY", "VE", "BD" ,"CA", "GL", "SB", "US"]
minimum_coverage = 2
code_allowed_actors = ["ABW", "AMN", "ANT", "ARG", "ASM", "ATG", "ATH", "BLZ", "BMU", "BOL", "BRA", "BRB", "BUS", "CAN", "CHL", "CHR", "CMN", "COK", "COL", "CPA", "CPC", "CPT", "CRB", "CRI", "CTH", "CUB", "CVL", "DMA", "DOM", "DOX", "ECD", "ECU", "EDU", "ELI", "FAO", "FID", "FLK", "GLP", "GRD", "GRL", "GRP", "GTM", "GUF", "GUY", "HCH", "HCR", "HLH", "HND", "HRW", "HTI", "ICC", "ICG", "ICJ", "ICO", "IGC", "IGO", "IHF", "ILO", "INT", "IOM", "IRC", "JAM", "JEW", "JHW", "JUD", "KID", "LAB", "LAM", "LCA", "MED", "MEX", "MOD", "MRX", "MSF", "MSR", "MTQ", "NGM", "NGO", "NMR", "NON", "OAS", "OPC", "OPP", "PAN", "PER", "PRI", "PRO", "PRY", "RAD", "REB", "REF", "REL", "REU", "SAM", "SLV", "SUR", "UAF", "URY", "USA", "VCT", "VEN", "VGB", "VIR", "WCT", "WEF", "WFP", "WHO", "WSM", "XFM"]
code_excluded_actors =["GOV", "COP", "SPY", "MIL", "CRM", "NGO", "RAD", "LEG", "IGO", "JUD", "REB", "SEP", "MNC", "ELI", "IMG", "UAF"]

gdelt_header = "GLOBALEVENTID	SQLDATE	MonthYear	Year	FractionDate	Actor1Code	Actor1Name	Actor1CountryCode	Actor1KnownGroupCode	Actor1EthnicCode	Actor1Religion1Code	Actor1Religion2Code	Actor1Type1Code	Actor1Type2Code	Actor1Type3Code	Actor2Code	Actor2Name	Actor2CountryCode	Actor2KnownGroupCode	Actor2EthnicCode	Actor2Religion1Code	Actor2Religion2Code	Actor2Type1Code	Actor2Type2Code	Actor2Type3Code	IsRootEvent	EventCode	EventBaseCode	EventRootCode	QuadClass	GoldsteinScale	NumMentions	NumSources	NumArticles	AvgTone	Actor1Geo_Type	Actor1Geo_FullName	Actor1Geo_CountryCode	Actor1Geo_ADM1Code	Actor1Geo_Lat	Actor1Geo_Long	Actor1Geo_FeatureID	Actor2Geo_Type	Actor2Geo_FullName	Actor2Geo_CountryCode	Actor2Geo_ADM1Code	Actor2Geo_Lat	Actor2Geo_Long	Actor2Geo_FeatureID	ActionGeo_Type	ActionGeo_FullName	ActionGeo_CountryCode	ActionGeo_ADM1Code	ActionGeo_Lat	ActionGeo_Long	ActionGeo_FeatureID	DATEADDED SOURCE"
subset_output = open("subset.txt", "w", encoding="utf-8")
subset_output.write(gdelt_header + "\n")
counter = 0

for path in filepaths:
	database = open(path, 'r', encoding="utf-8")
	print("Processing new data...")
	for line in database:
		line = line.replace('\n', '')
		split_line = line.split('\t')
		condition1 = split_line[52] in code_countrycode
		condition2 = split_line[28] in code_eventtype
		condition3 = (int(split_line[32]) + int(split_line[33])) > minimum_coverage
		# Actor1Code has to be given
		condition4 = len(split_line[5]) > 0
		# Actor1CountryCode in list of allowed actors or empty
		condition5 = split_line[7] in code_allowed_actors or len(split_line[7]) == 0
		# Actor1Code not in list of excluded actors
		condition6 = split_line[12] not in code_excluded_actors
		# religion of Actor1 not specified
		condition7 = len(split_line[10]) == 0  
		# some information on Actor1 has to be given
		condition8 = (len(split_line[7]) + len(split_line[8]) + len(split_line[9]) + len(split_line[10]) + len(split_line[11]) + len(split_line[12]) + len(split_line[13]) + len(split_line[14]) + len(split_line[15]) + len(split_line[16]) + len(split_line[17]) + len(split_line[18]) + len(split_line[19]) + len(split_line[20]) + len(split_line[21]) + len(split_line[22]) + len(split_line[23]) + len(split_line[24])) > 3
		# add or remove in the following line the conditions you want to apply
		if all([condition1, condition2]):
			counter = counter + 1
			print(counter, "hits")
			subset_output.write(line + "\n")

subset_output.close()
