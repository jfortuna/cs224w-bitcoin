import networkx as nx
import itertools as it

import random
import graphtools
import numpy as np

_START_ACTIVITY = 20110401

def generate_weighted_time_slices():
    slices = []
    early = _days[:_days.index(20110401)]
    section = len(early) / 24
    low = 0
    high = section
    for i in range(24):
        valid_days = early[low:section]
        start = random.choice(valid_days)
        next_index = valid_days.index(start)+5
        end = valid_days[valid_days.index(start)+5] if len(valid_days) -1 >= next_index  else valid_days[-1]
        slices.append((start, end))
        low += section_length
        high += section_length
    rest = _days[_days.index(20110401):]
    section = len(rest) / 200
    low = 0
    high = section
    for i in range(150):
        valid_days = rest[low:section]
        start = random.choice(valid_days)
        next_index = valid_days.index(start)+5
        end = valid_days[valid_days.index(start)+5] if len(valid_days) -1 >= next_index  else valid_days[-1]
        slices.append((start, end))
        low += section_length
        high += section_length




def generate_time_slices(slice_time=1, num_intervals=10, num_in_slice=10):
  """ Returns a list of tuples that represent time slices from the
      graph.

      parameters:
        slice_time: the number of days that should be included in each
                    time slice.
        num_intervals: the number of intervals the entire graph should
                       be sliced into
        num_in_slice: the number of sections to be taken from that slice
      returns:
        list of tuples of (start, end)
  """
  slices = []
  low = 0
  section_length = len(_days) / num_intervals
  high = section_length
  for interval in range(num_intervals):
    valid_days = _days[low:high]
    for section in range(num_in_slice):
      start = random.choice(valid_days)
      next_index = valid_days.index(start)+5
      end = valid_days[valid_days.index(start)+5] if len(valid_days) -1 >= next_index  else valid_days[-1]
      slices.append((start, end))
#      end = np.datetime64(graphtools.string_to_datetime(str(start))) + np.timedelta64(slice_time, 'D')
 #     slices.append((start, int(str(end)[:10].replace('-',''))))
    low += section_length
    high += section_length
  return slices

def random_slices(slice_time=1, num_slices=100):
  slices = []
  for i in range(num_slices):
    start = random.choice(_days)
    end = np.datetime64(graphtools.string_to_datetime(str(start))) + np.timedelta64(slice_time, 'D')
    slices.append((start, str(end)[:10].replace('-','')))
  return slices



def get_graph_slice(start, end):
    """
    Generate a networkx digraph of the bitcoin data with all transactions
    between start and end. Assumes you have bitcoin data in Bitoin
    folder. Check it.
    """
    g_slice = nx.MultiDiGraph()

    for filename in _get_files(start, end):
        with open(filename) as fp:
            for line in fp:
                vals = line.strip().split(',')
                if len(vals) == 5:
                    if int(vals[3]) < start or int(vals[3]) > end:
                        continue
                    g_slice.add_edge(vals[1], vals[2], value=float(vals[4]), date=vals[3], transaction_key=int(vals[0]))
    return g_slice


def add_slice_to_graph(graph, start, end):
    for filename in _get_files(start, end):
        with open(filename) as fp:
            for line in fp:
                vals = line.strip().split(',')
                if len(vals) == 5:
                    if int(vals[3]) < start or int(vals[3]) > end:
                        continue
                    graph.add_edge(vals[1], vals[2], value=float(vals[4]), date=vals[3], transaction_key=int(vals[0]))
    return graph


def _get_files(start, end):
    """
    Returns a list of filenames containing all transaction data between
    the two given dates.
    """    
    start_index, end_index = _days.index(start / _HMS) , _days.index(end / _HMS)
    return map(lambda day: _prefix + str(day), _days[start_index : end_index + 1])



# Constant for removing the hours, minutes, and seconds from a date
_HMS = 1000000
    
    
# This prefix is the location of the split user_edges data
_prefix = '../../Bitcoin/split/'
#_prefix = './'


