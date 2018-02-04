# -*- coding: utf-8 -*-
import pybitflyer
import time

class API:

    #初期化
    def __init__(self):
        self.public_api = pybitflyer.API()
        self.api = pybitflyer.API(api_key="TH8bgpMj9opE1CnzAqEkt9", api_secret="A5lDwm0Lsx8Phav34hiKxi4fuyNAk6CJE2o2TyIR5M8=")
        self.product_code = "FX_BTC_JPY"

    #注文用のメソッド(price = 0 なら成行)
    def placeOrder(self,side,price,size):

        if price == 0:
            self.api.sendchildorder(product_code = self.product_code,child_order_type = "MARKET",side = side , size = size)

        else:
            self.api.sendchildorder(product_code = self.product_code,child_order_type = "LIMIT",side = side , size = size,price = price)

    #建玉情報の取得メソッド
    def getmypos(self):
        side = ""
        size = 0
        poss = self.api.getpositions(product_code = self.product_code)

        #もしポジションがあれば合計値を取得
        if len(poss) != 0:
            for pos in poss:
                side = pos["side"]
                size += pos["size"]

        return side,size

    #中間価格の取得
    def getMidprice(self):
        midprice = self.public_api.board(product_code = self.product_code)["mid_price"]
        return midprice

    #すべての注文をキャンセル
    def cancelAllOrder(self):
        api.cancelallchildorders(product_code = self.product_code)


def main():
    midprice = 0
    before_midprice = 0
    mypos_side = ""
    mypos_size = 0
    size = 0.001

    #インスタンスの作成
    api = API()

    #中間価格の初期化
    midprice = before_midprice = api.getMidprice()

    #メインループ
    while True:
        time.sleep(10)

        #現在の中間価格を取得
        midprice = api.getMidprice()
        #自分のポジションを取得
        mypos_side, mypos_size = api.getmypos()

        #注文の全キャンセル

        #ポジションがあれば決済
        if mypos_size != 0:
            if mypos_side == "BUY":
                print("Close Long position")
                api.placeOrder("SELL",0,mypos_size)

            elif mypos_side == "SELL":
                print("Close Short position")
                api.placeOrder("BUY",0,mypos_size)

            before_midprice = midprice # 価格をシフト
            continue


        #10秒前より価格が高い時
        if midprice - before_midprice > 0:
                print("Long Entry")
                api.placeOrder("BUY",midprice,size) #ロングエントリー

        #1分前より価格が低い時
        if before_midprice - midprice > 0:
                print("Short Entry")
                api.placeOrder("SELL",midprice,size) #ショートエントリー

        before_midprice = midprice # 価格をシフト


if __name__ == "__main__":
    main()
