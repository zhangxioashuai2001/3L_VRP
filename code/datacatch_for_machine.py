import numpy as np
import pandas as pd
import os
from typing import List


class LoadMasterData:
    def __init__(self, path, sheet):
        self.path = path
        self.sheet = sheet
        self.rawdata = None
        self.indexlist = []
        self.readdata()

        self.ifloaded=self.__ifloaded()
        self.sku_counts: List[int] = self.__getskuCounts()
        self.total_skuvolume: List[float] = self.__gettotalskuVolume()
        self.sku_average_volume: List[float] = self.__getskuaveragevolume(self.total_skuvolume, self.sku_counts)
        self.aspect_ratio_avg: List[float] = self.__getasravg()
        self.aspect_ratio_var: List[float] = self.__getasrvar()
        self.vehicle_capacity: List[float] = self.__getvehiclecapacity()
        self.sku_length_avg: List[float] = self.__getsku_length_avg()
        self.sku_width_avg:  List[float] = self.__getsku_width_avg()
        self.sku_height_avg: List[float] = self.__getsku_height_avg()
        self.sku_length_var: List[float] = self.__getsku_length_var()
        self.sku_width_var: List[float] = self.__getsku_width_var()
        self.sku_height_var: List[float] = self.__getsku_height_var()
        self.max_asr: List[float] = self.__getmaxasr()
        self.spare_capacity: List[float] = self.__getspare_capacity()
        self.cpnumber = self.__cpnumber()
        self.sku_concentration: List[float] = self.__getsku_concentration()

    def generateExcel(self, encoding='utf-8') -> None:
        column_names = ['发车号', 'if_loaded', 'sku_counts', 'total_skuvolume', 'sku_average_volume', 'sku_length_var',
                        'sku_width_var', 'sku_height_var', 'aspect_ratio_var', 'vehicle_capacity', 'sku_length_avg',
                        'sku_width_avg', 'sku_height_avg', 'max_asr','vehicle_length','vehicle_width','vehicle_height','spare_capacity', 'sku_concentration']
        # 创建空的数据框
        df = pd.DataFrame(columns=column_names)
        print(len(df.index))
        # 向数据框中填入数据
        df['if_loaded'] = self.ifloaded
        df['sku_counts'] = self.sku_counts
        df['total_skuvolume'] = self.total_skuvolume
        df['sku_average_volume'] = self.sku_average_volume
        df['sku_length_var'] = self.sku_length_var
        df['sku_width_var'] = self.sku_width_var
        df['sku_height_var'] = self.sku_height_var
        df['aspect_ratio_var'] = self.aspect_ratio_var
        df['vehicle_capacity'] = self.vehicle_capacity
        df['sku_length_avg'] = self.sku_length_avg
        df['sku_width_avg'] = self.sku_width_avg
        df['sku_height_avg'] = self.sku_height_avg
        df['max_asr'] = self.max_asr
        # df['skuconcentration'] = self.skuconcentration
        df['发车号'] = self.cpnumber
        df['vehicle_length'] = 40
        df['vehicle_width'] = 20
        df['vehicle_height'] = 20
        df['spare_capacity'] = self.spare_capacity
        df['sku_concentration'] = self.sku_concentration

        # 创建目录路径
        folder_path = 'svm'
        csv_file_path = os.path.join(folder_path, 'training.csv')
        df.to_csv(csv_file_path, index=True, index_label='orderid', encoding='gbk')

    def readdata(self) -> None:
        self.rawdata = pd.read_excel(self.path, sheet_name=self.sheet)
        self.__getindexlist()
        self.indexlist.append([len(self.rawdata),0])

    def __cpnumber(self) -> list:
        cpnumberlist = []
        for i in range(len(self.indexlist) - 1):
            startindex: int = self.indexlist[i][0]
            cpnumberlist.append(str(self.rawdata.iloc[startindex]["发车号"]))
        return cpnumberlist

    def __ifloaded(self)->list:
        ifloadedlist = []
        for i in range(len(self.indexlist) - 1):
            ifloadedlist.append(self.indexlist[i][1])
        return ifloadedlist

    # def __getindexlist(self) -> None:
    #     for r in self.rawdata.index:
    #         if not np.isnan(self.rawdata.loc[r]["if_loaded"]):
    #             self.indexlist.append([r, self.rawdata.loc[r]["if_loaded"]])

    def __getindexlist(self) -> None:
        current_cpnumber = None
        for r in self.rawdata.index:
            cpnumber = self.rawdata.loc[r]["发车号"]
            if cpnumber != current_cpnumber:
                self.indexlist.append([r, self.rawdata.loc[r]["if_loaded"]])
                current_cpnumber = cpnumber

    def __getlength(self, i: int) -> float:
        it = self.rawdata.loc[i]
        length: float = it["SKU长度"]
        return length

    def __getwidth(self, i: int) -> float:
        it = self.rawdata.loc[i]
        width: float = it["SKU宽度"]
        return width

    def __getheight(self, i: int) -> float:
        it = self.rawdata.loc[i]
        height: float = it["SKU高度"]
        return height

    def __getvolume(self, i: int) -> float:
        l: float = self.__getlength(i)
        w: float = self.__getwidth(i)
        h: float = self.__getheight(i)
        volume: float = l * w * h
        return volume

    #返回第i个item的asr
    def __getasr(self, i: int) -> float:
        l: float = self.__getlength(i)
        w: float = self.__getwidth(i)
        h: float = self.__getheight(i)
        waitinglist: list = [l, w, h]
        asrlist: list = [l/w,w/l,l/h,h/l,w/h,h/w]
        return max(asrlist)

    def __getmaxasr(self) -> List[float]:
        maxasrlist: List[float]=[]
        for i in range(len(self.indexlist) - 1):
            asrlist: List[float] = []
            startindex: int = self.indexlist[i][0]
            endindex: int = self.indexlist[i + 1][0]
            for j in range(startindex,endindex):
                asrlist.append(self.__getasr(j))
            maxasrlist.append(max(asrlist))
        return maxasrlist

    def __getasrvar(self) ->List[float]:
        asrvarlist: List[float] = []
        for i in range(len(self.indexlist) - 1):
            asrlist: List[float] = []
            startindex: int = self.indexlist[i][0]
            endindex: int = self.indexlist[i + 1][0]
            for j in range(startindex, endindex):
                asrlist.append(self.__getasr(j))
            asrvar = np.average((asrlist-self.aspect_ratio_avg[i])**2)
            asrvarlist.append(asrvar)
        return asrvarlist

    def __getasravg(self) ->List[float]:
        asravglist: List[float] = []
        for i in range(len(self.indexlist) - 1):
            asrlist: List[float] = []
            startindex: int = self.indexlist[i][0]
            endindex: int = self.indexlist[i + 1][0]
            for j in range(startindex,endindex):
                asrlist.append(self.__getasr(j))
            asravg = np.average(asrlist)
            asravglist.append(asravg)
        return asravglist

    def __getvehiclecapacity(self) ->List[float]:
        vehiclecaplist: List[float] = []
        for i in range(len(self.indexlist) - 1):
            index: int = self.indexlist[i][0]
            vehiclecaplist.append(self.rawdata.iloc[index]['车辆总容积(m3)'])
        return vehiclecaplist

    # 返回第i行的item数目
    def __getcountnumber(self, i: int) -> int:
        countnumber: int = 1
        return countnumber

    # 生成每个sample的总items数量的list
    def __getskuCounts(self) -> List[int]:
        sku_counts: List[int] = []
        for i in range(len(self.indexlist) - 1):
            startindex: int = self.indexlist[i][0]
            endindex: int = self.indexlist[i + 1][0]
            countnumber: int = self.rawdata.iloc[startindex:endindex]['发车号'].count()
            sku_counts.append(countnumber)
        return sku_counts

    def __gettotalskuVolume(self) -> List[float]:
        totalskuvolumelist: List[float] = [
            sum((self.__getvolume(j)) * (self.__getcountnumber(j)) for j in
                range(self.indexlist[i][0], self.indexlist[i + 1][0]))
            for i in range(len(self.indexlist) - 1)
        ]
        return totalskuvolumelist
    def __getspare_capacity(self) -> List[float]:
        spare_capacity: List[float] = [
            self.vehicle_capacity[j] - self.total_skuvolume[j] for j in range(len(self.indexlist) - 1)
        ]
        return  spare_capacity


    def __getskuaveragevolume(self, lista: list, listb: list) -> List[float]:
        averageskuvolumelist: List[float] = [a / b for a, b in zip(lista, listb)]
        return averageskuvolumelist

    # 返回每个sample中的length的平均值
    def __getsku_length_avg(self) -> List[float]:
        skulenavglist: List[float] = []
        for i in range(len(self.indexlist) - 1):
            startindex: int = self.indexlist[i][0]
            endindex: int = self.indexlist[i + 1][0]
            skulenavg: float = np.average(self.rawdata.iloc[startindex:endindex]['SKU长度'])
            skulenavglist.append(skulenavg)
        return skulenavglist

    # #返回每个sample中的sku种类数skuconcentration
    # def __getsku_concentration(self) -> List[int]:
    #     skuconcentrationlist: List[int] = []
    #     for i in range(len(self.indexlist) - 1):
    #         startindex: int = self.indexlist[i][0]
    #         endindex: int = self.indexlist[i + 1][0]
    #         subset = self.rawdata.iloc[startindex:endindex, self.rawdata.columns.get_loc("商品ID")]
    #         # 统计不重复数据的个数
    #         unique_count = subset.nunique()
    #         skuconcentrationlist.append(unique_count)
    #     return skuconcentrationlist

    # 返回每个sample中的width的平均值
    def __getsku_width_avg(self) -> List[float]:
        skuwidavglist: List[float] = []
        for i in range(len(self.indexlist) - 1):
            startindex: int = self.indexlist[i][0]
            endindex: int = self.indexlist[i + 1][0]
            skuwidavg = np.average(self.rawdata.iloc[startindex:endindex]['SKU宽度'])
            skuwidavglist.append(skuwidavg)
        return skuwidavglist

        # 返回每个sample中的heigth的平均值
    def __getsku_height_avg(self) -> List[float]:
        skuheiavglist: List[float] = []
        for i in range(len(self.indexlist) - 1):
            startindex: int = self.indexlist[i][0]
            endindex: int = self.indexlist[i + 1][0]
            skuheiavg = np.average(self.rawdata.iloc[startindex:endindex]['SKU高度'])
            skuheiavglist.append(skuheiavg)
        return skuheiavglist

    def __getsku_length_var(self) -> List[float]:
        skulenvarlist: List[float] = []
        for i in range(len(self.indexlist) - 1):
            startindex: int = self.indexlist[i][0]
            endindex: int = self.indexlist[i + 1][0]
            skulenvar = np.average((self.rawdata.iloc[startindex:endindex]['SKU长度'] - self.sku_length_avg[i]) ** 2)
            skulenvarlist.append(skulenvar)
        return skulenvarlist

    def __getsku_width_var(self) -> List[float]:
        skuwidvarlist: List[float] = []
        for i in range(len(self.indexlist) - 1):
            startindex: int = self.indexlist[i][0]
            endindex: int = self.indexlist[i + 1][0]
            skuwidvar = np.average((self.rawdata.iloc[startindex:endindex]['SKU宽度'] - self.sku_width_avg[i]) ** 2)
            skuwidvarlist.append(skuwidvar)
        return skuwidvarlist

    def __getsku_height_var(self) -> List[float]:
        skuheivarlist: List[float] = []
        for i in range(len(self.indexlist) - 1):
            startindex: int = self.indexlist[i][0]
            endindex: int = self.indexlist[i + 1][0]
            skuheivar = np.average((self.rawdata.iloc[startindex:endindex]['SKU高度'] - self.sku_height_avg[i]) ** 2)
            skuheivarlist.append(skuheivar)
        return skuheivarlist

    def __getsku_concentration(self) -> List[float]:
        sku_concentration: List[float] = []
        for i in range(len(self.indexlist) - 1):
            startindex: int = self.indexlist[i][0]
            endindex: int = self.indexlist[i + 1][0]
            lengths: List[float] = []
            widths: List[float] = []
            heights: List[float] = []
            for j in range(startindex, endindex):
                lengths.append(self.__getlength(j))
                widths.append(self.__getwidth(j))
                heights.append(self.__getheight(j))
            length_cv = np.std(lengths) / np.mean(lengths)
            width_cv = np.std(widths) / np.mean(widths)
            height_cv = np.std(heights) / np.mean(heights)
            concentration = (length_cv + width_cv + height_cv) / 3
            sku_concentration.append(concentration)
        return sku_concentration

def main():
    data = LoadMasterData(path="items.xlsx", sheet = 0 )
    data.readdata()
    print(data.rawdata, data.indexlist,len(data.indexlist),data.sku_counts, data.total_skuvolume,data.ifloaded)
    data.generateExcel()


main()