# The definition of good style. List of all calendar days with data
_days = [20090103, 20090108, 20090109, 20090110, 20090111, 20090112,
    20090113, 20090114, 20090115, 20090116, 20090117, 20090118, 20090119,
    20090120, 20090121, 20090122, 20090123, 20090124, 20090125, 20090126,
    20090127, 20090128, 20090129, 20090130, 20090131, 20090201, 20090202,
    20090203, 20090204, 20090205, 20090206, 20090207, 20090208, 20090209,
    20090210, 20090211, 20090212, 20090213, 20090214, 20090215, 20090216,
    20090217, 20090218, 20090219, 20090220, 20090221, 20090222, 20090223,
    20090224, 20090225, 20090226, 20090227, 20090228, 20090301, 20090302,
    20090303, 20090304, 20090305, 20090306, 20090307, 20090308, 20090309,
    20090310, 20090311, 20090312, 20090313, 20090314, 20090315, 20090316,
    20090317, 20090318, 20090319, 20090320, 20090321, 20090322, 20090323,
    20090324, 20090325, 20090326, 20090327, 20090328, 20090329, 20090330,
    20090331, 20090401, 20090402, 20090403, 20090404, 20090405, 20090406,
    20090407, 20090408, 20090409, 20090410, 20090411, 20090412, 20090413,
    20090414, 20090415, 20090416, 20090417, 20090418, 20090419, 20090420,
    20090421, 20090422, 20090423, 20090424, 20090425, 20090426, 20090427,
    20090428, 20090429, 20090430, 20090501, 20090502, 20090503, 20090504,
    20090505, 20090506, 20090507, 20090508, 20090509, 20090510, 20090511,
    20090512, 20090513, 20090514, 20090515, 20090516, 20090517, 20090518,
    20090519, 20090520, 20090521, 20090522, 20090523, 20090524, 20090525,
    20090526, 20090527, 20090528, 20090529, 20090530, 20090531, 20090601,
    20090602, 20090603, 20090604, 20090605, 20090606, 20090607, 20090608,
    20090609, 20090610, 20090611, 20090612, 20090613, 20090614, 20090615,
    20090616, 20090617, 20090618, 20090619, 20090620, 20090621, 20090622,
    20090623, 20090624, 20090625, 20090626, 20090627, 20090628, 20090629,
    20090630, 20090701, 20090702, 20090703, 20090704, 20090705, 20090706,
    20090707, 20090708, 20090709, 20090710, 20090711, 20090712, 20090713,
    20090714, 20090715, 20090716, 20090717, 20090718, 20090719, 20090720,
    20090721, 20090722, 20090723, 20090724, 20090725, 20090726, 20090727,
    20090728, 20090729, 20090730, 20090731, 20090801, 20090802, 20090803,
    20090804, 20090805, 20090806, 20090807, 20090808, 20090809, 20090810,
    20090811, 20090812, 20090813, 20090814, 20090815, 20090816, 20090817,
    20090818, 20090819, 20090820, 20090821, 20090822, 20090823, 20090824,
    20090825, 20090826, 20090827, 20090828, 20090829, 20090830, 20090831,
    20090901, 20090902, 20090903, 20090904, 20090905, 20090906, 20090907,
    20090908, 20090909, 20090910, 20090911, 20090912, 20090913, 20090914,
    20090915, 20090916, 20090917, 20090918, 20090919, 20090920, 20090921,
    20090922, 20090923, 20090924, 20090925, 20090926, 20090927, 20090928,
    20090929, 20090930, 20091001, 20091002, 20091003, 20091004, 20091005,
    20091006, 20091007, 20091008, 20091009, 20091010, 20091011, 20091012,
    20091013, 20091014, 20091015, 20091016, 20091017, 20091018, 20091019,
    20091020, 20091021, 20091022, 20091023, 20091024, 20091025, 20091026,
    20091027, 20091028, 20091029, 20091030, 20091031, 20091101, 20091102,
    20091103, 20091104, 20091105, 20091106, 20091107, 20091108, 20091109,
    20091110, 20091111, 20091112, 20091113, 20091114, 20091115, 20091116,
    20091117, 20091118, 20091119, 20091120, 20091121, 20091122, 20091123,
    20091124, 20091125, 20091126, 20091127, 20091128, 20091129, 20091130,
    20091201, 20091202, 20091203, 20091204, 20091205, 20091206, 20091207,
    20091208, 20091209, 20091210, 20091211, 20091212, 20091213, 20091214,
    20091215, 20091216, 20091217, 20091218, 20091219, 20091220, 20091221,
    20091222, 20091223, 20091224, 20091225, 20091226, 20091227, 20091228,
    20091229, 20091230, 20091231, 20100101, 20100102, 20100103, 20100104,
    20100105, 20100106, 20100107, 20100108, 20100109, 20100110, 20100111,
    20100112, 20100113, 20100114, 20100115, 20100116, 20100117, 20100118,
    20100119, 20100120, 20100121, 20100122, 20100123, 20100124, 20100125,
    20100126, 20100127, 20100128, 20100129, 20100130, 20100131, 20100201,
    20100202, 20100203, 20100204, 20100205, 20100206, 20100207, 20100208,
    20100209, 20100210, 20100211, 20100212, 20100213, 20100214, 20100215,
    20100216, 20100217, 20100218, 20100219, 20100220, 20100221, 20100222,
    20100223, 20100224, 20100225, 20100226, 20100227, 20100228, 20100301,
    20100302, 20100303, 20100304, 20100305, 20100306, 20100307, 20100308,
    20100309, 20100310, 20100311, 20100312, 20100313, 20100314, 20100315,
    20100316, 20100317, 20100318, 20100319, 20100320, 20100321, 20100322,
    20100323, 20100324, 20100325, 20100326, 20100327, 20100328, 20100329,
    20100330, 20100331, 20100401, 20100402, 20100403, 20100404, 20100405,
    20100406, 20100407, 20100408, 20100409, 20100410, 20100411, 20100412,
    20100413, 20100414, 20100415, 20100416, 20100417, 20100418, 20100419,
    20100420, 20100421, 20100422, 20100423, 20100424, 20100425, 20100426,
    20100427, 20100428, 20100429, 20100430, 20100501, 20100502, 20100503,
    20100504, 20100505, 20100506, 20100507, 20100508, 20100509, 20100510,
    20100511, 20100512, 20100513, 20100514, 20100515, 20100516, 20100517,
    20100518, 20100519, 20100520, 20100521, 20100522, 20100523, 20100524,
    20100525, 20100526, 20100527, 20100528, 20100529, 20100530, 20100531,
    20100601, 20100602, 20100603, 20100604, 20100605, 20100606, 20100607,
    20100608, 20100609, 20100610, 20100611, 20100612, 20100613, 20100614,
    20100615, 20100616, 20100617, 20100618, 20100619, 20100620, 20100621,
    20100622, 20100623, 20100624, 20100625, 20100626, 20100627, 20100628,
    20100629, 20100630, 20100701, 20100702, 20100703, 20100704, 20100705,
    20100706, 20100707, 20100708, 20100709, 20100710, 20100711, 20100712,
    20100713, 20100714, 20100715, 20100716, 20100717, 20100718, 20100719,
    20100720, 20100721, 20100722, 20100723, 20100724, 20100725, 20100726,
    20100727, 20100728, 20100729, 20100730, 20100731, 20100801, 20100802,
    20100803, 20100804, 20100805, 20100806, 20100807, 20100808, 20100809,
    20100810, 20100811, 20100812, 20100813, 20100814, 20100815, 20100816,
    20100817, 20100818, 20100819, 20100820, 20100821, 20100822, 20100823,
    20100824, 20100825, 20100826, 20100827, 20100828, 20100829, 20100830,
    20100831, 20100901, 20100902, 20100903, 20100904, 20100905, 20100906,
    20100907, 20100908, 20100909, 20100910, 20100911, 20100912, 20100913,
    20100914, 20100915, 20100916, 20100917, 20100918, 20100919, 20100920,
    20100921, 20100922, 20100923, 20100924, 20100925, 20100926, 20100927,
    20100928, 20100929, 20100930, 20101001, 20101002, 20101003, 20101004,
    20101005, 20101006, 20101007, 20101008, 20101009, 20101010, 20101011,
    20101012, 20101013, 20101014, 20101015, 20101016, 20101017, 20101018,
    20101019, 20101020, 20101021, 20101022, 20101023, 20101024, 20101025,
    20101026, 20101027, 20101028, 20101029, 20101030, 20101031, 20101101,
    20101102, 20101103, 20101104, 20101105, 20101106, 20101107, 20101108,
    20101109, 20101110, 20101111, 20101112, 20101113, 20101114, 20101115,
    20101116, 20101117, 20101118, 20101119, 20101120, 20101121, 20101122,
    20101123, 20101124, 20101125, 20101126, 20101127, 20101128, 20101129,
    20101130, 20101201, 20101202, 20101203, 20101204, 20101205, 20101206,
    20101207, 20101208, 20101209, 20101210, 20101211, 20101212, 20101213,
    20101214, 20101215, 20101216, 20101217, 20101218, 20101219, 20101220,
    20101221, 20101222, 20101223, 20101224, 20101225, 20101226, 20101227,
    20101228, 20101229, 20101230, 20101231, 20110101, 20110102, 20110103,
    20110104, 20110105, 20110106, 20110107, 20110108, 20110109, 20110110,
    20110111, 20110112, 20110113, 20110114, 20110115, 20110116, 20110117,
    20110118, 20110119, 20110120, 20110121, 20110122, 20110123, 20110124,
    20110125, 20110126, 20110127, 20110128, 20110129, 20110130, 20110131,
    20110201, 20110202, 20110203, 20110204, 20110205, 20110206, 20110207,
    20110208, 20110209, 20110210, 20110211, 20110212, 20110213, 20110214,
    20110215, 20110216, 20110217, 20110218, 20110219, 20110220, 20110221,
    20110222, 20110223, 20110224, 20110225, 20110226, 20110227, 20110228,
    20110301, 20110302, 20110303, 20110304, 20110305, 20110306, 20110307,
    20110308, 20110309, 20110310, 20110311, 20110312, 20110313, 20110314,
    20110315, 20110316, 20110317, 20110318, 20110319, 20110320, 20110321,
    20110322, 20110323, 20110324, 20110325, 20110326, 20110327, 20110328,
    20110329, 20110330, 20110331, 20110401, 20110402, 20110403, 20110404,
    20110405, 20110406, 20110407, 20110408, 20110409, 20110410, 20110411,
    20110412, 20110413, 20110414, 20110415, 20110416, 20110417, 20110418,
    20110419, 20110420, 20110421, 20110422, 20110423, 20110424, 20110425,
    20110426, 20110427, 20110428, 20110429, 20110430, 20110501, 20110502,
    20110503, 20110504, 20110505, 20110506, 20110507, 20110508, 20110509,
    20110510, 20110511, 20110512, 20110513, 20110514, 20110515, 20110516,
    20110517, 20110518, 20110519, 20110520, 20110521, 20110522, 20110523,
    20110524, 20110525, 20110526, 20110527, 20110528, 20110529, 20110530,
    20110531, 20110601, 20110602, 20110603, 20110604, 20110605, 20110606,
    20110607, 20110608, 20110609, 20110610, 20110611, 20110612, 20110613,
    20110614, 20110615, 20110616, 20110617, 20110618, 20110619, 20110620,
    20110621, 20110622, 20110623, 20110624, 20110625, 20110626, 20110627,
    20110628, 20110629, 20110630, 20110701, 20110702, 20110703, 20110704,
    20110705, 20110706, 20110707, 20110708, 20110709, 20110710, 20110711,
    20110712, 20110713, 20110714, 20110715, 20110716, 20110717, 20110718,
    20110719, 20110720, 20110721, 20110722, 20110723, 20110724, 20110725,
    20110726, 20110727, 20110728, 20110729, 20110730, 20110731, 20110801,
    20110802, 20110803, 20110804, 20110805, 20110806, 20110807, 20110808,
    20110809, 20110810, 20110811, 20110812, 20110813, 20110814, 20110815,
    20110816, 20110817, 20110818, 20110819, 20110820, 20110821, 20110822,
    20110823, 20110824, 20110825, 20110826, 20110827, 20110828, 20110829,
    20110830, 20110831, 20110901, 20110902, 20110903, 20110904, 20110905,
    20110906, 20110907, 20110908, 20110909, 20110910, 20110911, 20110912,
    20110913, 20110914, 20110915, 20110916, 20110917, 20110918, 20110919,
    20110920, 20110921, 20110922, 20110923, 20110924, 20110925, 20110926,
    20110927, 20110928, 20110929, 20110930, 20111001, 20111002, 20111003,
    20111004, 20111005, 20111006, 20111007, 20111008, 20111009, 20111010,
    20111011, 20111012, 20111013, 20111014, 20111015, 20111016, 20111017,
    20111018, 20111019, 20111020, 20111021, 20111022, 20111023, 20111024,
    20111025, 20111026, 20111027, 20111028, 20111029, 20111030, 20111031,
    20111101, 20111102, 20111103, 20111104, 20111105, 20111106, 20111107,
    20111108, 20111109, 20111110, 20111111, 20111112, 20111113, 20111114,
    20111115, 20111116, 20111117, 20111118, 20111119, 20111120, 20111121,
    20111122, 20111123, 20111124, 20111125, 20111126, 20111127, 20111128,
    20111129, 20111130, 20111201, 20111202, 20111203, 20111204, 20111205,
    20111206, 20111207, 20111208, 20111209, 20111210, 20111211, 20111212,
    20111213, 20111214, 20111215, 20111216, 20111217, 20111218, 20111219,
    20111220, 20111221, 20111222, 20111223, 20111224, 20111225, 20111226,
    20111227, 20111228, 20111229, 20111230, 20111231, 20120101, 20120102,
    20120103, 20120104, 20120105, 20120106, 20120107, 20120108, 20120109,
    20120110, 20120111, 20120112, 20120113, 20120114, 20120115, 20120116,
    20120117, 20120118, 20120119, 20120120, 20120121, 20120122, 20120123,
    20120124, 20120125, 20120126, 20120127, 20120128, 20120129, 20120130,
    20120131, 20120201, 20120202, 20120203, 20120204, 20120205, 20120206,
    20120207, 20120208, 20120209, 20120210, 20120211, 20120212, 20120213,
    20120214, 20120215, 20120216, 20120217, 20120218, 20120219, 20120220,
    20120221, 20120222, 20120223, 20120224, 20120225, 20120226, 20120227,
    20120228, 20120229, 20120301, 20120302, 20120303, 20120304, 20120305,
    20120306, 20120307, 20120308, 20120309, 20120310, 20120311, 20120312,
    20120313, 20120314, 20120315, 20120316, 20120317, 20120318, 20120319,
    20120320, 20120321, 20120322, 20120323, 20120324, 20120325, 20120326,
    20120327, 20120328, 20120329, 20120330, 20120331, 20120401, 20120402,
    20120403, 20120404, 20120405, 20120406, 20120407, 20120408, 20120409,
    20120410, 20120411, 20120412, 20120413, 20120414, 20120415, 20120416,
    20120417, 20120418, 20120419, 20120420, 20120421, 20120422, 20120423,
    20120424, 20120425, 20120426, 20120427, 20120428, 20120429, 20120430,
    20120501, 20120502, 20120503, 20120504, 20120505, 20120506, 20120507,
    20120508, 20120509, 20120510, 20120511, 20120512, 20120513, 20120514,
    20120515, 20120516, 20120517, 20120518, 20120519, 20120520, 20120521,
    20120522, 20120523, 20120524, 20120525, 20120526, 20120527, 20120528,
    20120529, 20120530, 20120531, 20120601, 20120602, 20120603, 20120604,
    20120605, 20120606, 20120607, 20120608, 20120609, 20120610, 20120611,
    20120612, 20120613, 20120614, 20120615, 20120616, 20120617, 20120618,
    20120619, 20120620, 20120621, 20120622, 20120623, 20120624, 20120625,
    20120626, 20120627, 20120628, 20120629, 20120630, 20120701, 20120702,
    20120703, 20120704, 20120705, 20120706, 20120707, 20120708, 20120709,
    20120710, 20120711, 20120712, 20120713, 20120714, 20120715, 20120716,
    20120717, 20120718, 20120719, 20120720, 20120721, 20120722, 20120723,
    20120724, 20120725, 20120726, 20120727, 20120728, 20120729, 20120730,
    20120731, 20120801, 20120802, 20120803, 20120804, 20120805, 20120806,
    20120807, 20120808, 20120809, 20120810, 20120811, 20120812, 20120813,
    20120814, 20120815, 20120816, 20120817, 20120818, 20120819, 20120820,
    20120821, 20120822, 20120823, 20120824, 20120825, 20120826, 20120827,
    20120828, 20120829, 20120830, 20120831, 20120901, 20120902, 20120903,
    20120904, 20120905, 20120906, 20120907, 20120908, 20120909, 20120910,
    20120911, 20120912, 20120913, 20120914, 20120915, 20120916, 20120917,
    20120918, 20120919, 20120920, 20120921, 20120922, 20120923, 20120924,
    20120925, 20120926, 20120927, 20120928, 20120929, 20120930, 20121001,
    20121002, 20121003, 20121004, 20121005, 20121006, 20121007, 20121008,
    20121009, 20121010, 20121011, 20121012, 20121013, 20121014, 20121015,
    20121016, 20121017, 20121018, 20121019, 20121020, 20121021, 20121022,
    20121023, 20121024, 20121025, 20121026, 20121027, 20121028, 20121029,
    20121030, 20121031, 20121101, 20121102, 20121103, 20121104, 20121105,
    20121106, 20121107, 20121108, 20121109, 20121110, 20121111, 20121112,
    20121113, 20121114, 20121115, 20121116, 20121117, 20121118, 20121119,
    20121120, 20121121, 20121122, 20121123, 20121124, 20121125, 20121126,
    20121127, 20121128, 20121129, 20121130, 20121201, 20121202, 20121203,
    20121204, 20121205, 20121206, 20121207, 20121208, 20121209, 20121210,
    20121211, 20121212, 20121213, 20121214, 20121215, 20121216, 20121217,
    20121218, 20121219, 20121220, 20121221, 20121222, 20121223, 20121224,
    20121225, 20121226, 20121227, 20121228, 20121229, 20121230, 20121231,
    20130101, 20130102, 20130103, 20130104, 20130105, 20130106, 20130107,
    20130108, 20130109, 20130110, 20130111, 20130112, 20130113, 20130114,
    20130115, 20130116, 20130117, 20130118, 20130119, 20130120, 20130121,
    20130122, 20130123, 20130124, 20130125, 20130126, 20130127, 20130128,
    20130129, 20130130, 20130131, 20130201, 20130202, 20130203, 20130204,
    20130205, 20130206, 20130207, 20130208, 20130209, 20130210, 20130211,
    20130212, 20130213, 20130214, 20130215, 20130216, 20130217, 20130218,
    20130219, 20130220, 20130221, 20130222, 20130223, 20130224, 20130225,
    20130226, 20130227, 20130228, 20130301, 20130302, 20130303, 20130304,
    20130305, 20130306, 20130307, 20130308, 20130309, 20130310, 20130311,
    20130312, 20130313, 20130314, 20130315, 20130316, 20130317, 20130318,
    20130319, 20130320, 20130321, 20130322, 20130323, 20130324, 20130325,
    20130326, 20130327, 20130328, 20130329, 20130330, 20130331, 20130401,
    20130402, 20130403, 20130404, 20130405, 20130406, 20130407, 20130408,
    20130409, 20130410]    
