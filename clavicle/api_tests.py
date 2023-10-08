import json
import tempfile
import unittest
from rest_framework.test import APIRequestFactory, APITestCase

test_data_example = """Significant	#NAME?	Difference	Proteins	Positions within proteins	Leading proteins	Protein	Protein names	Gene names	Sequence window	Phospho (STY) Probabilities	Unique identifier	Symbol color	Symbol type	Symbol size	Show label	Amino acid	Charge	Reverse	Potential contaminant	Multiplicity	Localization prob	PEP	Score	Delta score	Score for localization	Mass error [ppm]	Intensity	Position	log2 DMSO.01	log2 DMSO.02	log2 DMSO.03	log2 MK.01	log2 MK.02	log2 MK.03	log2 14H.01	log2 14H.02	log2 14H.03	DMSO.01	DMSO.02	DMSO.03	MK.01	MK.02	MK.03	14H.01	14H.02	14H.03	Comparison
	0.647858789	0.435528437	A0AVK6	102	A0AVK6	A0AVK6	Transcription factor E2F8	E2F8	RSGLPEAKDCIHEHLSGDEFEKSQPSRKEKS	DCIHEHLS(1)GDEFEK	UID1	"Color2 [A=255, R=128, G=128, B=128]"	9	4		S	4			___1	1	2.58E-17	191.37	150.41	114.69	-0.29769	176170000	102	20.66092	21.21276	21.18126	20.70919	21.16693	20.90808	20.73496	20.91101	20.10239	1657893.611	2430396.051	2377905.58	1714302.174	2354403.237	1967701.568	1745198.853	1971701.876	1125699.244	1
	1.224866627	0.219369253	A0FGR8-2;A0FGR8;A0FGR8-6;A0FGR8-5	730;758;779;165	A0FGR8-2	A0FGR8-2	Extended synaptotagmin-2	ESYT2	SPGHISVKEPTPSIASDISLPIATQELRQRL	EPT(0.179)PS(0.827)IAS(0.998)DIS(0.995)LPIAT(0.001)QELR	UID6	"Color2 [A=255, R=128, G=128, B=128]"	9	4		S	3			___1	0.998404	9.04E-16	140.3	116.23	63.906	0.30499	1164600000	730	15.82729	15.7402	15.91205	15.83474	15.7688	15.91113	15.69919	15.47453	15.64771	58141.87593	54735.90937	61660.11672	58442.89402	55831.82134	61620.80888	53201.8945	45530.00508	51336.95123	1
	1.484787301	-0.352637927	A0FGR8-2	14	A0FGR8-2	A0FGR8-2	Extended synaptotagmin-2	ESYT2	__MTPPSRAEAGVRRSRVPSEGRWRGAEPPG	S(0.971)RVPS(0.029)EGR	UID8	"Color2 [A=255, R=128, G=128, B=128]"	9	4		S	3			___1	0.970816	0.0145773	52.937	30.55	52.937	-0.16217	6106600	14	15.05676	14.88751	14.99241	15.06861	14.90769	14.37137	15.52769	15.24626	15.22064	34082.88879	30310.07917	32596.06066	34363.9915	30737.02682	21194.02532	47238.97367	38867.05024	38182.92489	1
	1.612962058	-0.340634028	A0FGR8-2	18	A0FGR8-2	A0FGR8-2	Extended synaptotagmin-2	ESYT2	PPSRAEAGVRRSRVPSEGRWRGAEPPGISAS	SRVPS(1)EGR	UID9	"Color2 [A=255, R=128, G=128, B=128]"	9	4		S	2			___1	0.999997	0.00135458	108.43	35.503	103.26	-0.020584	20765000	18	16.93284	16.8439	16.98137	16.54906	16.61108	16.26615	17.39423	17.09455	17.29123	125110.2096	117630.2836	129390.3053	95887.8233	100099.8301	78813.21864	172260.2136	139949.8097	160390.5926	1
	0.329013292	-0.14700381	A0JNW5	989	A0JNW5	A0JNW5	UHRF1-binding protein 1-like	UHRF1BP1L	KISEDESSGLVYKSGSGEIGSETSDKKDSFY	S(0.026)GS(0.974)GEIGSETSDKK	UID11	"Color2 [A=255, R=128, G=128, B=128]"	9	4		S	3			___1	0.973973	7.16E-07	126.71	79.445	94.01	0.17804	48534000	989	18.39632	18.02567	18.26064	18.36521	18.31004	18.14096	18.28473	18.17407	18.66484	345019.888	266850.0951	314051.1442	337659.5883	324990.9458	289050.0908	319339.1703	295760.5283	415601.1152	1"""


class RawData(APITestCase):
    databases = {'clavicle'}
    def test_upload(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".txt")
        tmp.write(test_data_example.encode())
        tmp.seek(0)
        self.client.post("/api/rawdata/", {
            "name": "test",
            "description": "test",
            "file": tmp,
            "index_col": "Unique identifier",
            "metadata": json.dumps({
            }),
            "file_type": "txt",
            "sample_cols": json.dumps([
                    {"name": "DMSO.01", "group": "DMSO"},
                    {"name": "DMSO.02", "group": "DMSO"},
                    {"name": "DMSO.03", "group": "DMSO"},
                    {"name": "MK.01", "group": "MK"},
                    {"name": "MK.02", "group": "MK"},
                    {"name": "MK.03", "group": "MK"},
                    {"name": "14H.01", "group": "14H"},
                    {"name": "14H.02", "group": "14H"},
                    {"name": "14H.03", "group": "14H"},
                ])
        }, format="multipart")


if __name__ == '__main__':
    unittest.main()
